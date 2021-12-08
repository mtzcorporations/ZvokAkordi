import sys
import time

import numpy
import scipy.signal as s
from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QPushButton, QLineEdit, QPlainTextEdit, QSlider
from pyqtgraph import PlotWidget, mkPen

import utils
from src.audio import Audio, findPeak, getNote, vectorDistance


class MainWindow(QtWidgets.QMainWindow):
    infoPTE: QPlainTextEdit
    analyzePB: QPushButton
    linkLE: QLineEdit
    plotW: PlotWidget
    changeW: PlotWidget
    thresholdS: QSlider
    stopPB: QPushButton

    def __init__(self):
        super(MainWindow, self).__init__()  # Call the inherited classes __init__ method
        uic.loadUi(utils.currentDir(__file__, 'gui.ui'), self)  # Load the .ui file
        self.analyzePB.clicked.connect(self.onAnalyze)
        self.stopPB.clicked.connect(self.onStop)
        self.audio=Audio()
        #self.audio.play()

        #init for graphs
        self.fitItem = self.plotW.getPlotItem()
        self.thresholdItem = self.changeW.getPlotItem()
        self.changeItem = self.changeW.getPlotItem()
        self.specItem = self.plotW.getPlotItem()
        self.specItem.setMouseEnabled(y=False)
        self.specItem.setYRange(0, 2000)
        self.specItem.setXRange(60, 10000, padding=0)
        self.specAxis = self.specItem.getAxis("bottom")
        self.specAxis.setLabel("Frequency [Hz]")

        # timer which repate function `display_time` every 1000ms (1s)
        self.timer = QTimer()
        self.timer.timeout.connect(self.updateGraph)  # execute `display_time`
        self.timer.setInterval(1000/60)  # 1000ms = 1s
        self.timer.start()

        self.history = []
        self.changes = []
        self.note = []
        self.start = 0
        self.timeStamps = []

        self.bigChange = False
    def onStop(self) :
        # MIDI   poračunaš frekvence in timestampa da ustvariš midi
        pass
    def updateGraph(self):
        try:
            data = self.audio.readData()
        except IOError:
            return
        # spekter
        f, Pxx = self.audio.get_spectrum(data)
        # poračunam razdalje med trenutnim vektorjem in prejšnjim
        if (len(self.history) > 1):
            distance = vectorDistance(Pxx, self.history[-1])
            # če pride do dovolj velike spremembe, dodama noto
            if len(self.changes) > 1:
                if (self.changes[-1] < self.thresholdS.value() and distance > self.thresholdS.value()):
                    self.bigChange = True
            self.changes.append(distance)
        self.history.append(Pxx)


        self.changeItem.plot(y=self.changes, clear=True)
        self.thresholdItem.plot(x=[0,len(self.changes)-1],y=[self.thresholdS.value(),self.thresholdS.value()], clear=False,pen=mkPen('r', width=1))
        self.specItem.plot(x=f, y=Pxx, clear=False)
        info = findPeak(f, Pxx)
        if info is not None:
            self.fitItem.plot(x=info[1], y=info[2], clear=True, pen=mkPen('r', width=3))
            if self.bigChange:
                t=round(time.time() - self.start,2)
                self.recordNote(info[0],t)
                self.printInfo()
                self.bigChange = False
        else:
            self.specItem.plot(x=f, y=Pxx, clear=True)


    def recordNote(self,peakFreq,t):
        note = getNote(peakFreq)

        ## poglej če se ton obdrži dovolj časa vpiši, če se menja --> TODO
        if len(self.note) > 0:
            self.note.append(note)
            self.timeStamps.append(t)
        else:
            self.note.append(note)
            self.timeStamps.append(t)

    def printInfo(self):
        z= zip(self.note,self.timeStamps)
        self.infoPTE.setPlainText(f""" 
        Vse Note {list(z)}
        """)

    def onAnalyze(self):
        #print("test")
        link=self.linkLE.text()
        self.note = []
        self.infoPTE.setPlainText(f"""""")
        self.history = []
        self.changes = []
        self.start=time.time()
        self.timeStamps = []
        #print(link)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    app.exec()

