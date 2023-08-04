# Grabbers Deobfuscator
This repository contains some methods to disassemble and deobfuscate discord malwares (Blank, and others). It will give you the webhook and validate it if it found one.

# Usage
Open cmd.exe (or powershell idfk) and type this in the SAME directory as the script
```cmd
python deobf.py [yourfile.exe]
```
some grabbers like empyrean need python 3.10 so be sure to check the extractor warnings if there are.
![Tutorial](tutorial.gif)

# Decompiler & Disassembler
~~Im currently on linux so I can't compile pycdc for windows. However you can do it yourself and add the binaries inside the utils folder.~~ I got the windows binaries but if you think these are not safe, please build your own (recommended). Here's the decompiler repository: https://github.com/zrax/pycdc

# TODO
if you wish to add a grabber to the methods, Dm me on Discord: `taxmachine` (link the source code if existing and send me a sample of it (.exe)) or fork this repository and make a pull request.

- [x] Blank (python)
- [x] Vespy (python)
- [x] Luna (python)
- [x] All the random python grabbers with no obfuscation
- [ ] W4SP (python)
- [ ] Thiefcat (python)
- [ ] Ben (Java)
- [ ] QVoid (C#)
- [ ] Stealerium (C#)
- [ ] Creal (python)

# Issues
If you encounter an issue, before creating one on github, please read this. Provide as much informations as possible (stacktraces, with what you used it). If its because your grabber is unsupported, submit your sample in my Discord dms