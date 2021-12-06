import sys

from PyQt5 import QtWidgets, uic
from PyQt5.QtCore import QTimer
from PyQt5.QtWidgets import QPushButton, QLineEdit, QPlainTextEdit
from pyqtgraph import PlotWidget, mkPen

import utils
from src.audio import Audio, findPeak, getNote


class MainWindow(QtWidgets.QMainWindow):
    infoPTE: QPlainTextEdit
    analyzePB: QPushButton
    linkLE: QLineEdit
    plotW: PlotWidget

    def __init__(self):
        super(MainWindow, self).__init__()  # Call the inherited classes __init__ method
        uic.loadUi(utils.currentDir(__file__, 'gui.ui'), self)  # Load the .ui file
        self.analyzePB.clicked.connect(self.onAnalyze)
        self.audio=Audio()
        #self.audio.play()

        #init for graphs
        self.fitItem = self.plotW.getPlotItem()
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

    def updateGraph(self):
        #print("test Update")
        try:
            data = self.audio.readData()
        except IOError:
            return
        f, Pxx = self.audio.get_spectrum(data)
        info = findPeak(f, Pxx)
        if info is not None:
            self.fitItem.plot(x=info[1], y=info[2], clear=True, pen=mkPen('r', width=3))
            self.specItem.plot(x=f, y=Pxx, clear=False)
            self.printNote(info[0])
        else:
            self.specItem.plot(x=f, y=Pxx, clear=True)

    def printNote(self,peakFreq):
        note = getNote(peakFreq)
        self.infoPTE.setPlainText(f"""
        Max f: {round(peakFreq,0)} Hz
        Nota : {note} """)
    def onAnalyze(self):
        print("test")
        link=self.linkLE.text()
        print(link)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    app.exec()

