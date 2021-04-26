import sys
import os

from PyQt5 import QtWidgets,QtGui,QtCore
from PyQt5.QtCore import pyqtSignal,pyqtSlot,QObject

from Ui_fromwhere_set import *
from dabaseTool import *

class SetFromwhereWin(QtWidgets.QWidget):
    signalClose = pyqtSignal(bool)
    def __init__(self,parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.a = self.ui.setupUi(self)
        self.windowCenter()
        self.fillInTheFromwhere()
        self.sigToSlot()

    def emitSign(self):
        self.signalClose.emit(True)

    def sigToSlot(self):
        self.ui.pushButton_2.clicked.connect(self.addFromwhere)
        self.ui.pushButton_3.clicked.connect(self.delFromwhere)
        self.ui.pushButton.clicked.connect(self.saveTheNewFromwhere)

    def windowCenter(self):
    #使窗口居中
        screen = QtWidgets.QApplication.desktop()
        size = self.geometry()
        self.move((screen.width() - size.width())/2,(screen.height() - size.height())/2) 
    
    def fillInTheFromwhere(self):
        a = Parameters()
        b = a.read_fromwhere()
        c = list(dict.values(b))
        print(c)
        self.ui.tableWidget.setColumnCount(1)
        self.ui.tableWidget.setRowCount(len(c))
        self.ui.tableWidget.setColumnWidth(0,290)
        for i in range(len(c)):
            d = QtWidgets.QTableWidgetItem(c[i])
            self.ui.tableWidget.setItem(i,0,d)

    def addFromwhere(self):
        #添加
        nowRow = self.ui.tableWidget.currentRow()
        self.ui.tableWidget.insertRow(nowRow+1)
    def delFromwhere(self):
        #删除诊断
        a = self.ui.tableWidget.currentRow()
        self.ui.tableWidget.removeRow(a)
    def saveTheNewFromwhere(self):
        a = self.ui.tableWidget.rowCount()
        fromwhere = []
        fromwhereDict = {}
        for i in range(a):
            c = self.ui.tableWidget.item(i,0)
            print(c)
            if c !=None and c.text() !='':
                fromwhere.append(c.text())
        for n in range(len(fromwhere)):
            fromwhereDict[n]=fromwhere[n]
        print(fromwhereDict)
        try:
            delete = Parameters().delete_fromwhere()
            rewrite = Parameters().refresh_fromwhere_values(fromwhereDict)
            QtWidgets.QMessageBox.information(self,'保存成功','更新患者来源成功！')
            self.emitSign()
            self.close()

        except :
            QtWidgets.QMessageBox.warning(self,'保存诊断错误','删除原患者来源和保存新患者来源过程错误！')

  

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = SetFromwhereWin()
    main.show()

    sys.exit(app.exec_())
    

if __name__ == "__main__":
    main()