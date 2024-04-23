import json
import requests

from utils.config import Config


class Telegram:
    def __init__(self, token: str):
        self.token = token
        self.username = None
        self.firstName = None
        self.dump = None
        self.config = Config.getConfig()

    @staticmethod
    def CheckValid(token):
        r = requests.get(f"https://api.telegram.org/bot{token}/getMe")
        return r.status_code == 200

    def SendMessage(self, chat_id: str):
        payload = {
            "chat_id": "@" + chat_id,
            "text": self.config["telegram_message"]
        }
        r = requests.post(
            f"https://api.telegram.org/bot{self.token}/message",
            json=payload,
            headers={"Content-Type": "application/json"})
        if not r.json()["ok"]:
            print(r.json()["description"])

    def GetInformations(self):
        if not self.CheckValid(self.token):
            raise IOError("Invalid bot token")
        r = requests.get(f"https://api.telegram.org/bot{self.token}/getMe")
        parsed = r.json()
        self.username = parsed["result"]["username"]
        self.firstName = parsed["result"]["first_name"]
        self.dump = parsed["result"]["can_read_all_group_messages"]
