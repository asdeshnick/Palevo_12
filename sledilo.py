import os
import time
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime
import socket

SERVER_URL = "http://127.0.0.1:8000/log"
WATCH_LIST_FILE = "watch_list.txt"

class WatcherHandler(FileSystemEventHandler):
    def on_modified(self, event):
        print(f"[{datetime.now()}] Изменён файл: {event.src_path}")
        self.send_log(event.src_path, "modified")

    def on_created(self, event):
        print(f"[{datetime.now()}] Создан файл: {event.src_path}")
        self.send_log(event.src_path, "created")

    def on_deleted(self, event):
        print(f"[{datetime.now()}] Удалён файл: {event.src_path}")
        self.send_log(event.src_path, "deleted")

    def send_log(self, path, action):
        data = {
            "computer": socket.gethostname(),
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "user": "unknown",
            "action": action,
            "path": str(path),
        }
        try:
            response = requests.post(SERVER_URL, json=data)
            if response.status_code == 200:
                print(f"[{datetime.now()}] Данные успешно отправлены: {data}")
            else:
                print(f"[{datetime.now()}] Ошибка при отправке: {response.text}")
        except Exception as e:
            print(f"[{datetime.now()}] Не удалось отправить данные на сервер: {e}")

def load_watch_list():
    if not os.path.exists(WATCH_LIST_FILE):
        print(f"Файл {WATCH_LIST_FILE} не найден!")
        return []
    with open(WATCH_LIST_FILE, "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def track_file_usage(targets):
    observer = Observer()
    for target in targets:
        target = target.strip()
        if os.path.exists(target):
            print(f"Начинаю следить за: {target}")
            observer.schedule(WatcherHandler(), path=target, recursive=False)
        else:
            print(f"Путь {target} не существует или недоступен.")

    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

def main():
    print("Загрузка списка отслеживаемых путей...")
    targets = load_watch_list()
    if not targets:
        print("Список путей пуст или отсутствует.")
        return
    print("Список для отслеживания:", targets)

    print(f"Старт отслеживания...")
    track_file_usage(targets)

if __name__ == "__main__":
    main()