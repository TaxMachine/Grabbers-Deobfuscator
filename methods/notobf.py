import re, os, codecs, subprocess
from utils.deobfuscation import BlankOBF
from utils.decompile import strings
class NotObfuscated:
    def __init__(self, dir):
        self.extractiondir = dir
        self.tempdir = os.path.join(self.extractiondir, "..", "..", "temp")

    def GetWebhook(self):
        for root, subdirs, files in os.walk(self.extractiondir):
            for file in files:
                if file.endswith(".pyc"):
                    path = os.path.join(root, file)
                    #print(path)
                    # yeah fuck you I use strings
                    with open(path, "rb") as f:
                        strs = strings(f.read())
                    try:
                        webhook = BlankOBF.MatchWebhook(strs)
                        return webhook
                    except ValueError:
                        pass