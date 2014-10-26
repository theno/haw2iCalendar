haw2iCalendar
====

Termine der HAW-Veranstaltungen individuell zusammenstellen und im eigenen
Kalenderprogramm (z.B. Google Calendar) verwenden.

Features
----

 * für Department Informatik (Inf) sowie Informatik und Elektrotechnick (EuI)
 *  für Studenten und Dozenten
 *  ausführliche Veranstaltungsnamen
 *  zwei Guis:
   * haw2iCalendar.py
   * klickiBunti.py
 * {Uni,Linu}x, Windows
 * OpenSource

Ablauf
----

 1. HAW-Kalender Textdatei einlesen
 1. Termine auswählen
 1. Auswahl als iCalendar-Datei (*.ics) speichern.
 1. iCalendar-Datei in eigener Kalender-Anwendung importieren


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

haw2iCalendar ist in Python geschrieben. Neben einer Standard
Python-Installation (2.7.x) benötigt es noch:

 * SimpleParse: <http://simpleparse.sourceforge.net/>
 * wxglade (nur für klickiBunti.py): <http://wxglade.sourceforge.net/> 
  * Unter Ubuntu 10.10 (x86_64) wird dies mit einem
     'aptitude install python python-simpleparse python-wxglade'
    erledigt.

  * Unter Windows 7 (x86_64) ist es mir gelungen, haw2iCalendar zu verwenden,
    sofern ich immer die 32-bit Versionen installiert habe.

  * Einen Mac hatte ich bisher nicht zur Verfügung gehabt. Wenn jemand
    hier haw2iCalendar erfolgreich zum Laufen bekommt, bitte ich um Info
    der notwendigen Schritte.

haw2iCalendar selber wird 'installiert', indem es in einen Ordner Deiner
Wahl abgelegt wird:
    'git clone https://github.com/theno/haw2iCalendar.git'

Im Root-Dir liegen die zwei GUIs:
 * `python2 haw2iCalendar.py` -- startet die commandGui.py -- die Referenz-GUI (läuft in einem Terminal)
 * `python2 haw2iCalendar-klickiBunti.py` -- für Mausschubser ;-)


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

    python2 haw2iCalendar-klickiBunti.py

Hintergrund
----

Das Department Informations- und Elektrotechnik sowie das Department Informatik
der Hochschule für Angewandte Wissenschaften Hamburg (HAW) veröffentlicht neben
den PDFs die Termine aller Veranstaltungen (Vorlesungen, Praktika, Übungen,
etc.) auch in einer einzelnen Textdatei.  Diese (für Menschen nur mühsam
lesbare) Textdatei hat eine strukturierte Form (die sich andauerend ändert...),
jedoch folgt sie keinem Standard. DER Standard für Kalenderdateien ist im
RFC5545 definiert und heißt iCalendar.

Ablauf
----

Eine HAW-Kalender Textdatei wird von haw2iCalendar geladen und
anschließend geparst. Nun sind alle Veranstaltungen in einem aufklappbaren
Menü aufgelistet.
Dieses Menü kann nach den Semestern gruppiert werden (Studentensicht) oder
nach den Dozenten gruppiert werden (Dozentensicht).
Nun können dort Veranstaltungen per Doppelklick ausgewählt werden.
Anschließend wird diese Auswahl per Knopfdruck als iCalendar-Datei (`*.ics`)
gespeichert.

Das Besondere an haw2iCalender ist, daß aus einer Abkürzung der volle Name
einer Veranstaltung abgeleitet wird. So mußt Du nicht diese ganzen
komischen Abkürzungen auswendig lernen.
Jedoch geht keine Info verloren: In der Beschreibung zu einem Termin wird
sowohl die eigentliche Abkürzung, das Kürzel des Dozenten als auch die
Version des HAW-Kalender aufgeführt.

Weiterhin gibt es auch die Möglichkeit, in einem Rutsch iCalendar-Dateien
jeweils für alle Semestergruppen und Dozenten zu erzeugen ('Batch'-Menü).

haw2iCalendar mit Google Calendar verwenden
----

Wenn Du kein Problem damit hast, daß USA-Behörden Zugriff
auf Deine Termine erhalten, kannst Du die mit haw2iCalendar erzeugten
iCalendar-Dateien in den Google Kalender importieren. Diese hast Du dann
auf deinem (Android-) Smartphone immer dabei.

Am besten erstellst Du in Google Kalender unter
*'Meine Kalender -> Hinzufügen'* zunächst einen separaten Kalender für die
HAW-Veranstaltungen (z.B. "WiSe2011/12").
Anschließend auf 'Weitere Kalender -> Hinzufügen -> Kalender importieren'
drücken. Dort die mit haw2iCalendar erzeugte iCalendar-Datei auswählen und 
als Ziel den soeben erstellten Kalender festlegen.

Wenn nun eine neue Version der HAW-Kalender Textdatei veröffentlicht wird,
kannst Du einfach einen neuen Kalender mit den geänderten Terminen anlegen
und den alten Kalender wegschmeißen. Praktisch.

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

Es gibt doch schon Programme, um eine Kalender-Datei zu erstellen, wieso nun haw2iCalendar?
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

 * HAW Stundenplan Tool: <http://blog.seveq.de/haw-stundenplan-tool/>

 * HAWPlantool
   * zu finden im pub: `userName@shell:/home/pub> ls **/* | grep -C 5 -i plantool)`

   * hexren hat das HAWPlantool von Arvid auf github 'gelagert': https://github.com/Hexren/HAWPlantool

 * HAWapp: <http://www.myhaw.de/board/index.php?showtopic=9080&st=0&#entry68128>
 

Wieso kein Webdienst?
----
 
Ein Webdienst macht nur Sinn, wenn er auch durchgehend erreichbar ist.
Ein Webdienst muss gepflegt werden; ein Programm kannst Du immer verwenden.
Die Erfahrung hat mich gelehrt, daß der ein- oder andere Web-Dienst der HAW
"gerne mal ausfällt". haw2iCalendar soll nicht dazu gehören.

Die Idee eines per URL abbonierten Kalenders ist zwar reizvoll wegen
der Möglichkeit automatischer Updates, andererseits können dort keine
individuellen Terminänderungen vorgenommen werden.


Wieso keine Android-App?
----

Mit einer Android-App wäre man an nur ein System gebunden. haw2iCalendar
läuft auf GNU-Linux, Mac-OS und Windows, und mit den erzeugten iCalendar-
Dateien können viele Anwendungen und Umgebungen etwas anfangen.


Weiteres Kommando
====

`src/allgroups2icalendar.py` zeigt, wie haw2icalendar automatisiert (z.b. in
einer webanwendung -- spontan fällt mir django ein) verwendet werden kann,
etwa um von vorne herein ein standardisiertes format der veröffentlichten
veranstaltungspläne zu verwenden (wink-mit-dem-zaunpfahl).


Kontakt
====

Wenn Du einen Fehler findest, eine Idee zur Verbesserung hast, oder Kritik äussern möchtest, melde Dich bitte bei mir:

`theodor.nolte@{,www.informatik.}haw-hamburg.de`