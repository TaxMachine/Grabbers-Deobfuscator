import base64, os, zlib, zipfile, re, base64, io, dis
import marshal

from utils.pyaes import AESModeOfOperationGCM
from utils.decompile import decompilePyc, disassemblePyc
from utils.deobfuscation import BlankOBF


class AuthTag:
    def __init__(self, key, iv):
        self.key = key
        self.iv = iv


class BlankDeobf:
    def __init__(self, blankdir):
        self.extractiondir = blankdir
        self.tempdir = os.path.join(self.extractiondir, "..", "..", "temp")

    @staticmethod
    def getKeysFromPycFile(filename):
        f = open(filename, "rb")
        data = f.read()
        f.close()
        data = data.split(b"stub-oz,")[-1].split(b"\x63\x03")[0].split(b"\x10")
        key = base64.b64decode(data[0].split(b"\xDA")[0].decode())
        iv = base64.b64decode(data[-1].decode())
        return AuthTag(
            key,
            iv
        )

    def Deobfuscate(self):
        filename = None
        try:
            if os.path.exists(os.path.join(self.extractiondir, "loader-o.pyc")):
                filename = "loader-o.pyc"
            else:
                for files in os.listdir(self.extractiondir):
                    if re.match(r"([a-f0-9]{8}-[a-f0-9]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[a-f0-9]{12}\.pyc)", files):
                        filename = files
                    if filename:
                        break
            authtags = BlankDeobf.getKeysFromPycFile(os.path.join(self.extractiondir, filename))
            print("payload key: " + str(authtags.key))
            print("payload iv: " + str(authtags.iv))
            if len(authtags.key) != 32:
                raise ValueError("Key length is invalid")
            if len(authtags.iv) != 12:
                raise ValueError("IV length is invalid")

            encryptedfile = open(os.path.join(self.extractiondir, "blank.aes"), "rb").read()
            try:
                reversedstr = encryptedfile[::-1]
                encryptedfile = zlib.decompress(reversedstr)
            except zlib.error:
                pass
            decryptedfile = AESModeOfOperationGCM(authtags.key, authtags.iv).decrypt(encryptedfile)
            with zipfile.ZipFile(io.BytesIO(decryptedfile)) as aeszipe:
                aeszipe.extractall()
        except ValueError as e:
            print(e)
        except zipfile.BadZipFile as e:
            print(e)

        file = open(os.path.join(self.extractiondir, "stub-o.pyc"), "rb")
        assembly = file.read()
        file.close()
        stage3 = BlankOBF.DeobfuscateStage3(assembly)
        webhook = BlankOBF.DeobfuscateStage4(stage3.first, stage3.second, stage3.third, stage3.fourth)
        return webhook
