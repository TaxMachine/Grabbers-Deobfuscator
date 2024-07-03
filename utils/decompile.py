import subprocess, sys, zipfile, re
from os import path, makedirs
from colorama import Fore, Style, just_fix_windows_console, init
just_fix_windows_console()
init(autoreset=True)

PYCDC = "pycdc.exe" if sys.platform == 'win32' else "pycdc"
PYCDAS = "pycdas.exe" if sys.platform == 'win32' else "pycdas"
UPX = "upx.exe" if sys.platform == 'win32' else "upx"

dir = path.join(path.dirname(__file__))

def checkUPX(filename):
    res = subprocess.run([path.join(dir, "bin", UPX), "-l", filename], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if "not packed" not in res.stderr.decode():
        res = subprocess.run([path.join(dir, "bin", UPX), "-d", filename], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
        if "Unpacked" in res.stdout.decode():
            return True
        else:
            print(f"{Fore.RED}[!]{Style.RESET_ALL} UPX was detected but failed to decompress.")
    return False

def decompilePyc(filename):
    res = subprocess.run([path.join(dir, "bin", PYCDC), filename], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    return res.stdout.decode()

def disassemblePyc(filename):
    res = subprocess.run([path.join(dir, "bin", PYCDAS), filename], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    return res.stdout.decode()

def unzipJava(filename):
    if ".jar" not in filename:
        raise ValueError("Not a jar file")
    outdir = path.join(dir, "..", "temp", filename.split(path.sep)[len(filename.split(path.sep)) - 1].split(".")[0])
    if not path.exists(outdir):
        makedirs(outdir)
    with zipfile.ZipFile(filename) as f:
        f.extractall(outdir)
    return outdir

def strings(bytestring):
    matches = re.findall(r"([^\0]+)\0", bytestring.decode(errors="ignore"))
    if matches:
        return "".join(matches)
    else: return ""