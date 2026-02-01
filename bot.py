import json
import TelegramTextApp
from TelegramTextApp import config
import api
from TelegramTextApp.utils.utils import print_json


def get_inbounds(tta):
    inbounds = api.get_inbounds()
    if inbounds is None:
        return {}
    keyboard = {}
    for inbound in inbounds:
        keyboard[f"role:admin|inbound|{inbound['id']}"] = f"{inbound['remark']}"
    return keyboard


def get_inbound(tta):
    inbounds = api.get_inbound(tta.inbound_id)
    if inbounds is None:
        return {"text": "Ошибка при получении inbound'а"}
    inbounds["streamSettings"] = json.loads(inbounds["streamSettings"])
    inbounds["settings"] = json.loads(inbounds["settings"])
    inbounds["num_clients"] = len(inbounds["settings"]["clients"])
    return inbounds


def inbound_clients(tta):
    inbound = api.get_inbound(tta.inbound_id)
    if inbound is None:
        return {"text": "Ошибка при получении inbound'а"}
    inbound["settings"] = json.loads(inbound["settings"])
    clients = inbound["settings"]["clients"]
    keyboard = {}
    for client in clients:
        key = f"inbound|{inbound['id']}|{client['id']}"
        value = f"{client['email']}"
        keyboard[key] = value

    return keyboard


def get_inbound_client(tta):
    inbound = api.get_inbound(tta.inbound_id)
    if inbound is None:
        return {"text": "Ошибка при получении inbound'а"}
    inbound["settings"] = json.loads(inbound["settings"])
    clients = inbound["settings"]["clients"]
    for client in clients:
        if client["id"] == tta.inbound_client_id:
            return client


def get_test_token(tta):
    inbound_id = config.TEST_INBOUND
    client = api.get_client(inbound_id, tta.user.telegram_id, placeholder="test-")
    if client is None:
        api.create_client(
            inbound_id, tta.user.telegram_id, tta.user.username, total_gb=1
        )
        client = api.get_client(inbound_id, tta.user.telegram_id, placeholder="test-")
    return {"client": client}


if __name__ == "__main__":
    TelegramTextApp.start()
