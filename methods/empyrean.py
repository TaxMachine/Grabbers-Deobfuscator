import os, re, zlib, base64

from utils.decompile import decompilePyc, strings
from utils.deobfuscation import MatchWebhook


class VespyDeobf:
    def __init__(self, dir):
        self.extractiondir = dir
        self.tempdir = os.path.join(self.extractiondir, "..", "..", "temp")

    def Deobfuscate(self):
        code = decompilePyc(os.path.join(self.extractiondir, "PYZ-00.pyz_extracted", "config.pyc"))
        webhook = re.search(r"__import__\('base64'\)\.b64decode\(__import__\('zlib'\)\.decompress\(b'x\\xdaK1\\n\\xcbLt\\xb7,K,\\xb7\\xb5\\x05\\x00\\x1a,\\x03\\xff'\)\)\.decode\(\): __import__\('base64'\)\.b64decode\(__import__\('zlib'\)\.decompress\(b'(.*)'\)\)\.decode\(\)", code)
        if webhook is None or webhook == "":
            f = open(os.path.join(self.extractiondir, "PYZ-00.pyz_extracted", "config.pyc"), "rb")
            webhook = strings(f.read())
            f.close()
            webhook = MatchWebhook(webhook)
        else:
            webhook = webhook.group(1).encode().decode("unicode_escape", "ignore").encode("iso-8859-1")
            webhook = base64.b64decode(zlib.decompress(webhook)).decode()
        return webhook
