import subprocess, os, sys

PYCDC = "pycdc.exe" if sys.platform == 'nt' else "pycdc"
PYCDAS = "pycdas.exe" if sys.platform == 'nt' else "pycdas"

def decompilePyc(filename):
    res = subprocess.run([os.path.join(os.getcwd(), "..", "..", "utils", PYCDC), filename], stdout=subprocess.PIPE, stderr=None)
    return res.stdout.decode()

def disassemblePyc(filename):
    res = subprocess.run([os.path.join(os.getcwd(), "..", "..", "utils", PYCDAS), filename], stdout=subprocess.PIPE, stderr=None)
    return res.stdout.decode()