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
        self.fitItem = self.specWid.getPlotItem()
        self.specItem = self.specWid.getPlotItem()
        self.specItem.setMouseEnabled(y=False)
        self.specItem.setYRange(0,2000)
        self.specItem.setXRange(60, 10000, padding=0)

        self.specAxis = self.specItem.getAxis("bottom")
        self.specAxis.setLabel("Frequency [Hz]")
        self.lay.addWidget(self.specWid)

        self.mainWindow.show()
        self.app.aboutToQuit.connect(self.close)

    def close(self):
        self.audio.stream.close()
        sys.exit()

    def mainLoop(self):
        while 1:
            # Sometimes Input overflowed because of mouse events, ignore this
            try:
                data = self.audio.readData()
            except IOError:
                continue
            f, Pxx = self.audio.get_spectrum(data)
            info=findPeak(f,Pxx)
            if info is not None:
                self.fitItem.plot(x=info[1], y=info[2], clear=True, pen=mkPen('r', width=3))
                self.specItem.plot(x=f,y=Pxx, clear=False)
            else:
                self.specItem.plot(x=f, y=Pxx, clear=True)
            QtGui.QApplication.processEvents()

if __name__ == '__main__':
    sa = SpectrumAnalyzer()
    sa.mainLoop()
