import yara

from os.path import exists, join, sep, dirname
from utils.decompile import disassemblePyc

BenRule = yara.compile(filepath=join(dirname(__file__), "rules", "ben.yara"))
BlankRule = yara.compile(filepath=join(dirname(__file__), "rules", "blank.yara"))


class Detection:
    @staticmethod
    def BlankObfDetect(decompdir: str) -> bool:
        try:
            # Very shitty but it works ig
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
    def BlankGrabberDetect(exe: str) -> bool:
        return BlankRule.match(exe)

    @staticmethod
    def EmpyreanDetect(decompdir: str) -> bool:
        return exists(join(decompdir, "PYZ-00.pyz_extracted", "config.pyc"))

    @staticmethod
    def BenGrabberDetect(jar: str) -> bool:
        return BenRule.match(jar)

    @staticmethod
    def ThiefcatDetect(decompdir: str) -> bool:
        return exists(join(decompdir, "PYZ-00.pyz_extracted", "configparser.pyc")) and exists(
            join(decompdir, "PYZ-00.pyz_extracted", "gzip.pyc")) and exists(
            join(decompdir, "PYZ-00.pyz_extracted", "lzma.pyc"))
