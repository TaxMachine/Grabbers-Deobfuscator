rule Ben {
	meta:
		author = "TaxMachine"

	strings:
		$benclass = { 6E 65 74 2F 6A 6F 64 61 68 2F 74 79 70 65 74 6F 6F 6C 73 2F 42 65 6E 2E 63 6C 61 73 73 50 4B 01 02 14 00 14 00 08 08 08 00 }
		$jar = { 50 4B 03 04 }

	condition:
		$jar and $benclass
}