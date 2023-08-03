import os, re

from utils.decompile import decompilePyc

class VespyDeobf:
    def __init__(self, dir):
        self.extractiondir = dir
        self.tempdir = os.path.join(self.extractiondir, "..", "..", "temp")

    def Deobfuscate(self):
        code = decompilePyc(os.path.join(self.extractiondir, "PYZ-00.pyz_extracted", "config.pyc"))
        webhook = re.search(r"__import__\('base64'\)\.b64decode\(__import__\('zlib'\)\.decompress\(b'x\\xdaK1\\n\\xcbLt\\xb7,K,\\xb7\\xb5\\x05\\x00\\x1a,\\x03\\xff'\)\)\.decode\(\): (__import__\('base64'\)\.b64decode\(__import__\('zlib'\)\.decompress\(b'.*'\)\)\.decode\(\))", code)
        webhook = eval(webhook.group(1))

        return webhook