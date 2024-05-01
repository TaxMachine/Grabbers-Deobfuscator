import base64, os, subprocess, zlib, zipfile, re, lzma, codecs, base64
from utils.decompile import decompilePyc, disassemblePyc
from utils.deobfuscation import BlankStage3, BlankStage4

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
        stage3 = BlankStage3(assembly)
        webhook = BlankStage4(stage3)
        return webhook