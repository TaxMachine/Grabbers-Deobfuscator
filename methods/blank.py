import base64, os, subprocess, zlib, zipfile, re, lzma, codecs, base64, io
from utils.pyaes import AESModeOfOperationGCM
from utils.decompile import decompilePyc, disassemblePyc
from utils.deobfuscation import BlankOBF

class AuthTag:
    def __init__(self, key, iv):
        self.key = key
        self.iv = iv

class BlankDeobf:
    def __init__(self, dir):
        self.extractiondir = dir
        self.tempdir = os.path.join(self.extractiondir, "..", "..", "temp")

    def getKeysFromPycFile(self, filename):
        code = decompilePyc(filename)
        key = re.search(r"key = base64\.b64decode\('(.*?)'", code).group(1)
        iv = re.search(r"iv = base64\.b64decode\('(.*?)'", code).group(1)
        return AuthTag(
            base64.b64decode(key.encode()),
            base64.b64decode(iv.encode())
        )

    def Deobfuscate(self):
        try:
            authtags = BlankDeobf.getKeysFromPycFile(self, os.path.join(self.extractiondir, "loader-o.pyc"))
            print("payload key: " + str(authtags.key))
            print("payload iv: " + str(authtags.iv))
            if len(authtags.key) != 32: print("Key length is invalid")
            if len(authtags.iv) != 12: print("IV length is invalid")

            encryptedfile = open(os.path.join(self.extractiondir, "blank.aes"), "rb").read()
            reversed = encryptedfile[::-1]
            decompressed = zlib.decompress(reversed)
            decryptedfile = AESModeOfOperationGCM(authtags.key, authtags.iv).decrypt(decompressed)
            with zipfile.ZipFile(io.BytesIO(decryptedfile)) as zip:
                zip.extractall()
        except ValueError as e:
            print(e)
        except zipfile.BadZipFile as e:
            print(e)

        assembly = disassemblePyc(os.path.join(self.extractiondir, "stub-o.pyc"))
        stage3 = BlankOBF.DeobfuscateStage3(assembly)
        webhook = BlankOBF.DeobfuscateStage4(stage3.first, stage3.second, stage3.third, stage3.fourth)
        return webhook