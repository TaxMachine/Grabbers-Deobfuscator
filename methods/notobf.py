import re, os, codecs, subprocess
from utils.deobfuscation import BlankOBF

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
                    strings = subprocess.run(["strings", path], stdout=subprocess.PIPE).stdout.decode()
                    try:
                        webhook = BlankOBF.MatchWebhook(strings)
                        return webhook
                    except ValueError:
                        pass