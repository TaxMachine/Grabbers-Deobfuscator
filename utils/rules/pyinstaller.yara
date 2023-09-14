rule PyInstaller {
    meta:
        author = "TaxMachine"

    strings:
        $pyinstaller = { 4D 45 49 0C 0B 0A 0B 0E 01 16 24 }
        $pyz00 = { 50 59 5A 2D 30 30 2E 70 79 7A 00 00 00 00 }

    condition:
        $pyinstaller and $pyz00
}