import os, sys, importlib.util

class VespyDeobf:
    def __init__(self, dir):
        self.extractiondir = dir
        self.tempdir = os.path.join(self.extractiondir, "..", "..", "temp")

    def Deobfuscate(self):
        config_file = os.path.join(self.extractiondir, "PYZ-00.pyz_extracted", "config.pyc")

        if input("This method will execute the code found in the config.pyc to bypass the obfuscation. Make sure to run this in a virtual machine or a container in case there is malicious code, do you want to run the code (y/n)?: ").lower() != "y":
            return ""
        
        spec = importlib.util.spec_from_file_location("config", config_file)
        module = importlib.util.module_from_spec(spec)

        sys.modules["config"] = module
        spec.loader.exec_module(module)

        return module.__CONFIG__["webhook"]
