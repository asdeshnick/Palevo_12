#include <iostream>
#include <fstream>
#include <string>
#include <chrono>
#include <thread>
#include <filesystem>
#include <curl/curl.h>

namespace fs = std::filesystem;

// Структура для хранения данных о событии
struct EventData {
    std::string computer;
    std::string timestamp;
    std::string user;
    std::string action;
    std::string path;
};

// Функция для отправки POST-запроса на сервер
size_t write_callback(char* ptr, size_t size, size_t nmemb, void* userdata) {
    ((std::string*)userdata)->append(ptr, size * nmemb);
    return size * nmemb;
}

bool send_log(const EventData& data, const std::string& server_url) {
    // Инициализация curl
    CURL* curl = curl_easy_init();
    if (!curl) {
        std::cerr << "Ошибка инициализации curl." << std::endl;
        return false;
    }
    
    // Создание строки JSON для передачи данных
    std::string json_data = R"({"computer":" + data.computer + R"","timestamp":" + data.timestamp + R"","user":" + data.user + R"","action":" + data.action + R"","path":" + data.path + R"}" + ")";

    // Настройка параметров curl
    curl_easy_setopt(curl, CURLOPT_URL, server_url.c_str());
    curl_easy_setopt(curl, CURLOPT_POSTFIELDS, json_data.c_str());
    curl_easy_setopt(curl, CURLOPT_POSTFIELDSIZE, json_data.size());
    curl_easy_setopt(curl, CURLOPT_WRITEFUNCTION, &write_callback);

    // Буфер для ответа сервера
    std::string buffer;
    curl_easy_setopt(curl, CURLOPT_WRITEDATA, &buffer);

    // Выполнение запроса
    CURLcode res = curl_easy_perform(curl);
    if (res != CURLE_OK) {
        std::cerr << "Ошибка выполнения запроса: " << curl_easy_strerror(res) << std::endl;
        curl_easy_cleanup(curl);
        return false;
    }

    long http_code;
    curl_easy_getinfo(curl, CURLINFO_RESPONSE_CODE, &http_code);
    if (http_code == 200) {
        std::cout << "Данные успешно отправлены: " << json_data << std::endl;
    } else {
        std::cerr << "Ошибка при отправке: " << buffer << std::endl;
    }

    curl_easy_cleanup(curl);
    return true;
}

void on_event(const fs::path& path, const std::string& action) {
    auto now = std::chrono::system_clock::now();
    auto in_time_t = std::chrono::system_clock::to_time_t(now);
    std::stringstream ss;
    ss << std::put_time(std::localtime(&in_time_t), "%F %T");

    EventData data{
        .computer = "localhost",
        .timestamp = ss.str(),
        .user = "unknown",
        .action = action,
        .path = path.string()
    };

    bool success = send_log(data, "http://127.0.0.1:8000/log");
    if (success) {
        std::cout << "Лог отправлен успешно!" << std::endl;
    } else {
        std::cerr << "Не удалось отправить лог!" << std::endl;
    }
}

int main(int argc, char* argv[]) {
    std::vector<fs::path> paths_to_watch;

    // Загружаем список путей из файла
    std::ifstream file("watch_list.txt");
    if (file.is_open()) {
        std::string line;
        while (getline(file, line)) {
            if (!line.empty()) {
                paths_to_watch.push_back(line);
            }
        }
        file.close();
    } else {
        std::cerr << "Не удалось открыть файл 'watch_list.txt'." << std::endl;
        return 1;
    }

    if (paths_to_watch.empty()) {
        std::cerr << "Список путей пустой." << std::endl;
        return 1;
    }

    // Мониторинг изменений
    for (const auto& path : paths_to_watch) {
        if (fs::exists(path)) {
            std::cout << "Следим за: " << path << std::endl;
            while (true) {
                auto last_write_time = fs::last_write_time(path);
                std::this_thread::sleep_for(std::chrono::seconds(1));
                auto new_last_write_time = fs::last_write_time(path);
                if (new_last_write_time > last_write_time) {
                    on_event(path, "modified");
                }
            }
        } else {
            std::cerr << "Путь '" << path << "' не существует или недоступен." << std::endl;
        }
    }

    return 0;
}

