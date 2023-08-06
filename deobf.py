import sys, os, time
from utils.pyinxtractor import PyInstArchive

from utils.webhookspammer import Webhook

from methods.blank import BlankDeobf
from methods.empyrean import VespyDeobf
from methods.luna import LunaDeobf
from methods.thiefcat import TheifcatDeobf
from methods.notobf import NotObfuscated

from methods.ben import BenDeobf

from utils.detection import Detection
from utils.decompile import unzipJava

from os.path import join, dirname, exists

def updateDisplay(index, username, id, name):
    os.system('cls' if sys.platform == 'nt' else 'clear')
    print(f"""
  +--------------------------------------------------+
    Author name -> {username}
    Author ID -> {id}
    Webhook name -> {name}
  +--------------------------------------------------+
    Spammed
    +------+
     {index}
    +------+
""")

def main():
    if len(sys.argv) < 2:
        print("usage: deobf.py [file.exe]")
        exit(0)
    webhook = ""
    if not (exists(join(dirname(__file__), "temp"))): os.makedirs(join(dirname(__file__), "temp"))
    if sys.argv[1].endswith(".jar"):
        dir = unzipJava(sys.argv[1])
        if Detection.BenGrabberDetect(dir):
            print("[+] Ben grabber detected")
            ben = BenDeobf(dir)
            webhook = ben.Deobfuscate()
    else:
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
        elif Detection.ThiefcatDetect(extractiondir):
            print("[+] Thiefcat Stealer Detected")
            cat = TheifcatDeobf(extractiondir)
            webhook = cat.Deobfuscate()
        else:
            print("[-] Obfuscation/Stealer not detected. Strings method will be used instead")
            notobf = NotObfuscated(extractiondir)
            webhook = notobf.GetWebhook()
    
    if webhook == "" or webhook == None:
        print("No webhook found.")
        exit(0)

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
            choice = input("(You can modify the webhook messages in the config.json)\n[1] - Delete webhook\n[2] - Spam webhook\nquit - to leave\n-> ")
            if choice == 'quit':
                exit(0)
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
            break


if __name__ == '__main__':
    main()