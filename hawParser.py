from simpleparse.common import numbers #for 'int'
from simpleparse.parser import Parser

declaration = r'''#<token> := <definition>
root            := datei
datei           := (t/lb)*, header, sections
sections        := ((t/lb)*, section)+

header          := ersteZeile, lb, zweiteZeile
ersteZeile      := "Stundenplan", ts, infoString
infoString      := semester, ts, "(Vers.", version, " vom ", versionsDatum, ")"
semester      := "WiSe"/"SoSe", ts, jahr
jahr          := int
<zweiteZeile>   := -lb+
<version>       := -ts+
<versionsDatum> := -')'+

section         := wochen, lb, bezeichner, (lb, eintrag)+
wochen          := woche, (", ", woche)*
woche           := int
<bezeichner>    := -lb+
eintrag         := fach, tr, dozent, tr, raum, tr, tag, tr, anfang, tr, ende
fach            := keinTrenner+
dozent          := keinTrenner*
raum            := keinTrenner+
tag             := c"Mo"/c"Di"/c"Mi"/c"Do"/c"Fr"/c"Sa"/c"So"
anfang          := uhrzeit
ende            := uhrzeit

uhrzeit         := h, ':', m
h               := int
m               := int
<ts>            := t*
<t>             := [ \t]
<keinTrenner>   := -tr
<tr>            := ','
<lb>            := "\r\n" / '\n'
'''

HawParser = Parser(declaration, "root")
