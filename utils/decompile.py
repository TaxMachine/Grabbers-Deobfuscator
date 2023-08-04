import subprocess, sys
from os import path

PYCDC = "pycdc.exe" if sys.platform == 'nt' else "pycdc"
PYCDAS = "pycdas.exe" if sys.platform == 'nt' else "pycdas"

def decompilePyc(filename):
    res = subprocess.run([path.join(path.dirname(__file__), "bin", PYCDC), filename], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    return res.stdout.decode()

def disassemblePyc(filename):
    res = subprocess.run([path.join(path.dirname(__file__), "bin", PYCDAS), filename], stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    return res.stdout.decode()