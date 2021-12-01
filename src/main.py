import sys
import src.audio
import pyqtgraph

import utils
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QPushButton, QLineEdit, QPlainTextEdit


class MainWindow(QtWidgets.QMainWindow):
    infoPTE: QPlainTextEdit
    analyzePB: QPushButton
    linkLE: QLineEdit

    def __init__(self):

        super(MainWindow, self).__init__()  # Call the inherited classes __init__ method
        uic.loadUi(utils.currentDir(__file__, 'gui.ui'), self)  # Load the .ui file
        self.analyzePB.clicked.connect(self.onAnalyze)
        self.win = pyqtgraph.GraphicsWindow(title="Signal from serial port")  # creates a window
        self.p = self.win.addPlot(title="Realtime plot")  # creates empty space for the plot in the window
        self.curve = self.p.plot()
        self.audio=src.audio.AudioFile(self.curve)
        self.audio.play()


    def onAnalyze(self):
        print("test")
        link=self.linkLE.text()
        print(link)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    #mainWindow.show()
    app.exec()
