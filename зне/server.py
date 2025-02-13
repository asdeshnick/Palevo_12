from flask import Flask, request, jsonify
import os
from datetime import datetime

app = Flask(__name__)

LOG_FILE = "activity_log.txt"

@app.route('/log', methods=['POST'])
def log_activity():
    """
    Эндпоинт для записи информации о действиях.
    Ожидается JSON с json-структурой:
    {
        "computer": "имя компьютера",
        "timestamp": "время действия",
        "user": "пользователь",
        "action": "открытие/просмотр/изменение",
        "path": "путь к файлу или папке"
    }
    """
    try:
        data = request.json

        if not data:
            return jsonify({"status": "error", "message": "Empty request body"}), 400

        entry = (f"{data['timestamp']} - [Computer: {data['computer']}] [User: {data['user']}] "
                 f"[Action: {data['action']}] [Path: {data['path']}]\n")

        with open(LOG_FILE, "a", encoding="utf-8") as log_file:
            log_file.write(entry)

        print(f"Logged activity: {entry.strip()}")
        return jsonify({"status": "success", "message": "Activity logged"}), 200

    except KeyError as e:
        return jsonify({"status": "error", "message": f"Missing key: {e}"}), 400

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000)