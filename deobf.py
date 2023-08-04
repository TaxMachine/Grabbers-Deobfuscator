import sys, os, requests
from utils.pyinxtractor import PyInstArchive

from methods.blank import BlankDeobf
from methods.empyrean import VespyDeobf
from methods.luna import LunaDeobf
from methods.notobf import NotObfuscated

from utils.detection import Detection

from os.path import join, dirname, exists

def validate_webhook(webhook):
    return requests.get(webhook)

def main():
    if len(sys.argv) < 2:
        print("usage: deobf.py [file.exe]")
        exit(0)
    if not (exists(join(dirname(__file__), "temp"))): os.mkdir(join(dirname(__file__), "temp"))
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
    extractiondir = join(os.getcwd())
    webhook = ""
    if Detection.BlankGrabberDetect(extractiondir):
        print("[+] Blank Stealer detected")
        blank = BlankDeobf(extractiondir)
        webhook = blank.Deobfuscate()
    elif Detection.EmpyreanDetect(extractiondir):
        print("[+] Empyrean/Vespy Grabber detected")
        vespy = VespyDeobf(extractiondir)
        webhook = vespy.Deobfuscate()
    elif Detection.BlankObfDetect(extractiondir):
        print("[+] Blank Obfuscation detected: possibly luna grabber")
        luna = LunaDeobf(extractiondir)
        webhook = luna.Deobfuscate()
    else:
        print("[-] Obfuscation/Stealer not detected. Strings method will be used instead")
        notobf = NotObfuscated(extractiondir)
        webhook = notobf.GetWebhook()
    
    if webhook == "" or webhook == None:
        print("No webhook found.")
        exit(0)

    res = validate_webhook(webhook)
    if res.status_code != 200:
        print("[-] Invalid webhook: " + webhook)
    else:
        print("[+] Valid webhook: " + webhook)
        print("Author: " + res.json()["user"]["username"])
        print("Author ID: " + res.json()["user"]["id"])

if __name__ == '__main__':
    main()