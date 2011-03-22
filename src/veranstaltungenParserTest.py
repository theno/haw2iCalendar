# -*- coding: utf-8 -*-

import unittest

from veranstaltungen import VeranstaltungParser

class TestParser(unittest.TestCase):
    def testDeclaration(self):
        
        tokenTestData = {
            "Semesterkuerzel" : ["BTI5", "BAI5", "BAI1", "MINF2"],
            "Kuerzel" : ["PJ1", "AW2", "DB"],
            "FachKuerzel" : ["PJ", "AW", "DB"],
            "GwKuerzel" : ["DANN", "ZOEL", "STFF_Z", "SRHF_TK"],

            "GwKurs" : ["GWb SRHF_TK", "GWu STFF_Z", "GWu ZOEL", "GWu DANN"],
            "Orientierungseinheit" : ["BTI1-OE I", "BTI2-OE II"],
            "Praktikum" : ["BAI1-PRP1/02", "BTI1-GTP/02"],
            "Projekt" : ["INF-PRO 8", "INF-PRO 4"],
            "Seminar" : ["BAI5-AIS+BTI5-TIS"],
            "Uebung" : ["MINF2-THÜ/01"],
            "Vorlesung" : ["BAI1-PR1"],
            "Vorkurs" : ["Vorkurs PRG"],
            "VorlUebung" : ["BAI1-GI/GIÜ"],
            "Wahlpflichtmodul" : ["INF-WP-C1"],
            "WpPraktikum" : ["INF-WPP-B4/01", "INF-WPP-A1/01"],

            "ue" : ["Ü"]
	}

	for token in tokenTestData:
	    production = token
	    testData = tokenTestData[token]
	    for testDatum in testData:
	        success, children, nextcharacter = VeranstaltungParser.parse(testDatum, production)
		def errStr():
		    from pprint import pformat
		    r =  """Could not parse %s\nas a\n\n%s\t(%s chars parsed of %s)"""%(
		             repr(testDatum), production, nextcharacter, len(testDatum))
	            r += "\n\nreturned value was:\n\n" + pformat((success, children, nextcharacter))
	            r += "\n\nparsed:\n+++\n" + str(testDatum)[0:nextcharacter] + "\n+++"
	            r += "\n\nNOT parsed:\n+++\n" + str(testDatum)[nextcharacter:len(testDatum)] + "\n+++"
		    return r
		assert success and nextcharacter==len(testDatum), errStr()


if __name__ == "__main__":
    unittest.main()

