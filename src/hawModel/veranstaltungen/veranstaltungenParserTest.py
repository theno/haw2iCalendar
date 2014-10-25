#!/usr/bin/python2
# -*- coding: utf-8 -*-

###########################################################################
#  Copyright 2011 Theodor Nolte                                           #
#                                                                         #
#  This file is part of haw2iCalendar.                                    #
#                                                                         #
#  haw2iCalendar is free software: you can redistribute it and/or modify  #
#  it under the terms of the GNU General Public License as published by   #
#  the Free Software Foundation, either version 3 of the License, or      #
#  (at your option) any later version.                                    #
#                                                                         #
#  haw2iCalendar is distributed in the hope that it will be useful,       #
#  but WITHOUT ANY WARRANTY; without even the implied warranty of         #
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the          #
#  GNU General Public License for more details.                           #
#                                                                         #
#  You should have received a copy of the GNU General Public License      #
#  along with haw2iCalendar.  If not, see <http://www.gnu.org/licenses/>. #
###########################################################################

import unittest

from veranstaltungenParser import VeranstaltungParser

tokenTestData = {
    # low level token
    "fachKuerzel" : ["PJ", "AW", "DB", "BU"],
    "gwKuerzel" : ["DANN", "ZOEL", "STFF_Z", "SRHF_TK"],
    "kuerzel" : ["PJ1", "AW2", "DB"],
    "semesterkuerzel" : ["BTI5", "BAI5", "BAI1", "MINF2", "A-M2", "BWI1", "BTI1"],

    # mid level token
    "awSeminar" : ["MINF1-AW1", "MINF2-AW2"],
    "gwKurs" : ["GWb SRHF_TK", "GWu STFF_Z", "GWu ZOEL", "GWu DANN", "GW MATT", "GW RDTK SL", "GW SRHF_TK"],
    "labor" : ["IE2-EEL2/01", "BMT6-Robot L"],
    "orientierungseinheit" : ["BTI1-OE I", "BTI2-OE II", "BWI1 OE I", "MINF1 OE"],
    "praktikum" : ["BAI1-PRP1/02", "BTI1-GTP/02", "A-M2-PSP", "BMT5- BUP"],
    "projekt" : ["INF-PRO 8", "INF-PRO 4"],
    "seminar" : ["BAI5-AIS+BTI5-TIS"],
    "teamStudienEinstieg" : ["BTI1-TSE/02", "BTI1-TSE/01", "BAI1-TSE/02", "E1a-TSE", "BWI1 TSE/01", "BTI1 TSE"],
    "tutorium" : ["E1a-ET1 Tutor", "E1b-PH1 Tutor", "E4a/b GR Tutor"],
    "uebung" : ["MINF2-THÜ/01", "BMT2-TM2 Ü/01"],
    "verbundprojekt" : ["A-M2-VPJ"],
    "vorkurs" : ["Vorkurs PRG"],
    "vorlesung" : ["BAI1-PR1", "BMT5 BU"],
    "vorlUebung" : ["BAI1-GI/GIÜ"],
    "wahlpflichtmodul" : ["INF-WP-C1"],
    "wpPraktikum" : ["INF-WPP-B4/01", "INF-WPP-A1/01"],

    # high level token
    "veranstaltung" : ["INF-WPP-B4/01", "INF-WPP-A1/01", "GWb SRHF_TK", "GWu STFF_Z", "GWu ZOEL", "GWu DANN",
                       "BTI1-OE I", "BTI2-OE II", "BAI1-PRP1/02", "BTI1-GTP/02", "INF-PRO 8", "INF-PRO 4",
                       "BAI5-AIS+BTI5-TIS", "MINF2-THÜ/01", "BMT2-TM2 Ü/01", "BAI1-PR1", "E1a-TSE", "IE2-EEL2/01",
                       "BMT6-Robot L", "E1a-ET1 Tutor", "E1b-PH1 Tutor", "Vorkurs PRG", "A-M2-VPJ", "BAI1-GI/GIÜ",
                       "INF-WP-C1", "MINF1-AW1", "MINF2-AW2", "BWI1 OE I", "BWI1 TSE/01", "MINF1 OE", "BMT5 BU",
                       "BMT5- BUP",
                       
                       "foo bar baz bla",

                       # Inf, WiSe 2014
                       'BAI1-PM1/PT', 'BAI1-PTP/01', 'BAI1-PTP/07 optional', 'BAI2-RMP', 'BAI2-RMPP/01',
                       'BAI3-GKAP/01', 'BWI5-REC', 'BWI5-WI3', 'BWI5-WIP3/01', 'BWI5-WIS A', 'INF-WPnurWI/01',
                       'BTI1-PM1/PT', 'BTI1-PTP/02', 'BTI1-PTP/08 optional', 'BWI1-GM', 'BWI1-GMÜ', 'BWI1-GWIÜ/01',
                       'BWI1-PM1/PT', 'BWI1-PTP/04', 'BWI3-SEA1', 'BWI3-SEAP1/03', 'BWI3-WI1', 'BWI3-WIP1/03',
                       'BWI3-WS', 'BWI3-WSP/03',

                       # EuI, WiSe 2014
                       'A-M-ASS', 'A-M-MRP/01', 'EuI-M-WP1', 'EuI-M-WP3/WPP3', 'EuI-M-WPP4',
                       'B-EE1-MA1 Tutorium', 'B-EE1-MA1/MAÜ1', 'B-EE1-PH1', 'B-EE1-PR1', 'B-EE1-PR1 Tutorium',
                       'BMT1-KO1', 'BMT1-TMA/TMÜA',
                       'BMT2-TMB', 'BMT2-TMBÜ',
                       'BMT3-KO3', 'BMT3-KO3/KOP3', 'BMT3-WK',
                       'BMT4-AT1', 'BMT4-ATP1/02', 'BMT4-ATP1/03 (geparkt)', 'BMT4-EM', 'BMT4-EMP/03', 'BMT4-MK/MKP', 'BMT4-MP',
                       'BMT5-AT2', 'BMT5-MD/MDP', 'BMT6-ED', 'BMT6-SN', 'BMT6-SNP/01 (geparkt)',
                       'BMT6-BV', 'BMT6-EDP/01', 'BMT6-HT/HTP', 'BMT6-RO/ROP', 'BMT6-SN',
                       'E1a-EK/01', 'E1a/b-EK/03',
                       'E1b-ALÜ/01 u 02',
                       'E1a/b-W-PRP1/PR1',
                       'E6-DÜ', 'E6-DÜP/01', 'E6-AÜ', 'E6-AÜP/01', 'E7-PRO1',
                       'IE3-EM', 'IE3-EME/03',
                       'IE7-CJ', 'IE7-CM1', 'IE7-CML1/02', 'IE7-CML2/02',
                       'EuI-M-WP3', 'EuI-M-WP3/WPP3', 'EuI-M-WPP2/02', 'IKM1-HM', 'IKM1-HMP/01', 'IKM1/MES1-AM',
                       'EuI-M-WPP4', 'MES1-SC',
                       'EuI-Dienstbesprechung', 'EuI-Konvent', 'IE7-CJ', 'IE7-CM1', 'IE7-CML1/02',
    ]
}

class TestParser(unittest.TestCase):

    def testDeclaration(self):
        for token in tokenTestData:
            production = token
            testData = tokenTestData[token]
            for testDatum in testData:
                success, children, nextcharacter = VeranstaltungParser.parse(testDatum, production)

                from pprint import pformat
                def errStr():
                    r =  """Could not parse %s\nas a\n\n%s\t(%s chars parsed of %s)"""%(
                             repr(testDatum), production, nextcharacter, len(testDatum))
                    r += "\n\nreturned value was:\n\n" + pformat((success, children, nextcharacter))
                    r += "\n\nparsed:\n+++\n" + str(testDatum)[0:nextcharacter] + "\n+++"
                    r += "\n\nNOT parsed:\n+++\n" + str(testDatum)[nextcharacter:len(testDatum)] + "\n+++"
                    return r

                assert success and nextcharacter==len(testDatum), errStr()
                print testDatum + ": " + production + " parsed, details:\n " + pformat(children)

if __name__ == "__main__":
    unittest.main()

