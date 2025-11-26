import TelegramTextApp
from TelegramTextApp.utils.database import SQL_request as SQL  # type: ignore
import subprocess
import sys


def create_tokens():
    SQL("""
    CREATE TABLE IF NOT EXISTS configs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER NOT NULL,
        config TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        active_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        active BOOLEAN DEFAULT 1,
        FOREIGN KEY (user_id) REFERENCES TTA(id)
    )""")


create_tokens()


def create_config(tta_data):
    username = tta_data.get("username", "NoUsername")
    last_id = SQL("SELECT * FROM configs ORDER BY id DESC LIMIT 1;", fetch="one")

    try:
        # Запускаем команду openvpn
        process = subprocess.Popen(
            ["openvpn"],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

        config_name = f"{username}_{last_id[0] if last_id else 0}"

        # Отправляем '1' для выбора пункта "Add a new client"
        stdout, stderr = process.communicate(input=f"1\n{config_name}\n")

        SQL(
            f"INSERT INTO configs (user_id, config) VALUES ({tta_data['id']}, '{config_name}');"
        )

    except FileNotFoundError:
        print(
            "Ошибка: команда 'openvpn' не найдена. Убедитесь, что OpenVPN установлен."
        )
    except Exception as e:
        print(f"Произошла ошибка: {e}")
    return


if __name__ == "__main__":
    TelegramTextApp.start()  # type: ignore
