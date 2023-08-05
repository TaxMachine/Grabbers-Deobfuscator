import os, re, subprocess
from utils.deobfuscation import BlankOBF

class BenDeobf:
    def __init__(self, dir):
        self.dir = dir
        
    def Deobfuscate(self):
       for root, subdirs, files in os.walk(self.dir):
            for file in files:
                if file.endswith(".pyc"):
                    path = os.path.join(root, file)
                    strings = subprocess.run(["strings", path], stdout=subprocess.PIPE).stdout.decode()
                    try:
                        webhook = BlankOBF.MatchWebhook(strings)
                        return webhook
                    except ValueError:
                        pass