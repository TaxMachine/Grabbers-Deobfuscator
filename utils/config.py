import json

from os.path import dirname, exists, join


class Config:
    def __init__(self):
        if not exists(join(dirname(__file__), "..", "config.json")):
            f = open(join(dirname(__file__), "..", "config.json"))
            f.write(json.dumps({
                "deletemessage": {
                    "content": ":clown: Webhook deleted fucking skid"
                },
                "spammessage": {
                    "content": "lmao nerd you thought :nerd:"
                },
                "deleteafterdeobf": True,
                "telegram_message": "lmfao get fucked retard"
            }, indent=4))
            f.close()

    @staticmethod
    def getConfig():
        f = open(join(dirname(__file__), "..", "config.json"))
        parsed = json.loads(f.read())
        f.close()
        return parsed
