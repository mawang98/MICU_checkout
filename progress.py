import time
import sys
from PyQt5 import QtWidgets,QtGui,QtCore
from PyQt5.QtCore import pyqtSignal,pyqtSlot,QObject

from icucheckOut_sqlite3 import CheckinOut

if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)
    splah = QtWidgets.QSplashScreen(QtGui.QPixmap('./first.png'))
    splah.showMessage('程序加载中......')
    splah.show()
    app.processEvents()
    mainWin = CheckinOut()
    time.sleep(5)
    mainWin.show()
    splah.finish(mainWin)
    sys.exit(app.exec_())