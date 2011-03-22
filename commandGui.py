# -*- coding: utf-8 -*-
import re
import sys

import controller

def pd(str):
    """(global) Dialog printer;
       prints NOT to stdout, instead to stderr
    """
    print >> sys.stderr, str

class CommandGui:
    def __init__(self, controller):
	
	self.controller = controller

        self.keineAuswahlState = KeineAuswahlState(self)

	self.semestergruppen = sorted(self.controller.getSemestergruppen())

	self.semestergruppenStates = []
	for i in range(0, len(self.semestergruppen)):
	    self.semestergruppenStates.append(VeranstaltungenState(self, self.semestergruppen[i]))

	self.curState = self.setState(self.keineAuswahlState)

    def setState(self, state):
        self.curState = state
	self.curState.onEntry()
    

class State:
    def __init__(self, fsm):
        self.fsm = fsm

    #common used helper

    def write(self):
	if self.fsm.controller.selectedVeranstaltungen != set([]):
	    self.fsm.controller.writeIcalendar()
	    pd("Icalendar written")
	else:
	    pd("Keine Veranstaltung ausgewählt -> kein icalendar erzeugt")

    def toggleVeranstaltung(self, veranstaltung):
        if veranstaltung in self.fsm.controller.selectedVeranstaltungen:
	    self.fsm.controller.selectedVeranstaltungen.remove(veranstaltung)
	else:
	    self.fsm.controller.selectedVeranstaltungen.add(veranstaltung)

class KeineAuswahlState(State):
    def __init__(self, fsm):
       State.__init__(self, fsm)

       #self.semestergruppen = sorted(fsm.controller.getSemestergruppen())

    def onEntry(self):
        self.printSemestergruppen()
	self.printGruppenauswahlDialog()

	result = sys.stdin.readline()
        
	#navigate
	m = re.match(r"n([0-9]+)", result)
	if m != None:
	    number = int(m.group(1))
	    pd(str(number))
	    self.fsm.setState(self.fsm.semestergruppenStates[number])

	else:
	    # toggle selection
	    m = re.match("([0-9]+)", result)
	    if m != None:
	        number = int(m.group(1))
	        pd("toggle selection")
		for veranstaltung in self.fsm.controller.getVeranstaltungen(self.fsm.semestergruppen[number]):
		    self.toggleVeranstaltung(veranstaltung)
		self.fsm.setState(self)
	    # write and quit
	    elif re.match("wq", result) != None:
	        pd("wq eingegeben")
		self.write()
	    else:
	        pd("invalid input")
	        self.fsm.setState(self)

    # state specific behavior

    def printSemestergruppen(self):
        for i in range(0, len(self.fsm.semestergruppen)):
	    selected = ""
	    if self.gruppeSelected(self.fsm.semestergruppen[i]):
	        selected = " *"
    	    pd("%.2d\t" % i + self.fsm.semestergruppen[i] + selected)
    def printGruppenauswahlDialog(self):
        pd("navigate: n<number>, toggle selection: <number>, write&quit: wq")

    # helper

    def gruppeSelected(self, semestergruppe):
	return (self.fsm.controller.selectedVeranstaltungen &
	         set(self.fsm.controller.getVeranstaltungen(semestergruppe)) != set([]))

class VeranstaltungenState(State):
    def __init__(self, fsm, semestergruppe):
       State.__init__(self, fsm)

       self.semestergruppe = semestergruppe
       self.veranstaltungen = sorted(fsm.controller.getVeranstaltungen(semestergruppe))

    def onEntry(self):
	self.printVeranstaltungen()
        self.printVeranstaltungenAuswahlDialog()

	result = sys.stdin.readline()
        
	#navigate
	m = re.match(r"(b).*", result)
	if m != None:
	    self.fsm.setState(self.fsm.keineAuswahlState)
	else:
	    # toggle selection
	    m = re.match("([0-9]+)", result)
	    if m != None:
	        number = int(m.group(1))
	        pd("toggle selection")
		pd(self.veranstaltungen[number])
		self.toggleVeranstaltung(self.veranstaltungen[number])
		self.fsm.setState(self)
	    # write and quit
	    elif re.match("wq", result) != None:
	        print "wq eingegeben"
		self.write()
	    else:
	        pd("invalid input")
	        self.fsm.setState(self)

    # state specific behavior

    def printVeranstaltungen(self):
        for i in range(0, len(self.veranstaltungen)):
	    selected = ""
	    if self.veranstaltungSelected(self.veranstaltungen[i]):
	        selected = " *"
    	    pd("%.2d - - " % i + self.veranstaltungen[i] + selected)

    def printVeranstaltungenAuswahlDialog(self):
        pd("back: b, toggle selection: <number>, write&quit: wq")

    # helper

    def veranstaltungSelected(self, veranstaltung):
	return (self.fsm.controller.selectedVeranstaltungen &
	         set([veranstaltung]) != set([]))

