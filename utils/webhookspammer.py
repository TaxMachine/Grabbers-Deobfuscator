import requests, json, time
from os.path import exists, join, dirname

class Webhook():
    def __init__(self, webhook):
        self.webhook = webhook
        if not exists(join(dirname(__file__), "..", "config.json")):
            f = open(join(dirname(__file__), "..", "config.json"))
            f.write(json.dumps({
                "deletemessage": {
                    "content": ":clown: Webhook deleted fucking skid"
                },
                "spammessage": {
                    "content": "lmao nerd you thought :nerd:"
                }
            }, indent=4))
            f.close()
        self.getConfig()

    def getConfig(self):
        f = open(join(dirname(__file__), "..", "config.json"))
        self.config = json.loads(f.read())
        f.close()

    def CheckValid(self, webhook):
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
        if not self.CheckValid(self.webhook): raise IOError("Invalid token")
        r = requests.get(self.webhook)
        payload = r.json()
        self.author = payload["user"]["username"]
        self.author_id = payload["user"]["id"]
        self.name = payload["name"]