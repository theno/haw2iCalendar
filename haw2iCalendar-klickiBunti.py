#!/usr/bin/python
# -*- coding: utf-8 -*-

import copy
import logging
import os
import os.path
import sys
import threading
import urllib
import webbrowser

import wx

from src.controller import Controller
from src.hawModel.hawCalendar import DOZENT, SEMESTERGRUPPE, GRUPPENKUERZEL
import src.texts as texts

STUNDENPLAN_SITE_EuI = "http://www.etech.haw-hamburg.de/Stundenplan/"
STUNDENPLAN_URL_EuI = "http://www.etech.haw-hamburg.de/Stundenplan/Sem_IuE.txt"

STUNDENPLAN_SITE_Inf = "http://www.informatik.haw-hamburg.de/veranstaltungsplaene.html"
STUNDENPLAN_URL_Inf = "http://www.haw-hamburg.de/fileadmin/user_upload/TI-I/Studium/Veranstaltungsplaene/Sem_I.txt"

def iterChildren(treeCtrl, itemId):
    curId, curItem = treeCtrl.GetFirstChild(itemId)
    while curId.IsOk(): 
        yield curId
        curId, curItem = treeCtrl.GetNextChild(itemId, curItem)

class ScrollableDialog(wx.Dialog):
    def __init__(self, parent, text, title):
        wx.Dialog.__init__(self, parent, title=title)
       
        textCtrl = wx.TextCtrl(self, -1, text, size=(810,400), style=wx.TE_MULTILINE | wx.TE_READONLY)
        font = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Courier New')
        textCtrl.SetFont(font)
        textCtrl.SetInsertionPoint(0)
       
        sizer = wx.BoxSizer(wx.VERTICAL)
       
        btnsizer = wx.BoxSizer()

        btn = wx.Button(self, wx.ID_OK)
        btnsizer.Add(btn, 0, wx.ALL, 5)
        btnsizer.Add((5,-1), 0, wx.ALL, 5)

        sizer.Add(textCtrl, 0, wx.EXPAND|wx.ALL, 5)   
        sizer.Add(btnsizer, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)   
        self.SetSizerAndFit(sizer)

EVT_BATCH_ID = wx.NewId()

def EVT_BATCH(win, func):
    win.Connect(-1, -1, EVT_BATCH_ID, func)

class BatchEvent(wx.PyEvent):
    def __init__(self, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_BATCH_ID)
        self.data = data

EVT_BATCH_FINISHED_ID = wx.NewId()

def EVT_BATCH_FINISHED(win, func):
    win.Connect(-1, -1, EVT_BATCH_FINISHED_ID, func)

class BatchFinishedEvent(wx.PyEvent):
    def __init__(self, data):
        wx.PyEvent.__init__(self)
        self.SetEventType(EVT_BATCH_FINISHED_ID)
        self.data = data

class BatchExportWorkerThread(threading.Thread):
    def __init__(self, notifyWindow, ctrl, path):
        threading.Thread.__init__(self)

        self.notifyWindow = notifyWindow
        self.ctrl = ctrl
        self.path = path

        self.wantAbort = False

        self.start()

    def run(self):

        def writeIcals(subfolder):
            for key in sorted(self.ctrl.getKeys()):

                self.ctrl.selectedVeranstaltungen = set()
                veranstaltungen = self.ctrl.getVeranstaltungen(key)
                self.ctrl.selectVeranstaltungen(veranstaltungen)

                fileName = key.replace(' ', '_').replace('/','_').replace('[','(')
                fileName = fileName.replace(']',')').replace('ß','_et_')
                fileName = fileName.replace('A', 'AE').replace('ä', 'ae')
                fileName = fileName.replace('Ö', 'OE').replace('ö', 'oe')
                fileName = fileName.replace('Ü', 'UE').replace('ü', 'ue')
                fileName += ".ics"
                if fileName==".ics": fileName = "aaa_noName.ics"

                try: os.mkdir(subfolder)
                except OSError as e: pass

                self.ctrl.setOutfile(subfolder + fileName)
                sumEvents = self.ctrl.writeIcalendar()

                text = key + ": iCalendar '" + fileName + "' created (" + str(sumEvents) + " Events)\n"
                
                #TODO: this is sooo dirty (well, I don't like wxpython)
                try:
                    wx.PostEvent(self.notifyWindow, BatchEvent(text))
                except TypeError as e:
                    return True
                #if (self.wantAbort): return True

            return False

        self.ctrl.tupleKeyIndex = self.ctrl.optimalGruppenKeyIndex()
        subfolder = self.path + "/" + "Studentensicht" + "/"
        wantAbort = writeIcals(subfolder)

        if wantAbort:
            return
        
        self.ctrl.tupleKeyIndex = DOZENT
        subfolder = self.path + "/" + "Dozentensicht" + "/"
        writeIcals(subfolder)

        wx.PostEvent(self.notifyWindow, BatchFinishedEvent(None))

    def abort(self):
        self.wantAbort = True
       
