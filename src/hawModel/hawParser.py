# ~*~ encoding: utf-8 ~*~

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

import re

from simpleparse.common import numbers #for token 'int'
from simpleparse.parser import Parser

declaration = r'''#<token> := <definition>
datei              := semestergruppe, ((t/lb)*, semestergruppe)*, (t/lb)*
semestergruppe     := header, (t/lb)*, sections?, ((t/lb)*, "<>", (t/lb)*)?, (t/lb)*

header             := ersteZeile, (lb, zweiteZeile)?

ersteZeile         := ("Stundenplan" / "Dozentenplan"), ts, infoString, ts*
infoString         := semester, ts, "("?, "Vers", ("."/ts), ts?, version, ts, "vom", ts, versionsDatum, ")"?
semester           := "WiSe"/"SoSe", ts, jahr
jahr               := int, ("/", int)?
version            := -ts+
<versionsDatum>    := int, (".", int)*

zweiteZeile        := "Semestergruppe", ts, gruppenKuerzel
gruppenKuerzel     := -lb+

sections           := section, ((t/lb)+, section)*
section            := wochen, lb, bezeichner, (lb, eintrag)+

wochen             := wocheOrWochenRange, (", ", wocheOrWochenRange)*
wocheOrWochenRange := wochenRange / woche
wochenRange        := anfangsWoche, "-", endWoche
anfangsWoche       := woche
endWoche           := woche
woche              := int

eintrag            := septupel / sixtupel
sixtupel           := fach, tr, dozent, tr, raum, tr, wochentag, tr, anfang, tr, ende
septupel           := fach, tr, dozent, tr, gebaeude, tr, raum, tr, wochentag, tr, anfang, tr, ende

fach               := gruppe, ( [ -], keinTrenner+, ( tr, int+ )* )?
gruppe             := ("A-M", [0-9]) / ("IK-M", [0-9]) / -("Name" / [ -])+ 
dozent             := keinTrenner*
gebaeude           := keinTrenner*
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


def _truncated(text):
    """text without empty lines, and each line without leading or trailing spaces."""
    return '\n'.join([line.strip() for line in text.splitlines() if line.strip() != ''])


def prepared_Sem_I_txt(text):
    """
    Make errornous Sem_I.txt content parsable.

    Problem: ',' ist der Feldtrenner.  Aber das Komma wird in den Department-
    Informtik-Textdateien auch bei den Dozentennamen verwendet (Nachname, Vorname).
    Manchmal gibt es mehr als einen Dozenten, also auch mehrere Kommas zuviel.
    Diese Kommas werden vorm Parsen durch ein anderes Zeichen ersetzt. Dann
    ist das Komma wieder ausschließlich Feldtrenner.
    """

    if ('Padberg, Julia' in text):
        # Now we know: the comma ',' is used in a wrong way

        # <Nachname> von, <Vorname>
        pattern = r'([a-zA-ZäöüÄÖÜß -]+)\s+von\s*,\s+([a-zA-ZäöüÄÖÜß -]+)'
        repl = r'\2 von \1'
        text = re.sub(pattern, repl, text, count=0, flags=0)
    
        # <Nachname>, <Vorname>
        pattern = r'([a-zA-ZäöüÄÖÜß -]+), ([a-zA-ZäöüÄÖÜß -]+)' # ☃
        repl = r'\2 \1'
        text = re.sub(pattern, repl, text, count=0, flags=0)
    
        pattern = r'\s[ ]+'
        repl = r' '
        text = re.sub(pattern, repl, text, count=0, flags=0)

    text = _truncated(text)

#    print(text) #TODO DEBUG

    return text
