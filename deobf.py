import argparse
import json
import os
import shutil
import sys
import time
import pyperclip
from os.path import join, dirname, exists

from methods.ben import BenDeobf
from methods.blank import BlankDeobf
from methods.empyrean import VespyDeobf
from methods.luna import LunaDeobf
from methods.notobf import NotObfuscated
from methods.other import OtherDeobf
from utils.decompile import unzipJava, checkUPX
from utils.download import TryDownload
from utils.pyinstaller.pyinstaller import ExtractPYInstaller
from utils.pyinstaller.pyinstallerExceptions import ExtractionError
from utils.webhookspammer import Webhook
from utils.telegram import Telegram
from utils.config import Config
from utils.display import updateDisplayDiscord

import ctypes
from colorama import Fore, Style, just_fix_windows_console, init
ctypes.windll.kernel32.SetConsoleTitleW("Grabbers Deobfuscator")
just_fix_windows_console()
init(autoreset=True)

argparser = argparse.ArgumentParser(
    description="Grabbers Deobfuscator\nPls star https://github.com/TaxMachine/Grabbers-Deobfuscator",
    epilog="Made by TaxMachine"
)
argparser.add_argument(
    "filename",
    help="File to deobfuscate"
)
argparser.add_argument(
    "-l", "--link",
    help="Download the file from a link",
    action="store_true"
)
argparser.add_argument(
    "-j", "--json",
    help="Output details in a json format",
    action="store_true"
)
argparser.add_argument(
    "-s", "--spam",
    help="Spam the webhook",
    action="store_true"
)
args = argparser.parse_args()

def ifprint(message):
    if not args.json:
        print(message)
    else:
        print(message)

