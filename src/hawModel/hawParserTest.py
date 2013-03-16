# -*- encoding: utf-8 -*-

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

from hawParser import HawParser

sectionTestDatum = r"""15, 18, 21
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

semestergruppeTestDatum = r"""Stundenplan  SoSe 11 (Vers.0.9 vom 1.3.11)
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

semestergruppeTestDatum2 = r"""Stundenplan  SoSe 11 (Vers.0.9 vom 1.3.11)
Semestergruppe  M-INF2


12-14, 16, 23
Name,Dozent,Raum,Tag,Anfang,Ende
MINF2-TH1/ue,HFFM,0480,Di,12:30,15:45
MINF2-TH1,HFFM,0480,Di,12:30,15:45"""


dateiTestDatum1 = semestergruppeTestDatum
dateiTestDatum2 = semestergruppeTestDatum + "\n" + semestergruppeTestDatum2
dateiTestDatum3 = """Stundenplan  SoSe 11 (Vers.0.9 vom 1.3.11)
Semestergruppe  M-AI1


10-11
Name,Dozent,Raum,Tag,Anfang,Ende
BAI1-OE I,,1260,Do,9:00,17:00
BAI1-OE I,,1260,Fr,9:00,17:00
Stundenplan  SoSe 11 (Vers.0.9 vom 1.3.11)
Semestergruppe  M-INF2


12-14, 16, 23
Name,Dozent,Raum,Tag,Anfang,Ende
MINF2-TH1/ue,HFFM,0480,Di,12:30,15:45
MINF2-TH1,HFFM,0480,Di,12:30,15:45"""

f = open("testData/Sem_I.txt", 'r')
dateiTestDatum4 = f.read()
f.close()

f = open("testData/Sem_I.v11.txt", 'r')
dateiTestDatum5 = f.read()
f.close()

# only one semestergruppe containig all gruppenKuerzel
f = open("testData/Sem_IuE.SoSe2011.v10.txt", 'r')
dateiTestDatum6 = f.read()
f.close()

# header but no sections:
f = open("testData/Sem_IuE.SoSe2011.v11.txt", 'r')
dateiTestDatum7 = f.read()
f.close()

# header but no sections:
f = open("testData/Sem_I.WiSe2011.v101.txt", 'r')
dateiTestDatum8 = f.read()
f.close()

# header but no sections:
f = open("testData/Sem_IuE.WiSe2011.v10.txt", 'r')
dateiTestDatum9 = f.read()
f.close()

f = open("testData/Sem_I.WiSe2012.v12.txt", 'r')
dateiTestDatum10 = f.read()
f.close()

class TestParser(unittest.TestCase):
    def testDeclaration(self):
        
        tokenTestData = {
            "gruppe" : ["BAI1", "GWu", "INF", "Vorkurs"],
            "fach" : ["BAI1-GI/GIÜ", "GWu DANN", "INF-WPP-C2/01", "Vorkurs PRG", "BAI4-CI"],
            "uhrzeit" : ["17:00", "9:00", "8:15", "24:66"],
            "wochentag" : ["Mo", "Di", "Mi", "Do", "Fr", "Sa", "So", "mo", "mO", "MO"],
            "raum" : ["1260", "1101b", "1101a", "irgendwasOhneKomma"],
            "dozent" : ["SRS", "WND/[Oel]"],
            "wochen" : ["11", "12, 18, 21"],
            "bezeichner" : ["Name, Dozent, Raum, Tag, Anfang, Ende"],
            "section" : [ sectionTestDatum ],

            "version" : ["0.9", "1.2"],
            "versionsDatum" : ["1.3.11", "30.09.2012"],
            "semester" : ["SoSe 11", "WiSe 10", "WiSe 11/12", "WiSe 2012/13"],
            "infoString" : ["SoSe 11 (Vers.0.9 vom 1.3.11)",
                            "WiSe 2012/13 Vers 1.2  vom  30.09.2012",
                           ],
            "ersteZeile" : ["Stundenplan  SoSe 11 (Vers.0.9 vom 1.3.11)",
                            "Stundenplan  SoSe 11 (Vers.0.9 vom 1.3.11)",
                            "Stundenplan  WiSe 11/12 Vers.1.01 vom 16.09.2011",
                            "Stundenplan  WiSe 2012/13 Vers 1.2  vom  30.09.2012",
                           ],
            "zweiteZeile" : ["Semestergruppe  M-AI1"],
            "header" : ["Stundenplan  SoSe 11 (Vers.0.9 vom 1.3.11)\nSemestergruppe  M-AI1",
                        "Stundenplan  WiSe 11/12 Vers.1.01 vom 16.09.2011\nSemestergruppe  B-AI1",
                        ],
            "semestergruppe" : [semestergruppeTestDatum, semestergruppeTestDatum2],
            "datei" : [dateiTestDatum1, dateiTestDatum2, dateiTestDatum3,
                       dateiTestDatum4, dateiTestDatum5, dateiTestDatum6,
                       dateiTestDatum7, dateiTestDatum8, dateiTestDatum9,
                       dateiTestDatum10
                       ]
        }

        for token in tokenTestData:
            production = token
            testData = tokenTestData[token]
            for testDatum in testData:
                success, children, nextcharacter = HawParser.parse(testDatum, production)
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

