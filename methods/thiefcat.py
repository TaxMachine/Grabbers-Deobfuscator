# Thank you to meisr cuz yes
import re, base64, subprocess, marshal, datetime, zlib, sys, dis, bz2, lzma, gzip, binascii
from os import path, walk
from os.path import join
from utils.decompile import decompilePyc, disassemblePyc
from utils.deobfuscation import BlankOBF

class TheifcatDeobf:
    def __init__(self, dir):
        self.extractiondir = dir
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
    
    def DetectCompression(self, bytecode):
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

    def Deobfuscate(self):
        entrypoint = ""
        for root, subdirs, files in walk(self.extractiondir):
            for file in files:
                if file.endswith(".pyc"):
                    path = join(root, file)
                    strings = subprocess.run(["strings", path], stdout=subprocess.PIPE).stdout.decode()
                    if "CryptUnprotectData" in strings:
                        entrypoint = path
        code = decompilePyc(entrypoint)
        bytestr = re.search(r"exec\(marshal.loads\(binascii.a2b_base64\(b'(.*)'\)\)\)", code)
        b64 = bytestr.group(1).encode().decode("unicode_escape", "ignore").encode("iso-8859-1")
        decoded = base64.b64decode(b64)
        serialized = marshal.loads(decoded)

        bytecode = dis.Bytecode(serialized).dis()
        
        for i in range(4, 202):
            bytecode = self.DecompressBytecodeX(bytecode)
            
        webhook = BlankOBF.MatchWebhook(bytecode)
        return webhook