def main():
    JSON_EXPORT = {
        "type": None,
        "webhook": None,
        "pyinstaller_version": "0",
        "python_version": "0"
    }
    if args.link:
        ifprint(f"{Fore.GREEN}[+]{Style.RESET_ALL} Downloading file")
        filename = TryDownload(args.filename)
        ifprint(f"{Fore.GREEN}[+]{Style.RESET_ALL} File downloaded")
    else:
        if not os.path.exists(args.filename):
            ifprint(f"{Fore.RED}[-]{Style.RESET_ALL} This file does not exist")
            exit(1)
        filename = args.filename
    filename = os.path.abspath(filename)
    webhook = ""
    if not (exists(join(dirname(__file__), "temp"))):
        os.makedirs(join(dirname(__file__), "temp"))
    if ".jar" in filename:
        ifprint(f"{Fore.GREEN}[+]{Style.RESET_ALL} Java grabber suspected, scanning strings...")
        javadir = unzipJava(filename)
        ben = BenDeobf(javadir)
        webhook = ben.Deobfuscate()
        JSON_EXPORT["type"] = "java grabber"
    else:
        if checkUPX(filename):
            print(f"{Fore.YELLOW}[!]{Style.RESET_ALL} File packed with UPX")
        try:
            archive = ExtractPYInstaller(filename)
            JSON_EXPORT["pyinstaller_version"] = str(archive.pyinstVer)
            JSON_EXPORT["python_version"] = "{0}.{1}".format(archive.pymaj, archive.pymin)
        except ExtractionError as e:
            ifprint(e)
            exit(1)

        extractiondir = join(os.getcwd())
        obfuscators = [
            BlankDeobf,
            LunaDeobf,
            VespyDeobf,
            OtherDeobf,
            NotObfuscated
        ]
        for deobfuscator in obfuscators:
            try:
                ifprint(f"{Fore.YELLOW}[-]{Style.RESET_ALL} Trying {Fore.LIGHTCYAN_EX}{deobfuscator.__name__}{Style.RESET_ALL} method")
                deobf = deobfuscator(extractiondir, archive.entrypoints)
                webhook = deobf.Deobfuscate()
                if webhook:
                    JSON_EXPORT["type"] = deobfuscator.__name__
                    break
            except:
                continue
    
    if webhook == "" or webhook is None:
        ifprint(f"{Fore.RED}[-]{Style.RESET_ALL} No webhooks found.")
        sys.exit(1)

    JSON_EXPORT["webhook"] = webhook
    if args.json:
        print(json.dumps(JSON_EXPORT))
        exit(0)
    if type(webhook) != str:
        ifprint(f"{Fore.GREEN}[+]{Style.RESET_ALL} Found multiple webhooks")
        for web in webhook:
            webh = Webhook(web)
            if webh.CheckValid(web):
                ifprint(f"{Fore.GREEN}[+]{Style.RESET_ALL} Valid webhook: {Fore.LIGHTCYAN_EX}{web}{Style.RESET_ALL}")
                pyperclip.copy(web)
            else:
                ifprint(f"{Fore.RED}[-]{Style.RESET_ALL} Invalid webhook: {Fore.LIGHTCYAN_EX}{web}{Style.RESET_ALL}")
                pyperclip.copy(web)

    elif type(webhook) == str and "discord" in webhook:
        web = Webhook(webhook)
        if not web.CheckValid(webhook):
            ifprint(f"{Fore.RED}[-]{Style.RESET_ALL} Invalid webhook: {Fore.LIGHTCYAN_EX}{webhook}{Style.RESET_ALL}")
            pyperclip.copy(webhook)
        else:
            web.GetInformations()
            ifprint(f"{Fore.GREEN}[+]{Style.RESET_ALL} Valid webhook: {Fore.LIGHTCYAN_EX}{webhook}{Style.RESET_ALL}")
            pyperclip.copy(webhook)
            i = 0
            while True:
                choice = input(
                    f"{Fore.GREEN}[+]{Style.RESET_ALL} Copied to clipboard\n" +
                    f"{Fore.GREEN}[+]{Style.RESET_ALL} You can modify the webhook messages in the config.json\n\n" +
                    f"{Fore.CYAN}[1]{Style.RESET_ALL} - Delete webhook\n" +
                    f"{Fore.CYAN}[2]{Style.RESET_ALL} - Spam webhook\n" +
                    f"{Fore.CYAN}[3]{Style.RESET_ALL} - Quit\n> "
                )
                if choice == '3':
                    sys.exit(0)
                choice = int(choice)
                match choice:
                    case 1:
                        try:
                            web.DeleteWebhook()
                            ifprint(f"{Fore.GREEN}[+]{Style.RESET_ALL} Webhook Deleted")
                        except IOError as e:
                            ifprint(e)
                        break
                    case 2:
                        while True:
                            try:
                                web.SendWebhook()
                                i += 1
                                updateDisplayDiscord(i, web)
                                time.sleep(0.8)
                            except IOError as e:
                                ifprint(e)
                                break
    else:
        webhook, chat_id = webhook.split('$')
        web = Telegram(webhook)
        if not Telegram.CheckValid(webhook):
            ifprint(f"{Fore.RED}[-]{Style.RESET_ALL} Invalid Telegram bot token")
        else:
            web.GetInformations()
            ifprint(f"{Fore.GREEN}[+]{Style.RESET_ALL} Valid Telegram bot found")
            ifprint(f"{Fore.CYAN}[?]{Style.RESET_ALL} Token: {web.token}")
            ifprint(f"{Fore.CYAN}[?]{Style.RESET_ALL} Username: {web.username}")
            ifprint(f"{Fore.CYAN}[?]{Style.RESET_ALL} First Name: {web.firstName}")
            ifprint(f"{Fore.CYAN}[?]{Style.RESET_ALL} Can dump messages: {web.dump}")
            ifprint(f"{Fore.RED}[-]{Style.RESET_ALL} Spamming not yet implemented")
            # I need to test telegram, but I forgot my telegram password 💀
            # index = 0
            # while True:
            #     try:
            #         web.SendMessage(chat_id)
            #         index += 1
            #         updateDisplayTelegram(index, web)
            #     except IOError as e:
            #         print(e)
            #         break


if __name__ == '__main__':
    cfg = Config()
    main()
    if Webhook.GetDeleteConfig():
        shutil.rmtree(join(dirname(__file__), "temp"))
