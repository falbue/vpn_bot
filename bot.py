import json
import TelegramTextApp
import api


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
        keyboard[f"inbound|{inbound['id']}|client|{client['id']}"] = (
            f"{client['email']}"
        )
    return keyboard


if __name__ == "__main__":
    TelegramTextApp.start()  # type: ignore
