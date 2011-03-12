import unittest

from parser import *

sectionTestData = r"""15, 18, 21
Name,Dozent,Raum,Tag,Anfang,Ende
BTI3-SEP1/02,DAI,0709,Mi,8:15,11:30
BTI3-DTP/03,CNZ/[Vol],0801,Mi,12:30,15:45
BTI3-BSP/01,FHL/[Loh],0701,Mi,12:30,15:45
BTI3-ADP/02,PRG/[Nmn],1105,Mi,8:15,11:30
BTI3-SE1,DAI,0460,Fr,8:15,11:30
BTI3-DT,CNZ,1065,Do,8:15,11:30
BTI3-BS,FHL,1001,Di,12:30,15:45
BTI3-AD,PRG/SCHM,1260,Do,12:30,15:45
BTI3-AA/AAU,BRN,0360,Mo,8:15,13:30"""

dateiTestData = r"""Stundenplan  SoSe 11 (Vers.0.9 vom 1.3.11)
Semestergruppe  B-AI1


10
Name,Dozent,Raum,Tag,Anfang,Ende
BAI1-OE I,,1260,Do,9:00,17:00
BAI1-OE I,,1260,Fr,9:00,17:00

11, 12, 14
Name,Dozent,Raum,Tag,Anfang,Ende
Vorkurs PRG,,1101a,Do,8:15,14:35
Vorkurs PRG,,1101b,Fr,8:15,14:35
Vorkurs PRG,,1102,Do,8:15,14:35
BAI1-OE I,,1260,Mo,9:00,17:00
BAI1-OE I,,1260,Di,9:00,17:00
BAI1-OE I,,1260,Mi,9:00,17:00"""
#f = open("./muster.txt", "r")
#dateiTestData = f.read()
#f.close()

class TestParser(unittest.TestCase):
    def testDeclaration(self):
        
        tokenTestData = {
	    "datei" : [ dateiTestData ],
	    "ersteZeile" : ["Stundenplan  SoSe 11 (Vers.0.9 vom 1.3.11)"],
	    "semester" : ["SoSe 11", "WiSe 10"],
	    "versionsDatum" : ["1.3.11"],

	    "section" : [ sectionTestData ],
	    "bezeichner" : ["Name,Dozent,Raum,Tag,Anfang,Ende"],
	    "wochen" : ["11", "12, 18, 21"],
	    "dozent" : ["SRS", "WND/[Oel]"],
	    "raum" : ["1260", "1101b", "1101a", "irgendwasOhneKomma"],
	    "tag" : ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So", "mo", "mO", "MO"],
            "uhrzeit" : ["17:00", "9:00", "8:15", "24:66"]
	}

	for token in tokenTestData:
	    production = token
	    testData = tokenTestData[token]
	    for s in testData:
	        success, children, nextcharacter = parser.parse(s, production)
		from pprint import pprint
		def errStr():
		    return """Could not parse %s as a %s (%s chars parsed of %s), returned value was %s"""%(
		             repr(testData), production, nextcharacter,
			     len(testData), (success, children, nextcharacter))
		assert success and nextcharacter==len(s), errStr()

if __name__ == "__main__":
    unittest.main()

