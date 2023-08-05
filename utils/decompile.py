import subprocess, sys, zipfile
from os import path, makedirs

PYCDC = "pycdc.exe" if sys.platform == 'nt' else "pycdc"
PYCDAS = "pycdas.exe" if sys.platform == 'nt' else "pycdas"

dir = path.join(path.dirname(__file__))

def decompilePyc(filename):
    res = subprocess.run([path.join(dir, "bin", PYCDC), filename], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    return res.stdout.decode()

def disassemblePyc(filename):
    res = subprocess.run([path.join(dir, "bin", PYCDAS), filename], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    return res.stdout.decode()

def unzipJava(filename):
    if not filename.endswith(".jar"):
        raise ValueError("Not a jar file")
    outdir = path.join(dir, "..", "temp", filename.split(path.sep)[len(filename.split(path.sep)) - 1].split(".")[0])
    if not path.exists(outdir): makedirs(outdir)
    with zipfile.ZipFile(filename) as f:
        f.extractall(outdir)
    return outdir
