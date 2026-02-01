import json
import uuid
import requests
from TelegramTextApp import config
from TelegramTextApp.utils.logger import setup as setup_logger


logger = setup_logger("API")
headers = {"Cookie": config.API_TOKEN}


def create_client_body(tgid, username="", total_gb=0, expiry_time=0):
    body = {
        "clients": [
            {
                "id": str(uuid.uuid4()),
                "flow": "",
                "email": f"test-{tgid}",
                "limitIp": 0,
                "totalGB": total_gb,
                "expiryTime": expiry_time,
                "enable": True,
                "tgId": "",
                "subId": str(uuid.uuid4()),
                "comment": username,
                "reset": 0,
            }
        ]
    }
    return json.dumps(body)


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


def get_client(inbound_id, tg_id, placeholder=""):
    data = get_inbound(inbound_id)
    clients = data["settings"]
    clients = json.loads(clients)["clients"]
    for client in clients:
        if client["email"] == placeholder + str(tg_id):
            return client
    return None


def create_client(inbound_id, tgid, username, total_gb=0, expiry_time=0):
    inbound_id = inbound_id
    response = requests.post(
        f"{config.URL}/inbounds/addClient",
        headers=headers,
        data={
            "id": inbound_id,
            "settings": create_client_body(tgid, username, total_gb, expiry_time),
        },
    )
    if response.json().get("success") is True:
        return None

    logger.error(
        f"Не удалось создать тестового клиента для inbound с id {inbound_id}: {response.json().get('msg')}"
    )
    return {
        "error_message": f"Не удалось добавить клиента. {response.json().get('msg')}"
    }
