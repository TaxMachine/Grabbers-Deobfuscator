import os
from utils.deobfuscation import MatchWebhook
from utils.decompile import strings


class BenDeobf:
    def __init__(self, dir):
        self.dir = dir

    def Deobfuscate(self):
        for root, _, files in os.walk(self.dir):
            for file in files:
                if file.endswith(".class"):
                    path = os.path.join(root, file)
                    with open(path, "rb") as f:
                        strs = strings(f.read())
                    try:
                        webhook = MatchWebhook(strs)
                        return webhook
                    except ValueError:
                        pass
