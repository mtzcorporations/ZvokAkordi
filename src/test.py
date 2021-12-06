import sys

import pyqtgraph as pg
from pyqtgraph import mkPen
from pyqtgraph.Qt import QtGui

# Audio Format (check Audio MIDI Setup if on Mac)
from src.audio import findPeak, Audio


class SpectrumAnalyzer():
    def __init__(self):
        self.audio=Audio()
        self.initUI()


    def initUI(self):
        self.app = QtGui.QApplication([])
        self.app.quitOnLastWindowClosed()

        self.mainWindow = QtGui.QMainWindow()
        self.mainWindow.setWindowTitle("Spectrum Analyzer")
        self.mainWindow.resize(800,300)
        self.centralWid = QtGui.QWidget()
        self.mainWindow.setCentralWidget(self.centralWid)
        self.lay = QtGui.QVBoxLayout()
        self.centralWid.setLayout(self.lay)

        self.specWid = pg.PlotWidget(name="spectrum")

        self.lay.addWidget(self.specWid)

        self.mainWindow.show()
        self.app.aboutToQuit.connect(self.close)

    def close(self):
        self.audio.stream.close()
        sys.exit()

    def mainLoop(self):
        while 1:
            # Sometimes Input overflowed because of mouse events, ignore this

            QtGui.QApplication.processEvents()

if __name__ == '__main__':
    sa = SpectrumAnalyzer()
    sa.mainLoop()
