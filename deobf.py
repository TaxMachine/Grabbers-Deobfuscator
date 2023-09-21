import argparse
import os
import shutil
import sys
import time
from os.path import join, dirname, exists

from methods.ben import BenDeobf
from methods.blank import BlankDeobf
from methods.empyrean import VespyDeobf
from methods.luna import LunaDeobf
from methods.notobf import NotObfuscated
from methods.thiefcat import TheifcatDeobf
from utils.decompile import unzipJava
from utils.detection import Detection
from utils.download import TryDownload
from utils.pyinstxtractor import PyInstArchive
from utils.pyinstxtractorng import PyInstArchive as PyInstArchiveNG
from utils.webhookspammer import Webhook


def updateDisplay(index: int, username: str, userid: str, name: str):
    os.system('clear' if sys.platform == 'nt' else 'cls')
    print(f"""
  +--------------------------------------------------+
    Author name -> {username}
    Author ID -> {userid}
    Webhook name -> {name}
  +--------------------------------------------------+
    Spammed
    +------+
     {index}
    +------+
""")


def main():
    argparser = argparse.ArgumentParser(
        description="Grabbers Deobfuscator\nPls star https://github.com/TaxMachine/Grabbers-Deobfuscator", 
        epilog="Made by TaxMachine"
    )
    argparser.add_argument(
        "filename", 
        help="File to deobfuscate"
    )
    argparser.add_argument(
        "-d", "--download", 
        help="Download the file from a link", 
        action="store_true"
    )
    args = argparser.parse_args()
    if args.download:
        print("[+] Downloading file")
        filename = TryDownload(args.filename)
        print("[+] File downloaded")
    else:
        filename = args.filename
    filename = os.path.abspath(filename)
    webhook = ""
    if not (exists(join(dirname(__file__), "temp"))):
        os.makedirs(join(dirname(__file__), "temp"))
    if ".jar" in filename:
        if Detection.BenGrabberDetect(filename):
            print("[+] Ben grabber detected")
            javadir = unzipJava(filename)
            ben = BenDeobf(javadir)
            webhook = ben.Deobfuscate()
    else:
        arch = None
        try:
            arch = PyInstArchive(filename)
            if arch.open() and arch.checkFile() and arch.getCArchiveInfo():
                arch.parseTOC()
                arch.extractFiles()
                print('[+] Successfully extracted pyinstaller archive: {0}'.format(filename))
        except Exception:
            arch = PyInstArchiveNG(filename)
            if arch.open() and arch.checkFile() and arch.getCArchiveInfo():
                arch.parseTOC()
                arch.extractFiles()
                print(f"[+] Successfully extracted pyinstaller archive: {filename}")
        entries = arch.entrypoints
        arch.close()
        extractiondir = join(os.getcwd())
        if Detection.BlankGrabberDetect(filename):
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
        elif Detection.ThiefcatDetect(extractiondir):
            print("[+] Thiefcat Stealer Detected")
            cat = TheifcatDeobf(extractiondir, entries)
            webhook = cat.Deobfuscate()
        else:
            print("[-] Obfuscation/Stealer not detected. Strings method will be used instead")
            notobf = NotObfuscated(extractiondir)
            webhook = notobf.GetWebhook()
    
    if webhook == "" or webhook is None:
        print("No webhook found.")
        sys.exit(0)

    web = Webhook(webhook)
    if not web.CheckValid(webhook):
        print(f"[-] Invalid webhook: {webhook}")
    else:
        web.GetInformations()
        print(f"[+] Valid webhook: {webhook}")
        print(f"Author: {web.author}")
        print(f"Author ID: {web.author_id}")
        i = 0
        while True:
            choice = input(
                "(You can modify the webhook messages in the config.json)\n[1] - Delete webhook\n[2] - "
                "Spam webhook\nquit - to leave\n-> "
            )
            if choice == 'quit':
                sys.exit(0)
            choice = int(choice)
            match choice:
                case 1:
                    try:
                        web.DeleteWebhook()
                        print("[+] Webhook Deleted")
                    except IOError as e:
                        print(e)
                    break
                case 2:
                    while True:
                        try:
                            web.SendWebhook()
                            i += 1
                            updateDisplay(i, web.author, web.author_id, web.name)
                            time.sleep(0.8)
                        except IOError as e:
                            print(e)
                            break


if __name__ == '__main__':
    main()
    if Webhook.GetDeleteConfig():
        shutil.rmtree(join(dirname(__file__), "temp"))
