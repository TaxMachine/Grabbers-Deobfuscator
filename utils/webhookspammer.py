from os.path import exists, join, dirname

import json
import requests
import time

from utils.config import Config


class Webhook:
    def __init__(self, webhook):
        self.name = None
        self.author_id = None
        self.author = None
        self.config = Config.getConfig()
        self.webhook = webhook

    @staticmethod
    def CheckValid(webhook):
        r = requests.get(webhook)
        return r.status_code == 200

    def DeleteWebhook(self):
        if not self.CheckValid(self.webhook):
            raise IOError("Invalid Webhook")
        requests.post(self.webhook, headers={"Content-Type": "application/json"}, json=self.config["deletemessage"])
        requests.delete(self.webhook)

    def SendWebhook(self):
        if not self.CheckValid(self.webhook):
            raise IOError("Invalid webhook")
        r = requests.post(self.webhook, headers={"Content-Type": "application/json"}, json=self.config["spammessage"])
        match r.status_code:
            case 429:
                print("[-] Rate limited, waiting 5 seconds")
                time.sleep(5)
            case 404:
                print("[-] Webhook got deleted")
                quit(0)

    def GetInformations(self):
        if not self.CheckValid(self.webhook):
            raise IOError("Invalid token")
        r = requests.get(self.webhook)
        payload = r.json()
        self.author = payload["user"]["username"]
        self.author_id = payload["user"]["id"]
        self.name = payload["name"]

    @staticmethod
    def GetDeleteConfig():
        f = open(join(dirname(__file__), "..", "config.json"))
        config = json.loads(f.read())
        f.close()
        return config["deleteafterdeobf"]
