import base64, os, subprocess, zlib, zipfile, re, lzma, codecs, base64
from utils.pyaes import AESModeOfOperationGCM
from utils.decompile import decompilePyc, disassemblePyc

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

    def deobfStage4(self, firstpart, secondpart, thirdpart, fourthpart):
        pythonbytes = base64.b64decode(codecs.decode(firstpart, "rot13")+secondpart+thirdpart[::-1]+fourthpart)
        with open(os.path.join(self.tempdir, "stage5.pyc"), "wb") as f:
            f.write(pythonbytes)

    def Deobfuscate(self):
        try:
            authtags = BlankDeobf.getKeysFromPycFile(self, os.path.join(self.extractiondir, "loader-o.pyc"))
            print("payload key: " + str(authtags.key))
            print("payload iv: " + str(authtags.iv))
            if len(authtags.key) != 32: print("Key length is invalid")
            if len(authtags.iv) != 12: print("IV length is invalid")


            encryptedfile = open(os.path.join(self.extractiondir, "blank.aes"), "rb").read()
            print("compressed not reversed: " + str(encryptedfile[:6]))


            reversed = encryptedfile[::-1]
            print("compressed reversed: " + str(reversed[:6]))


            decompressed = zlib.decompress(reversed)
            print("decompressed: " + str(decompressed[:6]))


            decryptedfile = AESModeOfOperationGCM(authtags.key, authtags.iv).decrypt(decompressed)
            print("decrypted: " + str(decryptedfile[:6]))

            with open('decrypted.zip', 'wb') as f:
                f.write(decryptedfile)
            with zipfile.ZipFile("decrypted.zip", "r") as zip:
                zip.extractall()
        except ValueError as e:
            print(e)
        except zipfile.BadZipFile as e:
            print(e)

        assembly = disassemblePyc(os.path.join(self.extractiondir, "stub-o.pyc"))
        
        # very shitty workaround dont mind me
        bytestr = re.search(r"b'(\\xfd7zXZ\\x00\\x00.*?YZ)'", assembly).group(1)
        with open(os.path.join(self.tempdir, "shittyworkaround.py"), "w") as f:
            f.write(f"stage3 = b'{bytestr}'")

        try:
            from temp.shittyworkaround import stage3
            decompressed = lzma.decompress(stage3)
            sanitized = decompressed.decode().replace(";", "\n")
            sanitized = re.sub(r"^__import__.*", "", sanitized, flags=re.M)
            with open(os.path.join(self.tempdir, "stage4.py"), "w") as f:
                f.write(sanitized)
        except ImportError as e:
            print(e)
            exit(0)
        
        try:
            from temp.stage4 import ____ as firstpart, _____ as secondpart, ______ as thirdpart, _______ as fourthpart
            BlankDeobf.deobfStage4(self, firstpart, secondpart, thirdpart, fourthpart)
        except ImportError as e:
            print(e)
            exit(0)

        strings = subprocess.run(["strings", os.path.join(self.tempdir, "stage5.pyc")], stdout=subprocess.PIPE, stderr=None).stdout.decode()
        webhook = re.search(r"(aHR0cHM6Ly9kaXNjb3JkLmNvbS9hcGkvd2ViaG9va3Mv.*==)", strings).group(1)
        decodedwebhook = base64.b64decode(webhook)
        return decodedwebhook.decode()