class RunningBatchExportDialog(wx.Dialog):
    def __init__(self, parent, text, title, ctrl, path):
        wx.Dialog.__init__(self, parent, title=title)
        
        EVT_BATCH(self, self.onResult)
        EVT_BATCH_FINISHED(self, self.onBatchFinished)
        workerThread = BatchExportWorkerThread(self, ctrl, path)
       
        self.textCtrl = wx.TextCtrl(self, -1, text, size=(810,400), style=wx.TE_MULTILINE | wx.TE_READONLY)
        font = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Courier New')
        self.textCtrl.SetFont(font)
        self.textCtrl.SetInsertionPoint(0)
       
        sizer = wx.BoxSizer(wx.VERTICAL)

        btnsizer = wx.BoxSizer()

        self.btnCancel = wx.Button(self, wx.ID_CANCEL)
        btnsizer.Add(self.btnCancel, 0, wx.ALL, 5)

        self.btnOk = wx.Button(self, wx.ID_OK)
        self.btnOk.Disable()
        btnsizer.Add(self.btnOk, 0, wx.ALL, 5)

        btnsizer.Add((5,-1), 0, wx.ALL, 5)

        sizer.Add(self.textCtrl, 0, wx.EXPAND|wx.ALL, 5)   
        sizer.Add(btnsizer, 0, wx.EXPAND|wx.ALIGN_CENTER_VERTICAL|wx.ALL, 5)   
        self.SetSizerAndFit(sizer)

    def onResult(self, batchEvent):
        text = batchEvent.data
        self.textCtrl.AppendText(text)

    def onBatchFinished(self, event):
        self.btnOk.Enable()
        self.btnCancel.Disable()

ITEM_BATCH_EXPORT_ID = wx.NewId()

ITEM_EUI_ID = wx.NewId()
ITEM_EUI_LOAD_ID = wx.NewId()
ITEM_INF_ID = wx.NewId()
ITEM_INF_LOAD_ID = wx.NewId()
ITEM_GOOGLE_CALENDAR_ID = wx.NewId()
ITEM_RFC5545_ID = wx.NewId()

ITEM_HELP_ID = wx.NewId()
ITEM_GPL_ID = wx.NewId()
ITEM_ABOUT_ID = wx.NewId()

