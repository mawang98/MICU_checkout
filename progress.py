import time
import sys
from PyQt5 import QtWidgets,QtGui,QtCore
from PyQt5.QtCore import pyqtSignal,pyqtSlot,QObject

from icucheckOut_sqlite3 import CheckinOut

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    splah = QtWidgets.QSplashScreen(QtGui.QPixmap('./first.png'))
    splah.show()
    app.processEvents()
    mainWin = CheckinOut()
    mainWin.show()
    splah.finish(mainWin)
    sys.exit(app.exec_())


