import sys, os, requests
from utils.pyinxtractor import PyInstArchive

from methods.blank import BlankDeobf

def validate_webhook(webhook):
    return requests.get(webhook)

def main():
    if len(sys.argv) < 2:
        print("usage: deobf.py [file.exe]")
        exit(0)
    if not (os.path.exists("temp")): os.mkdir("temp")
    arch = PyInstArchive(sys.argv[1])
    if arch.open():
        if arch.checkFile():
            if arch.getCArchiveInfo():
                arch.parseTOC()
                arch.extractFiles()
                arch.close()
                print('[+] Successfully extracted pyinstaller archive: {0}'.format(sys.argv[1]))
        else:
            arch.close()
            exit(0)
    extractiondir = os.path.join(os.getcwd())
    if (os.path.join(extractiondir, "blank.aes")):
        print("[+] Blank Stealer detected")
        blank = BlankDeobf(extractiondir)
        webhook = blank.Deobfuscate()
        res = validate_webhook(webhook)
        if res.status_code != 200:
            print("[-] Invalid webhook: " + webhook)
        else:
            print("[+] Valid webhook: " + webhook)
            print("Author: " + res.json()["user"]["username"])
            print("Author ID: " + res.json()["user"]["id"])

if __name__ == '__main__':
    main()