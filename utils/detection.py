import yara

from os.path import exists, join, sep, dirname
from utils.decompile import disassemblePyc

BenRule = yara.compile(source='rule Ben { meta: author = "TaxMachine" strings: $benclass = { 6E 65 74 2F 6A 6F 64 61 68 2F '
                       '74 79 70 65 74 6F 6F 6C 73 2F 42 65 6E 2E 63 6C 61 73 73 50 4B 01 02 14 00 14 00 08 08 08 00 '
                       '} $jar = { 50 4B 03 04 } condition: $jar and $benclass }')
BlankRule = yara.compile(source='rule Blank { meta: author = "TaxMachine" strings: $loader = { 6C 6F 61 64 65 72 2D 6F } '
                         '$blank = { 62 6C 61 6E 6B 2E 61 65 73 } $xrarregkey = { 78 72 61 72 72 65 67 2E 6B 65 79 } '
                         '$rar = { 72 61 72 2E 65 78 65 } condition: $loader or $blank and $xrarregkey and $rar}')


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
    def BlankGrabberDetect(decompdir: str) -> bool:
        return exists(join(decompdir, "blank.aes"))

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
