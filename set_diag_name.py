import sys
import os

from PyQt5 import QtWidgets,QtGui,QtCore
from PyQt5.QtCore import pyqtSignal,pyqtSlot,QObject

from Ui_diag_names import *
from dabaseTool import *

class SetDiagNameWin(QtWidgets.QWidget):
    signalClose = pyqtSignal(bool)
    def __init__(self,parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.a = self.ui.setupUi(self)
        self.windowCenter()
        self.fillInTheDiagnosis()
        self.sigToSlot()

    def emitSign(self):
        self.signalClose.emit(True)

    def sigToSlot(self):
        self.ui.pushButton_2.clicked.connect(self.addDiagnosis)
        self.ui.pushButton_3.clicked.connect(self.delDiagnosis)
        self.ui.pushButton.clicked.connect(self.saveTheNewDiagnosis)

    def windowCenter(self):
    #使窗口居中
        screen = QtWidgets.QApplication.desktop()
        size = self.geometry()
        self.move((screen.width() - size.width())/2,(screen.height() - size.height())/2) 
    
    def fillInTheDiagnosis(self):

        a = Parameters()
        b = a.read_diagnosis()
        c = list(dict.values(b))
        self.ui.tableWidget.setRowCount(len(c))
        self.ui.tableWidget.setColumnCount(1)
        self.ui.tableWidget.setColumnWidth(0,290)
        for i in range(len(c)):
            print(c[i])
            d = QtWidgets.QTableWidgetItem(c[i])
            self.ui.tableWidget.setItem(i,0,d)

    def addDiagnosis(self):
        #添加诊断
        nowRow = self.ui.tableWidget.currentRow()
        self.ui.tableWidget.insertRow(nowRow+1)
    def delDiagnosis(self):
        #删除诊断
        a = self.ui.tableWidget.currentRow()
        self.ui.tableWidget.removeRow(a)
    def saveTheNewDiagnosis(self):
        a = self.ui.tableWidget.rowCount()
        diagnosis = []
        diagnosisDict = {}
        for i in range(a):
            c = self.ui.tableWidget.item(i,0)
            if c !=None and c.text() !='':
                diagnosis.append(c.text())
        for n in range(len(diagnosis)):
            diagnosisDict[n]=diagnosis[n]
        print(diagnosisDict)
        try:
            delete = Parameters().delete_diagnosis()
            rewrite = Parameters().refresh_diagnosis_values(diagnosisDict)
            QtWidgets.QMessageBox.information(self,'保存成功','更新诊断名称成功！')
            self.emitSign()
            self.close()

        except :
            QtWidgets.QMessageBox.warning(self,'保存诊断错误','删除原诊断名称和保存新诊断名称过程错误！')



  

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = SetDiagNameWin()
    main.show()

    sys.exit(app.exec_())
    

if __name__ == "__main__":
    main()