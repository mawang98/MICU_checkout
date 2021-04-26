import sys
import os

from PyQt5 import QtWidgets,QtGui,QtCore
from PyQt5.QtCore import pyqtSignal,pyqtSlot,QObject

from Ui_towhere_set import *
from dabaseTool import *

class SetTowhereWin(QtWidgets.QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.a = self.ui.setupUi(self)
        self.windowCenter()
        self.fillInTheTowhere()
        self.sigToSlot()
    
    def sigToSlot(self):
        self.ui.pushButton_2.clicked.connect(self.addTowhere)
        self.ui.pushButton_3.clicked.connect(self.delTowhere)
        self.ui.pushButton.clicked.connect(self.saveTheNewTowhere)

    def windowCenter(self):
    #使窗口居中
        screen = QtWidgets.QApplication.desktop()
        size = self.geometry()
        self.move((screen.width() - size.width())/2,(screen.height() - size.height())/2) 
    
    def fillInTheTowhere(self):
        a = Parameters()
        b = a.read_towhere()
        c = list(dict.values(b))
        print(c)
        self.ui.tableWidget.setColumnCount(1)
        self.ui.tableWidget.setRowCount(len(c))
        self.ui.tableWidget.setColumnWidth(0,290)
        for i in range(len(c)):
            d = QtWidgets.QTableWidgetItem(c[i])
            self.ui.tableWidget.setItem(i,0,d)

    def addTowhere(self):
        #添加诊断
        self.ui.tableWidget.setRowCount(self.ui.tableWidget.rowCount()+1)
    def delTowhere(self):
        #删除诊断
        a = self.ui.tableWidget.currentRow()
        self.ui.tableWidget.removeRow(a)
    def saveTheNewTowhere(self):
        a = self.ui.tableWidget.rowCount()
        towhere = []
        towhereDict = {}
        for i in range(a):
            c = self.ui.tableWidget.item(i,0)
            print(c)
            if c !=None and c.text() !='':
                towhere.append(c.text())
        for n in range(len(towhere)):
            towhereDict[n]=towhere[n]
        print(TtreDict)
        try:
            delete = Parameters().delete_towhere()
            rewrite = Parameters().refresh_towhere_values(towhereDict)
            QtWidgets.QMessageBox.information(self,'保存成功','更新患者归属设置成功！')
            self.close()

        except :
            QtWidgets.QMessageBox.warning(self,'保存诊断错误','删除原患者归属和保存新患者归属过程错误！')

  

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = SetTowhereWin()
    main.show()

    sys.exit(app.exec_())
    

if __name__ == "__main__":
    main()