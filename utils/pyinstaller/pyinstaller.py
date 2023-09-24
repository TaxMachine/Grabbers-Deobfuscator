from utils.pyinstaller.extractors.pyinstxtractor import PyInstArchive
from utils.pyinstaller.extractors.pyinstxtractorng import PyInstArchive as PyInstArchiveNG

from typing import List


def ExtractPYInstaller(filename: str) -> PyInstArchive | PyInstArchiveNG:
    arch: PyInstArchive | PyInstArchiveNG = None
    try:
        arch = PyInstArchive(filename)
        if arch.open() and arch.checkFile() and arch.getCArchiveInfo():
            arch.parseTOC()
            arch.extractFiles()
            # print('[+] Successfully extracted pyinstaller archive: {0}'.format(filename))
    except Exception:
        arch = PyInstArchiveNG(filename)
        if arch.open() and arch.checkFile() and arch.getCArchiveInfo():
            arch.parseTOC()
            arch.extractFiles()
            # print(f"[+] Successfully extracted pyinstaller archive: {filename}")
    finally:
        arch.close()
    return arch
