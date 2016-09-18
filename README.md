*****
haw2iCalendar-Webapp online:
----
[haw2iCalendar.theno.eu](https://haw2icalendar.theno.eu)
====
Bitte Bugs reporten!
----
*****


haw2iCalendar
====

Termine der HAW-Veranstaltungen individuell zusammenstellen und im eigenen
Kalenderprogramm (z.B. Google Calendar) verwenden.

Features
----

 * für **[Department Informatik (Inf)](http://www.haw-hamburg.de/ti-i/studium.html)** sowie **[Department Informations- und Elektrotechnik (IuE)](http://www.etech.haw-hamburg.de/Stundenplan/)**
 * für Studenten und Dozenten
 * ausführliche Veranstaltungsnamen (z.B. 'Praktikum Software Engineering 2 (Gruppe 3)' statt 'SEP2/03')
 * zwei Guis:
   * `haw2iCalendar.py`
   * `haw2iCalendar-klickiBunti.py`
 * {Uni,Linu}x, Windows
 * Konform zum iCalendar-Standard ([RFC-5543](http://tools.ietf.org/html/rfc5545))
 * [OpenSource](http://de.wikipedia.org/wiki/Freie_Software)

Genereller Ablauf
----

 1. HAW-Kalender csv-Textdatei einlesen
 1. Termine auswählen
 1. Auswahl als iCalendar-Datei (`*.ics`) speichern.
 1. iCalendar-Datei in eigene Kalender-Anwendung importieren


Screenshots
----

 * [Studentensicht](http://www.flickr.com/photos/62642553@N06/6173044417/in/set-72157627606253923/)
 * [Dozentensicht](http://www.flickr.com/photos/62642553@N06/8572120989/in/set-72157627606253923/)
 * [Google Calendar Import](http://www.flickr.com/photos/62642553@N06/8573215362/in/set-72157627606253923/) (eine Foto-Story)
 * [Android](http://www.flickr.com/photos/62642553@N06/8572121329/in/set-72157627606253923/)


Download
----

<https://github.com/theno/haw2iCalendar>


Installation
----

haw2iCalendar ist in **Python** geschrieben. Neben einer Standard
Python2-Installation (2.7.x) benötigt es noch:

 * **SimpleParse**: <http://simpleparse.sourceforge.net/>
 * **wxglade** (nur für klickiBunti.py): <http://wxglade.sourceforge.net/> 
  * Unter Ubuntu 10.10 (x86_64) wird dies erledigt mit einem:
    `aptitude install python python-simpleparse python-wxglade`

  * Unter Windows 7 (x86_64) ist es mir gelungen, haw2iCalendar zu verwenden,
    sofern ich immer die 32-bit Versionen installiert habe.

  * Einen Mac hatte ich bisher nicht zur Verfügung gehabt. Wenn jemand
    hier haw2iCalendar erfolgreich zum Laufen bekommt, bitte ich um Info
    der notwendigen Schritte.

**haw2iCalendar** selber wird 'installiert', indem es in einen Ordner Deiner
Wahl abgelegt wird:

    git clone https://github.com/theno/haw2iCalendar.git

Im Root-Dir liegen die zwei GUIs:
 * `python2  haw2iCalendar.py` -- startet die commandGui.py -- die Referenz-GUI (läuft in einem Terminal)
 * `python2  haw2iCalendar-klickiBunti.py` -- für Mausschubser ;-)


`haw2iCalendar.py`
====

    user@host:~/haw2iCalendar$ python2  ./haw2iCalendar.py  --help
    
    Usage: haw2iCalendar.py [-o ICS-FILE] INFILE
    
    Parse a haw calendar text file (Sem_I.txt or Sem_IuE.txt),
    select dates, convert the dates to the iCalendar format (rfc5545)
    and write them to stdout.
    
    Options:
      -h, --help        show this help message and exit
      -p, --prof        group by lecturers
      -i, --informatik  alternative grouping (by semestergruppe from header)
      -o ICS-FILE       write iCalendar-output to file instead stdout


`haw2iCalendar-klickiBunti.py`
====

    python2  ./haw2iCalendar-klickiBunti.py

Hintergrund
----

Das Department **Informations- und Elektrotechnik (IuE)** sowie das
**Department Informatik (Inf)**
der [Hochschule für Angewandte Wissenschaften Hamburg (HAW)](http://www.haw-hamburg.de/) veröffentlichen neben
den PDFs die Termine aller Veranstaltungen (Vorlesungen, Praktika, Übungen,
etc.) auch in einer einzelnen Textdatei ([IuE](http://www.etech.haw-hamburg.de/Stundenplan/Sem_IuE.txt), [Inf](http://www.haw-hamburg.de/fileadmin/user_upload/TI-I/Studium/Veranstaltungsplaene/Sem_I.txt)).  Diese (für Menschen nur mühsam
lesbare) Textdatei hat eine strukturierte Form *(die sich andauerend ändert...)*,
jedoch folgt sie keinem Standard. DER Standard für Kalenderdateien ist im
[RFC-5545](http://tools.ietf.org/html/rfc5545) definiert und heißt **iCalendar**.

Ablauf
----

Eine HAW-Kalender Textdatei wird von **haw2iCalendar** geladen und
anschließend geparst. Nun sind alle Veranstaltungen in einem aufklappbaren
Menü aufgelistet.
Alternativ zum Öffnen einer lokalen Datei können über das Menü *'Links'* die gerade auf den HAW-Webseiten
veröffentlichten Versionen heruntergeladen werden -- total praktisch.
Die Veranstaltungen können nach den Semestern gruppiert werden (**Studentensicht**) oder
nach den Dozenten gruppiert werden (**Dozentensicht**).
Nun können dort Veranstaltungen per Doppelklick ausgewählt werden.
Anschließend wird diese Auswahl per Knopfdruck als iCalendar-Datei (`*.ics`)
gespeichert.

Das Besondere an haw2iCalender ist, daß aus einer Abkürzung der volle Name
einer Veranstaltung abgeleitet wird. So mußt Du nicht diese ganzen
komischen Abkürzungen auswendig lernen.
Jedoch geht keine Info verloren: In der Beschreibung zu einem Termin wird
sowohl die eigentliche Abkürzung, das Kürzel des Dozenten als auch die
Version des HAW-Kalenders aufgeführt.

Weiterhin gibt es auch die Möglichkeit, in einem Rutsch iCalendar-Dateien
jeweils für alle Semestergruppen und Dozenten zu erzeugen (*Batch*-Menü).

haw2iCalendar mit Google Calendar verwenden
----

Wenn Du kein Problem damit hast, daß USA-Behörden Zugriff
auf Deine Termine erhalten, kannst Du die mit haw2iCalendar erzeugten
iCalendar-Dateien in den Google Kalender importieren. Diese hast Du dann
auf deinem (Android-) Smartphone immer dabei.

Am besten erstellst Du in Google Kalender unter
*'Meine Kalender -> Hinzufügen'* zunächst einen separaten Kalender für die
HAW-Veranstaltungen (z.B. "WiSe2011/12").
Anschließend auf *'Weitere Kalender -> Hinzufügen -> Kalender importieren'*
drücken. Dort die mit haw2iCalendar erzeugte iCalendar-Datei auswählen und 
als Ziel den soeben erstellten Kalender festlegen.

Wenn nun eine neue Version der HAW-Kalender Textdatei veröffentlicht wird,
kannst Du einfach einen neuen Kalender mit den geänderten Terminen anlegen
und den alten Kalender wegschmeißen -- auch voll praktisch.

Im Gegensatz zu einem abonnierten Kalender kannst Du bei einem 'eigenen'
Kalender auch selber Termine verändern, etwa weil ein Prof krank geworden
ist oder so.

Andere Kalender-Programme
----

Alle ernstzunehmenden Kalender-Programme können Termine im iCalender-Format
importieren. Auch hier empfiehlt es sich, die HAW-Termine in einem
separaten Kalender zu führen, damit diese bei Terminänderungen durch einen
neuen Kalender ersetzt werden könnnen.

Unter anderem können folgende Anwendungen oder Umgebungen mit iCalender-
Dateien umgehen:

 * Google Calendar <https://calendar.google.com/>
 * Android <https://play.google.com/store/apps/details?id=com.google.android.calendar&hl=de>
 * I-Phone <https://www.apple.com/de/iphone/>
 * Evolution <https://wiki.gnome.org/Apps/Evolution>
 * Kontact <https://userbase.kde.org/KOrganizer>


Fragen
====

Es gibt doch schon Programme, um eine Kalender-Datei zu erstellen, wieso nun **haw2iCalendar**?
----

Fun. Python-Programmierübung. Keine Lust mehr, den Kram von Hand zu machen.
Etwas, was unter Linux läuft und volle Veranstaltungsnamen erzeugt.

Außerdem wird das Parsen nicht durch Regexe erledigt, sondern durch das
Python-Modul 'SimpleParse'.
Regexe sind, finde ich, schwer zu lesen und führen somit zu schwer
wartbaren Code ('Read-only' Code).
Mit SimpleParse wird die Struktur der Haw-Kalender Textdateien und der
Veranstaltungskürzel jeweils durch eine verständlichere EBNF beschrieben.
Dank einer Testumgebung in haw2iCalendar können die EBNFs zukünftig an neue
Formulierungen zuverlässig angepasst werden (Ziel: wartbarer Code).

Welche anderen Programme gibt es noch, die sich mit diesen HAW-Kalender Textdateien herumschlagen?
----

 * **HAW Stundenplan Tool**: <http://blog.seveq.de/haw-stundenplan-tool/>

 * **HAWPlantool**
   * zu finden im pub: `userName@shell:/home/pub> ls **/* | grep -C 5 -i plantool)`

   * hexren hat das HAWPlantool von Arvid auf github 'gelagert': <https://github.com/Hexren/HAWPlantool>

 * **HAWapp**: <http://www.myhaw.de/board/index.php?showtopic=9080&st=0&#entry68128>
 

Eine haw2icalendar-Website wäre ja derbs cool, gibt es sowas?
----
 
Ja! Der Webdienst ist hier erreichbar: [haw2icalendar.theno.eu](https://haw2icalendar.theno.eu)

([Testversion](https://haw2icalendar-testing.theno.eu/)).


Wieso keine Android-App?
----

Mit einer Android-App wäre man an nur ein System gebunden. **haw2iCalendar**
läuft auf GNU-Linux, Mac-OS und Windows, und mit den erzeugten iCalendar-
Dateien können viele Anwendungen und Umgebungen etwas anfangen.


Weiteres Kommando
====

`python2  src/allgroups2icalendar.py` zeigt, wie haw2icalendar automatisiert (z.b. in
einer Webanwendung -- spontan fällt mir Django ein) verwendet werden kann,
etwa um von vorne herein ein standardisiertes Format der veröffentlichten
Veranstaltungspläne zu verwenden (Wink-mit-dem-Zaunpfahl).


Kontakt
====

Wenn Du einen Fehler findest, eine Idee zur Verbesserung hast, oder Kritik äussern möchtest, melde Dich bitte bei mir:

`theodor.nolte AT {,informatik.}haw-hamburg.de`
