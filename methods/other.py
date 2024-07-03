# Thank you to meisr cuz yes
import re, base64, marshal, zlib, dis, bz2, lzma, gzip
from os import path
from utils.decompile import disassemblePyc
from utils.deobfuscation import MatchWebhook
from cryptography.fernet import Fernet

class OtherDeobf:
    def __init__(self, dir, entries):
        self.extractiondir = dir
        self.entries = entries
        self.tempdir = path.join(self.extractiondir, "..", "..", "temp")

    def DecompressBytecodeX(self, bytecode):
        if re.search(r"72 LOAD_ATTR                [0-9]{1,2} \(a2b_base64\)", bytecode):
            encoded = re.search(r"\(b'(.*)'\)", bytecode).group(1)
            if encoded.endswith("\\n"): encoded = encoded[:-2]
            decoded = base64.b64decode(encoded)
            newserialized = marshal.loads(decoded)
            bytecodenext = dis.Bytecode(newserialized).dis()
        else:
            compression = self.DetectCompression(bytecode)
            compressed = re.search(r"\(b'(.*)'\)", bytecode).group(1)
            formatedcompressed = compressed.encode().decode("unicode_escape", "ignore").encode("iso-8859-1")
            decompressed = compression.decompress(formatedcompressed)
            serialized = marshal.loads(decompressed)
            bytecodenext = dis.Bytecode(serialized).dis()
        return bytecodenext

    @staticmethod
    def DetectCompression(bytecode):
        match = re.search(r"70 LOAD_NAME                [0-9]{1,2} \((.*)\)", bytecode)
        res = match.group(1)
        match res:
            case "lzma":
                return lzma
            case "gzip":
                return gzip
            case "bz2":
                return bz2
            case "zlib":
                return zlib
    
    @staticmethod
    def DeobfuscateVare(bytecode):
        pattern = r"""        [0-9]{1,4}    LOAD_CONST                      [0-9]{1,4}: '(.*)'\r
        [0-9]{1,4}    STORE_NAME                      [0-9]{1,4}: [\d\w]+\r
        [0-9]{1,4}    BUILD_LIST                      [0-9]{1,4}\r
        [0-9]{1,4}    LOAD_CONST                      [0-9]{1,4}: \('(.*)', '(.*)', '(.*)'\)"""

        matches = re.search(pattern, bytecode, re.MULTILINE)
        key = matches.group(1)
        first = matches.group(2)
        second = matches.group(3)
        third = matches.group(4)

        def decodearr(arr):
            arr = arr[::-1]
            result = []
            for i in arr.split("|"):
                result.append(chr(int(i)))
            return ''.join(result)

        f = Fernet(key)

        first = decodearr(first)
        second = decodearr(second)
        third = decodearr(third)

        decrypted = f.decrypt(bytes.fromhex(first + third + second))
        decoded = base64.b64decode(decrypted)
        decompressed = zlib.decompress(decoded)
        return decompressed.decode(errors='ignore')

    def Deobfuscate(self):
        entrypoint = None
        for i in self.entries:
            if 'pyi' not in i:
                entrypoint = i
        code = disassemblePyc(entrypoint)
        if entrypoint == "Obfuscated.pyc":
            content = self.DeobfuscateVare(code)
            webhook = MatchWebhook(content)
            return webhook
        bytestr = re.search(r"exec\(marshal.loads\(binascii.a2b_base64\(b'(.*)'\)\)\)", code)
        if bytestr is None:
            webhook = MatchWebhook(code)
            return webhook
        b64 = bytestr.group(1).encode().decode("unicode_escape", "ignore").encode("iso-8859-1")
        decoded = base64.b64decode(b64)
        serialized = marshal.loads(decoded)

        bytecode = dis.Bytecode(serialized).dis()
        
        while True:
            try:
                bytecode = self.DecompressBytecodeX(bytecode)
                webhook = MatchWebhook(bytecode)
                if webhook:
                    return webhook
            except Exception:
                pass