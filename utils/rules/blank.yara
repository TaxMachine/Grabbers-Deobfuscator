include "pyinstaller.yara"

rule Blank {
	meta:
		author = "TaxMachine"
	
	strings:
		$loader = { 6C 6F 61 64 65 72 2D 6F 00 00 00 00 00 00 00 00 00 }
		$blank = { 62 6C 61 6E 6B 2E 61 65 73 00 00 00 00 00 00 00 00 }
		$xrarregkey = { 78 72 61 72 72 65 67 2E 6B 65 79 00 00 00 00 00 00 00 }
		$rar = { 72 61 72 2E 65 78 65 00 00 00 00 00 00 00 00 00 00 }

	condition:
		$loader and $blank and $xrarregkey and $rar
}