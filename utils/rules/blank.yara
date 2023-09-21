include "pyinstaller.yara"

rule Blank {
	meta:
		author = "TaxMachine"
	
	strings:
		$loader = { 6C 6F 61 64 65 72 2D 6F }
		$blank = { 62 6C 61 6E 6B 2E 61 65 73 }
		$xrarregkey = { 78 72 61 72 72 65 67 2E 6B 65 79 }
		$rar = { 72 61 72 2E 65 78 65 }

	condition:
		$loader or $blank and $xrarregkey and $rar
}