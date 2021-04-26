import sys
import os

from PyQt5 import QtWidgets,QtGui,QtCore
from PyQt5.QtCore import pyqtSignal,pyqtSlot,QObject

from Ui_about import *

class AboutWin(QtWidgets.QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.ui=Ui_Form()
        self.a = self.ui.setupUi(self)
        self.windowCenter()


    def windowCenter(self):
    #使窗口居中
        screen = QtWidgets.QApplication.desktop()
        size = self.geometry()
        self.move((screen.width() - size.width())/2,(screen.height() - size.height())/2) 

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = AboutWin()
    main.show()

    sys.exit(app.exec_())
    

if __name__ == "__main__":
    main()
