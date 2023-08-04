import re, os
from utils.decompile import disassemblePyc


class Detection:
    def BlankObfDetect(dir):
        try:
            ## Very shitty but it works ig
            file = dir.split(".exe")[0].split(os.path.sep)[len(dir.split(os.path.sep)) - 1] + ".pyc"
            assembly = disassemblePyc(dir + os.path.sep + file)
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
        return os.path.exists(os.path.join(dir, "loader-o.pyc"))
    
    def EmpyreanDetect(dir):
        return os.path.exists(os.path.join(dir, "PYZ-00.pyz_extracted", "config.pyc"))