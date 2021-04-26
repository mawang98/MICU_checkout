import sys
import os

from PyQt5 import QtWidgets,QtGui,QtCore
from PyQt5.QtCore import pyqtSignal,pyqtSlot,QObject

from Ui_beds_set import *
from dabaseTool import *

class SetBedsWin(QtWidgets.QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.a = self.ui.setupUi(self)
        self.windowCenter()
        self.fillInTheBeds()
        self.sigToSlot()
    
    def sigToSlot(self):
        self.ui.pushButton_2.clicked.connect(self.addBeds)
        self.ui.pushButton_3.clicked.connect(self.delBeds)
        self.ui.pushButton.clicked.connect(self.saveTheNewBeds)

    def windowCenter(self):
    #使窗口居中
        screen = QtWidgets.QApplication.desktop()
        size = self.geometry()
        self.move((screen.width() - size.width())/2,(screen.height() - size.height())/2) 
    
    def fillInTheBeds(self):
        a = Parameters()
        b = a.read_beds()
        c = list(dict.values(b))
        print(c)
        self.ui.tableWidget.setColumnCount(1)
        self.ui.tableWidget.setRowCount(len(c))
        self.ui.tableWidget.setColumnWidth(0,290)
        for i in range(len(c)):
            d = QtWidgets.QTableWidgetItem(c[i])
            self.ui.tableWidget.setItem(i,0,d)

    def addBeds(self):
        #添加诊断
        self.ui.tableWidget.setRowCount(self.ui.tableWidget.rowCount()+1)
    def delBeds(self):
        #删除诊断
        a = self.ui.tableWidget.currentRow()
        self.ui.tableWidget.removeRow(a)
    def saveTheNewBeds(self):
        a = self.ui.tableWidget.rowCount()
        beds = []
        bedsDict = {}
        for i in range(a):
            c = self.ui.tableWidget.item(i,0)
            if c !=None and c.text()!= '':
                beds.append(c.text())
        for n in range(len(beds)):
            bedsDict[n]=beds[n]
        print(bedsDict)
        try:
            delete = Parameters().delete_beds()
            rewrite = Parameters().refresh_beds_values(bedsDict)
            QtWidgets.QMessageBox.information(self,'保存成功','更新床位成功！')
            self.close()

        except :
            QtWidgets.QMessageBox.warning(self,'保存诊断错误','删除原床位和保存新床位过程错误！')

  

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = SetBedsWin()
    main.show()

    sys.exit(app.exec_())
    

if __name__ == "__main__":
    main()