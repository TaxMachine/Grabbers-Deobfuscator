import re, os, codecs, subprocess
from utils.deobfuscation import MatchWebhook
from utils.decompile import strings
class NotObfuscated:
    def __init__(self, dir):
        self.extractiondir = dir
        self.tempdir = os.path.join(self.extractiondir, "..", "..", "temp")

    def GetWebhook(self):
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