BTN_LOAD_ID = wx.NewId()
BTN_EXPORT_ID = wx.NewId()
TXT_INFO_STRING_ID = wx.NewId()
TREE_CTRL_STUD_ID = wx.NewId()
TREE_CTRL_DOZ_ID = wx.NewId()

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.notebook_1 = wx.Notebook(self, -1, style=wx.NB_BOTTOM)
        self.notebook_1_pane_2 = wx.Panel(self.notebook_1, -1)
        self.notebook_1_pane_1 = wx.Panel(self.notebook_1, -1)
        self.panel_1 = wx.Panel(self, -1)
        
        # Menu Bar
        self.menuBar = wx.MenuBar()

        menu = wx.Menu()
        menu.Append(ITEM_BATCH_EXPORT_ID, u"für alle Semestergruppen und Dozenten exportieren", "", wx.ITEM_NORMAL)
        self.menuBar.Append(menu, "Batch")

        menu = wx.Menu()
        menu.Append(ITEM_EUI_ID, "Elektrotechnik und Informatik", "", wx.ITEM_NORMAL)
        menu.Append(ITEM_EUI_LOAD_ID, "            -> direkt einlesen", "", wx.ITEM_NORMAL)
        menu.Append(ITEM_INF_ID, "Informatik", "", wx.ITEM_NORMAL)
        menu.Append(ITEM_INF_LOAD_ID, "            -> direkt einlesen", "", wx.ITEM_NORMAL)
        menu.AppendSeparator()
        menu.Append(ITEM_GOOGLE_CALENDAR_ID, "Google Calendar", "", wx.ITEM_NORMAL)
        menu.AppendSeparator()
        menu.Append(ITEM_RFC5545_ID, "iCalendar rfc5545", "", wx.ITEM_NORMAL)
        self.menuBar.Append(menu, "Links")

        menu = wx.Menu()
        menu.Append(ITEM_HELP_ID, "Anleitung", "", wx.ITEM_NORMAL)
        menu.Append(ITEM_GPL_ID, "GPL", "", wx.ITEM_NORMAL)
        menu.Append(ITEM_ABOUT_ID, "About", "", wx.ITEM_NORMAL)
        self.menuBar.Append(menu, "Hilfe")

        self.SetMenuBar(self.menuBar)

        # frame pane
        self.button_Load = wx.Button(self, BTN_LOAD_ID, "HAW-Kalender einlesen")
        self.button_Export = wx.Button(self, BTN_EXPORT_ID, "Termin-Auswahl als iCalendar exportieren")
        self.infoString = wx.StaticText(self.panel_1, TXT_INFO_STRING_ID, "      Bitte eine HAW-Kalender Textdatei einlesen                    ")
        self.treeCtrl_Stud = wx.TreeCtrl(self.notebook_1_pane_1, TREE_CTRL_STUD_ID, style=wx.TR_HIDE_ROOT|wx.TR_HAS_BUTTONS|wx.TR_NO_LINES|wx.TR_DEFAULT_STYLE|wx.SUNKEN_BORDER|wx.TR_MULTIPLE)
        self.treeCtrl_Doz = wx.TreeCtrl(self.notebook_1_pane_2, TREE_CTRL_DOZ_ID, style=wx.TR_HIDE_ROOT|wx.TR_HAS_BUTTONS|wx.TR_NO_LINES|wx.TR_DEFAULT_STYLE|wx.SUNKEN_BORDER|wx.TR_MULTIPLE)

        self.__doLayout()
        self.__doFrameBindings()
        self.__doMenuBindings()

        self.menuItem_AlleSemUndDoz = self.menuBar.FindItemById(ITEM_BATCH_EXPORT_ID)
        self.menuItem_AlleSemUndDoz.Enable(False)

        self.space = "      "

    def __doLayout(self):
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_2 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_5 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4.Add(self.button_Load, 0, 0, 0)
        sizer_4.Add(self.button_Export, 0, 0, 0)
        sizer_5.Add(self.infoString, 0, wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL, 0)
        self.panel_1.SetSizer(sizer_5)
        sizer_4.Add(self.panel_1, 1, wx.EXPAND|wx.ALIGN_RIGHT, 0)
        sizer_1.Add(sizer_4, 0, 0, 0)
        sizer_2.Add(self.treeCtrl_Stud, 1, wx.EXPAND, 0)
        self.notebook_1_pane_1.SetSizer(sizer_2)
        sizer_3.Add(self.treeCtrl_Doz, 1, wx.EXPAND, 0)
        self.notebook_1_pane_2.SetSizer(sizer_3)
        self.notebook_1.AddPage(self.notebook_1_pane_1, "Studentensicht")
        self.notebook_1.AddPage(self.notebook_1_pane_2, "Dozentensicht")
        sizer_1.Add(self.notebook_1, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        sizer_1.Fit(self)
        self.Layout()

    def __doFrameBindings(self):
        self.button_Load.Bind(wx.EVT_BUTTON, self.onButton_Load)
        self.button_Export.Bind(wx.EVT_BUTTON, self.onButton_Export)
        self.button_Export.Disable()
        self.treeCtrl_Stud.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.onDoubleClick_Stud)
        self.treeCtrl_Doz.Bind(wx.EVT_TREE_ITEM_ACTIVATED, self.onDoubleClick_Doz)

    def __doMenuBindings(self):

        self.Bind(wx.EVT_MENU, self.onMenuItem_BatchStudUndDoz, id=ITEM_BATCH_EXPORT_ID)

        self.Bind(wx.EVT_MENU, self.onMenuItem_EuI, id=ITEM_EUI_ID)
        self.Bind(wx.EVT_MENU, self.onMenuItem_EuI_load, id=ITEM_EUI_LOAD_ID)
        self.Bind(wx.EVT_MENU, self.onMenuItem_Inf, id=ITEM_INF_ID)
        self.Bind(wx.EVT_MENU, self.onMenuItem_Inf_load, id=ITEM_INF_LOAD_ID)
        self.Bind(wx.EVT_MENU, self.onMenuItem_GoogleCalendar, id=ITEM_GOOGLE_CALENDAR_ID)
        self.Bind(wx.EVT_MENU, self.onMenuItem_rfc5545, id=ITEM_RFC5545_ID)

        self.Bind(wx.EVT_MENU, self.onMenuItem_Anleitung, id=ITEM_HELP_ID)
        self.Bind(wx.EVT_MENU, self.onMenuItem_GPL, id=ITEM_GPL_ID)
        self.Bind(wx.EVT_MENU, self.onMenuItem_About, id=ITEM_ABOUT_ID)

    def onButton_Load(self, event):
        dlg = wx.FileDialog(self, "txt-Version des Semesterplans auswählen")
        dlg.SetWildcard("nur Textdateien (*.txt)|*.txt|alle Dateien|*")

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            self.ctrl = Controller(inFileName=path, outFileName=None)
            self.infoString.SetLabel(self.space + "HAW-Kalender: " + self.ctrl.getInfoString())

            self.fillTrees()

        dlg.Destroy()

        self.updateExportButton()
        self.menuItem_AlleSemUndDoz.Enable()

    def fillTrees(self):

        def fillTree(treeCtrl):
            font = wx.Font(12, wx.MODERN, wx.NORMAL, wx.NORMAL, False, u'Courier New')
            treeCtrl.SetFont(font)

            groups = sorted(self.ctrl.getKeys())
            treeCtrl.DeleteAllItems()
            rootName = "root"
            rootName_unicode = rootName.decode("utf-8")
            root = treeCtrl.AddRoot(rootName_unicode)
            for key in groups:
                key_unicode = key.decode("utf-8")
                parent = treeCtrl.AppendItem(root, key_unicode)
                veranstaltungen = sorted(self.ctrl.getVeranstaltungen(key))

                maxLen = len(reduce(lambda x,y: max(x,y, key=len), veranstaltungen))
                formatter = "{0:<" + str(maxLen+3) + "}"

                for veranstaltung in veranstaltungen:
                    leftAlignedVeranstaltung = formatter.format(veranstaltung)
                    #FIXME: dirty hack (a 'Ü' is represented in utf-8 by 2 byte)
                    if 'Ü' in leftAlignedVeranstaltung:
                        leftAlignedVeranstaltung += " "
                    s = leftAlignedVeranstaltung + self.ctrl.tryGetFullName(veranstaltung)
                    s_unicode = s.decode("utf-8")
                    treeCtrl.AppendItem(parent, s_unicode)

        self.ctrl.tupleKeyIndex = DOZENT
        fillTree(self.treeCtrl_Doz)

        self.ctrl.tupleKeyIndex = self.ctrl.optimalGruppenKeyIndex()
        fillTree(self.treeCtrl_Stud)

    def onButton_Export(self, event):
        style = wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT
        dlg = wx.FileDialog(self, message="iCalendar (.ics) speichern unter", style=style)
        dlg.SetWildcard("iCalendar-Dateien (*.ics)|*.ics")

        if dlg.ShowModal() == wx.ID_OK:

            path = dlg.GetPath()
            if not path.endswith(".ics"):
                path = path + ".ics"

            self.ctrl.setOutFileName(path)
            self.ctrl.writeIcalendar()

        dlg.Destroy()

    def onDoubleClick_Stud(self, wxTreeEvent):
        self.ctrl.tupleKeyIndex = self.ctrl.optimalGruppenKeyIndex()
        self.onDoubleClick(wxTreeEvent, self.treeCtrl_Stud)

    def onDoubleClick_Doz(self, wxTreeEvent):
        self.ctrl.tupleKeyIndex = DOZENT
        self.onDoubleClick(wxTreeEvent, self.treeCtrl_Doz)
        
    def onDoubleClick(self, wxTreeEvent, treeCtrl):
        itemId = wxTreeEvent.GetItem()

        text_unicode = treeCtrl.GetItemText(itemId)
        text_utf8 = text_unicode.encode("utf-8")

        isVeranstaltung = not treeCtrl.ItemHasChildren(itemId)

        if not isVeranstaltung:
            key = text_utf8
            veranstaltungen = self.ctrl.getVeranstaltungen(key)
            if self.groupFullSelected(key):
                self.ctrl.unselectVeranstaltungen(veranstaltungen)
            else:
                self.ctrl.selectVeranstaltungen(veranstaltungen)
        else:
            veranstaltung = text_utf8.split("   ")[0] #FIXME: dirty
            if veranstaltung in self.ctrl.selectedVeranstaltungen:
                    self.ctrl.selectedVeranstaltungen.remove(veranstaltung)
            else: 
                self.ctrl.selectedVeranstaltungen.add(veranstaltung)

        self.updateTrees()
        self.updateExportButton()

    def updateTrees(self):
        def updateTree(treeCtrl):
            for keyItemId in iterChildren(treeCtrl, treeCtrl.GetRootItem()):

                allSelected = True
                for veranstItemId in iterChildren(treeCtrl, keyItemId):

                    text_unicode = treeCtrl.GetItemText(veranstItemId)
                    veranstaltung = text_unicode.encode("utf-8").split("   ")[0] #FIXME: dirty

                    if not veranstaltung in self.ctrl.selectedVeranstaltungen:
                        treeCtrl.SetItemBold(veranstItemId, False)
                        allSelected = False
                    else:
                        treeCtrl.SetItemBold(veranstItemId)

                treeCtrl.SetItemBold(keyItemId, allSelected)

            treeCtrl.Refresh()

        updateTree(self.treeCtrl_Stud)
        updateTree(self.treeCtrl_Doz)

    def updateExportButton(self):
        if len(self.ctrl.selectedVeranstaltungen) > 0:
            self.button_Export.Enable()
        else:
            self.button_Export.Disable()

    def groupFullSelected(self, key):
        return (self.ctrl.selectedVeranstaltungen & set(self.ctrl.getVeranstaltungen(key)) == set(self.ctrl.getVeranstaltungen(key)))

    def onMenuItem_BatchStudUndDoz(self, event):

        dlg = wx.DirDialog(self, "Verzeichnis für Batch-Export auswählen")

        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            dlg.Destroy()

            batchCtrl = copy.deepcopy(self.ctrl)

            dlg = RunningBatchExportDialog(parent=self,
                                           text="Batch-Export gestartet:\n\n",
                                           title="Batch-Export",
                                           ctrl=batchCtrl,
                                           path=path)
            dlg.ShowModal() 
            dlg.Destroy()

    def onMenuItem_EuI(self, event):
        webbrowser.open(STUNDENPLAN_SITE_EuI, autoraise=True)

    def onMenuItem_EuI_load(self, event):
        try:
            sys.stdin = urllib.urlopen(STUNDENPLAN_URL_EuI)
            self.ctrl = Controller(inFileName=None, outFileName=None)
            self.infoString.SetLabel(self.space + "HAW-Kalender: " + self.ctrl.getInfoString())
            self.fillTrees()

            self.updateExportButton()

            self.menuItem_AlleSemUndDoz.Enable()

        except IOError as e:
            print "Could not open EuI-url: " + str(e)

    def onMenuItem_Inf(self, event):
        webbrowser.open(STUNDENPLAN_SITE_Inf, autoraise=True)

    def onMenuItem_Inf_load(self, event):
        try:
            sys.stdin = urllib.urlopen(STUNDENPLAN_URL_Inf)
            self.ctrl = Controller(inFileName=None, outFileName=None)
            self.infoString.SetLabel(self.space + "HAW-Kalender: " + self.ctrl.getInfoString())
            self.fillTrees()

            self.updateExportButton()

            self.menuItem_AlleSemUndDoz.Enable()

        except IOError as e:
            print "Couldn't open Inf-url: " + str(e)

    def onMenuItem_GoogleCalendar(self, event):
        webbrowser.open("http://www.google.com/calendar", autoraise=True)

    def onMenuItem_rfc5545(self, event):
        webbrowser.open("http://tools.ietf.org/html/rfc5545/", autoraise=True)

    def onMenuItem_Anleitung(self, event):

        text_unicode = texts.anleitung.decode("utf-8")

        dlg = ScrollableDialog(None, text_unicode, title="Anleitung")
        dlg.ShowModal()
        dlg.Destroy()

    def onMenuItem_GPL(self, event):

        text = texts.gpl
        text = " " + text.replace("\n", "\n ")
        text_unicode = text.decode("utf-8")

        dlg = ScrollableDialog(self, text_unicode, title="GPL")
        dlg.ShowModal()
        dlg.Destroy()

    def onMenuItem_About(self, event):

        text = texts.version + "\n\n" + texts.homepage + "\n\n" + texts.about
        text_unicode = text.decode("utf-8")

        dlg = wx.MessageDialog(self, text_unicode, caption="About", style=wx.OK)
        dlg.ShowModal()
        dlg.Destroy()


if __name__ == '__main__':

    # create a logfile only when warnings or errors occur
    logging.basicConfig(level=logging.WARNING)
    handler = logging.FileHandler(filename="haw2iCalendar-klickiBunti.log", delay=True)
    formatter = logging.Formatter('%(asctime)s %(levelname)-8s %(message)s')
    handler.setFormatter(formatter)
    logging.getLogger("").addHandler(handler) #add handler to the root logger

    app = wx.App()
    frame = MyFrame(parent=None, id=-1, title="haw2iCalendar")
    frame.SetSize(wx.Size(900,800))
    frame.Show()
    app.MainLoop()

