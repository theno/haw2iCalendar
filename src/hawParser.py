from simpleparse.common import numbers #for token 'int'
from simpleparse.parser import Parser

declaration = r'''#<token> := <definition>
datei              := semestergruppe, ((t/lb)*, semestergruppe)*, (t/lb)*
semestergruppe     := header, (t/lb)*, sections

header             := ersteZeile, lb, zweiteZeile

ersteZeile         := "Stundenplan", ts, infoString
infoString         := semester, ts, "(Vers.", version, " vom ", versionsDatum, ")"
semester           := "WiSe"/"SoSe", ts, jahr
jahr               := int
<version>          := -ts+
<versionsDatum>    := -')'+

zweiteZeile        := "Semestergruppe",  ts, gruppenKuerzel
gruppenKuerzel     := -lb+

sections           := section, ((t/lb)+, section)*
section            := wochen, lb, bezeichner, (lb, eintrag)+

wochen             := wocheOrWochenRange, (", ", wocheOrWochenRange)*
wocheOrWochenRange := wochenRange / woche
wochenRange        := anfangsWoche, "-", endWoche
anfangsWoche       := woche
endWoche           := woche
woche              := int

eintrag            := fach, tr, dozent, tr, raum, tr, wochentag, tr, anfang, tr, ende
fach               := keinTrenner+
dozent             := keinTrenner*
raum               := keinTrenner*
wochentag          := c"Mo"/c"Di"/c"Mi"/c"Do"/c"Fr"/c"Sa"/c"So"
anfang             := uhrzeit
ende               := uhrzeit
uhrzeit            := h, ':', m
h                  := int
m                  := int

# help-patterns:
<ts>               := t*
<t>                := [ \t]
<keinTrenner>      := -tr
<tr>               := ','
<lb>               := "\r\n" / '\n'
<bezeichner>       := -lb+
'''

HawParser = Parser(declaration, root="datei")

