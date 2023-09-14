import re
from os.path import exists, join, sep
from utils.decompile import disassemblePyc


class Detection:
    @staticmethod
    def BlankObfDetect(decompdir):
        try:
            ## Very shitty but it works ig
            file = decompdir.split(".exe")[0].split(sep)[-1] + ".pyc"
            assembly = disassemblePyc(decompdir + sep + file)
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

    @staticmethod
    def BlankGrabberDetect(decompdir):
        return exists(join(decompdir, "loader-o.pyc"))

    @staticmethod
    def EmpyreanDetect(decompdir):
        return exists(join(decompdir, "PYZ-00.pyz_extracted", "config.pyc"))

    @staticmethod
    def BenGrabberDetect(decompdir):
        return exists(join(decompdir, "net", "jodah", "typetools"))

    @staticmethod
    def ThiefcatDetect(decompdir):
        return exists(join(decompdir, "PYZ-00.pyz_extracted", "configparser.pyc")) and exists(join(decompdir, "PYZ-00.pyz_extracted", "gzip.pyc")) and exists(join(decompdir, "PYZ-00.pyz_extracted", "lzma.pyc"))