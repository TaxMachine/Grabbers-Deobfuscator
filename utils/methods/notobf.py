import os
from deobfuscation import MatchWebhook # type: ignore
from decompile import strings # type: ignore
class NotObfuscated:
    def __init__(self, dir, entries):
        self.extractiondir = dir
        self.entries = entries
        self.tempdir = os.path.join(self.extractiondir, "..", "..", "temp")

    def Deobfuscate(self):
        for root, _, files in os.walk(self.extractiondir):
            for file in files:
                if file.endswith(".pyc"):
                    path = os.path.join(root, file)
                    with open(path, "rb") as f:
                        strs = strings(f.read())
                    try:
                        webhook = MatchWebhook(strs)
                        return webhook
                    except ValueError:
                        pass
