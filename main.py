import sys
import utils
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QPushButton, QLineEdit, QTextEdit, QPlainTextEdit


class MainWindow(QtWidgets.QMainWindow):
    infoPTE: QPlainTextEdit
    analyzePB: QPushButton
    linkLE: QLineEdit



    def __init__(self):
        super(MainWindow, self).__init__()  # Call the inherited classes __init__ method
        uic.loadUi(utils.currentDir(__file__, 'gui.ui'), self)  # Load the .ui file
        self.analyzePB.clicked.connect(self.onAnalyze)

    def onAnalyze(self):
        print("test")
        link=self.linkLE.text()
        print(link)

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    app.exec()
