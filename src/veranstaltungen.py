# -*- coding: utf-8 -*-

from simpleparse.common import numbers #for token 'int'
from simpleparse.parser import Parser

# Beispiele:
#
# Vorlesung:       BAI1-PR1                 Programmieren I
# Praktikum:       BAI1-PRP1/02             Praktikum Programmieren I
# Übung:           MINF2-THÜ/01             Übung Theoretische Informatik (Gruppe 1)
# VorlÜbung:       BAI1-GI/GIÜ              Vorl./Übung Grundlagen der Informatik
# Wahlpflichtfach: INF-WPP-B2/01 INF-WP-C1  Wachlpflichtmodul
# Seminar:         BAI5-AIS+BTI5-TIS        Seminar
#                  MINF2-AW2                Seminar Anwendungen II
# Projekt:         INF-PRO 8                Projekt (Gruppe 8)
# Vorkurs:         Vorkurs PRG              Vorkurs Programmieren
# Geswissensch.    GWu DANN                 GW-Kurs DANN
#                  GWb SRHF_TK              GW-Kurs SRHF_TK
# Orientierungse.  BAI1-OE I                Orientierungseinheit

declaration = r'''#<token> := <definition>
Veranstaltung := Vorlesung / Uebung / VorlUebung / Vorkurs / Orientierungseinheit /
                  Wahlpflichtmodul / WpPraktikum / Seminar / Projekt / Praktikum / GwKurs

GwKurs              := "GW", [ub], " ", GwKuerzel
Orientierungseinheit := Semesterkuerzel, "OE I", "I"?
Praktikum            := Semesterkuerzel, "-", Kuerzel, "P", No?, "/", Gruppe
Projekt              := "INF-PRO ", Gruppe
Seminar              := Semesterkuerzel, "-", ("AIS"/"TIS"), "+", Semesterkuerzel, "-", ("AIS"/"TIS")
Uebung               := Semesterkuerzel, "-", Kuerzel, "Ü", No?, "/", Gruppe
Vorlesung            := Semesterkuerzel, "-", Kuerzel, No?
Vorkurs              := "Vorkurs ", FachKuerzel
VorlUebung           := Semesterkuerzel, "-", Kuerzel, "/", Kuerzel, "Ü"
Wahlpflichtmodul     := "INF-WP-", AlphanumGruppe, No
WpPraktikum         := "INF-WPP-", AlphanumGruppe, No, "/", Gruppe

Semesterkuerzel      := -"-"+
Kuerzel              := FachKuerzel, Nummer?
FachKuerzel          := -int+
GwKuerzel            := [a-zA-Z_-]+
Nummer               := int
No                   := int
Gruppe               := int
AlphanumGruppe       := [A-Z]

ue                   := "Ü"
'''
VeranstaltungParser = Parser(declaration)

fullNames = {

# Master Informatik

"MINF1-AW1"     : "Seminar Anwendungen 1",
"MINF1-TT1"     : "Vorl. Technik und Technologie 1",
"MINF1-MT"      : "Vorl. Modellierung Technischer Systeme",
"MINF1-MI"      : "Vorl. Modellierung von Informationssystemen",

"MINF2-TH1"      : "Vorl. Theoretische Informatik",
"MINF2-THÜ/01"  : "Übung Theoretische Informatik (Gruppe 1)",
"MINF2-THÜ/02"  : "Übung Theoretische Informatik (Gruppe 2)",
"MINF2-AW2"     : "Seminar Anwendungen 2",
"MINF2-TT2"     : "Vorl. Technik und Technologie 2",
"MINF2-TTP2/01" : "Praktikum Technik und Technologie (Gruppe 1)",
"MINF2-TTP2/02" : "Praktikum Technik und Technologie (Gruppe 2)",
"MINF2-PJ1"     : "Projekt I",

"MINF3-SEM"     : "Seminar",
"MINF3-TH2"     : "Vorl. Theoretische Informatik 2",
"MINF3-THÜ1/01" : "Übung Theoretische Informatik 3 (Gruppe 1)",
"MINF3-THÜ1/02" : "Übung Theoretische Informatik 3 (Gruppe 2)",
"MINF3-PJ2"     : "Projekt II",
"MINF3-UO"      : "Vorlesung Unternehmensorientierung",
"MINF3-UOÜ/01"  : "Übung Unternehmensorientierung (Gruppe 1)",
"MINF3-UOÜ/02"  : "Übung Unternehmensorientierung (Gruppe 2)",

"MINF4-MA"      : "Masterthesis",
"MINF4-MAK"     : "Kolloquium"
}

def test():
    from pprint import pprint
    pprint(fullNames)
    
if __name__ == "__main__":
    test()

