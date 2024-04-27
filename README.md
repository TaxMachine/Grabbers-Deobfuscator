# Grabbers Deobfuscator

This repository contains some methods to disassemble and deobfuscate discord malwares (Blank, and others). It will give you the webhook and validate it if it found one.

## Usage

Open cmd.exe (or powershell idfk) and type this in the SAME directory as the script

```cmd
python deobf.py [yourfile.exe]
```

You can also directly analyze it from a external source

```cmd
python deobf.py -d https://link.com/malware.exe
```

You can also do this to get help

```cmd
python deobf.py -h
```

some grabbers like empyrean need python 3.10 so be sure to check the extractor warnings if there are.
**if you have an error with thiefcat deobfuscation, use python 3.11.4**
![Tutorial](tutorial.gif)

## Decompiler & Disassembler

pycdc is precompiled and the binaries are in this repo but if you think these are not safe, please build your own (recommended). Here's the decompiler repository: [https://github.com/zrax/pycdc]

## TODO

if you wish to add a grabber to the methods, Dm me on Discord: `taxmachine` (link the source code if existing and send me a sample of it (.exe)) or fork this repository and make a pull request.

- [x] Blank (python)
- [x] Vespy (python)
- [x] Luna (python)
- [x] Red Tiger (python)
- [x] Vare obfuscation (Potna stealer?) (python)
- [x] All the random python grabbers with no obfuscation
- [x] W4SP (python)
- [x] Thiefcat (python)
- [x] Ben (Java)
- [x] Creal (python)

## Issues

If you encounter an issue, before creating one on github, please read this. Provide as much informations as possible (stacktraces, with what you used it). If its because your grabber is unsupported, submit your sample in my Discord dms

## Credits

- [PyInstxtractor](https://github.com/extremecoders-re/pyinstxtractor) for the pyinstaller archive extractor
- [PyInstxtractor-ng](https://github.com/extremecoders-re/pyinstxtractor) for the encrypted pyinstaller archive extractor
- [pycdc](https://github.com/zrax/pycdc) for the python bytecode disassembler
