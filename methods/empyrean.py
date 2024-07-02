import os, sys, importlib.util
from colorama import Fore, Style, just_fix_windows_console, init
just_fix_windows_console()
init(autoreset=True)

class VespyDeobf:
    def __init__(self, dir, entries):
        self.extractiondir = dir
        self.entries = entries
        self.tempdir = os.path.join(self.extractiondir, "..", "..", "temp")

    def Deobfuscate(self):
        config_file = os.path.join(self.extractiondir, "PYZ-00.pyz_extracted", "config.pyc")
        if not os.path.exists(config_file):
            raise Exception()

        if input(
            f"{Fore.RED}[!]{Style.RESET_ALL} This method will execute the code found in the {Fore.LIGHTCYAN_EX}config.pyc{Style.RESET_ALL} to bypass the obfuscation.\n" +
            f"{Fore.RED}[!]{Style.RESET_ALL} Make sure to run this in a virtual machine or a container in case there is malicious code.\n" +
            f"{Fore.RED}[!]{Style.RESET_ALL} Do you want to proceed running the code? (y/n): "
        ).lower() != "y":
            raise Exception()
        
        spec = importlib.util.spec_from_file_location("config", config_file)
        module = importlib.util.module_from_spec(spec)

        sys.modules["config"] = module
        spec.loader.exec_module(module)

        return module.__CONFIG__["webhook"]