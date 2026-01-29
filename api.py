import json
import requests
from TelegramTextApp import config
from TelegramTextApp.utils.logger import setup as setup_logger


logger = setup_logger("API")
headers = {"Cookie": config.API_TOKEN}


def print_json(data):  # удобный вывод json
    try:
        if isinstance(data, (dict, list)):
            text = json.dumps(data, indent=4, ensure_ascii=False)
        else:
            print(type(data))
            text = str(data)
        print(text)
    except Exception as e:
        logger.error(f"Ошибка при выводе json: {e}")


def get_inbounds():
    response = requests.get(f"{config.URL}/inbounds/list", headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data["obj"]
    logger.error(
        f"Не удалось получить список inbound'ов: {response.status_code} - {response.text}"
    )
    return None


def get_inbound(inbound_id):
    response = requests.get(f"{config.URL}/inbounds/get/{inbound_id}", headers=headers)
    if response.status_code == 200:
        data = response.json()
        return data["obj"]
    logger.error(
        f"Не удалось получить inbound с id {inbound_id}: {response.status_code} - {response.text}"
    )
    return None
