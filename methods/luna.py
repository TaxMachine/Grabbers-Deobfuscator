import os
from utils.deobfuscation import BlankStage3, BlankStage4

class LunaDeobf:
    def __init__(self, dir, entries):
        self.extractiondir = dir
        self.entries = entries
        self.tempdir = os.path.join(self.extractiondir, "..", "..", "temp")

    def Deobfuscate(self):
        for entry in self.entries:
            if 'pyi' not in entry:
                file = entry
        f = open(self.extractiondir + os.path.sep + file, "rb")
        assembly = f.read()
        f.close()
        stage3 = BlankStage3(assembly)
        webhook = BlankStage4(stage3)
        return webhook