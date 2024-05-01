import base64, os, subprocess, zlib, zipfile, re, lzma, codecs, base64
from utils.decompile import decompilePyc, disassemblePyc
from utils.deobfuscation import BlankOBF

class LunaDeobf:
    def __init__(self, dir, entries):
        self.extractiondir = dir
        self.entries = entries
        self.tempdir = os.path.join(self.extractiondir, "..", "..", "temp")

    def Deobfuscate(self):
        file = self.extractiondir.split(".exe")[0].split(os.path.sep)[len(self.extractiondir.split(os.path.sep)) - 1] + ".pyc"
        f = open(self.extractiondir + os.path.sep + file, "rb")
        assembly = f.read()
        f.close()
        stage3 = BlankOBF.DeobfuscateStage3(assembly)
        webhook = BlankOBF.DeobfuscateStage4(stage3.first, stage3.second, stage3.third, stage3.fourth)
        return webhook