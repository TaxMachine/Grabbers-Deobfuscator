import re
from os.path import exists, join, sep
from utils.decompile import disassemblePyc


class Detection:
    def BlankObfDetect(dir):
        try:
            ## Very shitty but it works ig
            file = dir.split(".exe")[0].split(sep)[len(dir.split(sep)) - 1] + ".pyc"
            assembly = disassemblePyc(dir + sep + file)
            keywordstuffidk = [
                "'eval'",
                "'getattr'",
                "'__import__'",
                "'bytes'",
                "'decode'",
                "'__________'",
                "'___________'",
                "'_______________'",
                "'________________'",
                "'____________'",
                "'________'",
                "'_________'"
            ]
            found = True
            for i in keywordstuffidk:
                if i not in assembly:
                    found = False
            if found:
                return True
        except Exception:
            pass
        return False
            
    def BlankGrabberDetect(dir):
        return exists(join(dir, "loader-o.pyc"))
    
    def EmpyreanDetect(dir):
        return exists(join(dir, "PYZ-00.pyz_extracted", "config.pyc"))
    
    def BenGrabberDetect(dir):
        return exists(join(dir, "net", "jodah", "typetools"))
    
    def ThiefcatDetect(dir):
        return exists(join(dir, "PYZ-00.pyz_extracted", "configparser.pyc")) and exists(join(dir, "PYZ-00.pyz_extracted", "gzip.pyc")) and exists(join(dir, "PYZ-00.pyz_extracted", "lzma.pyc"))