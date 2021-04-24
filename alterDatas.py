import sys
import json
import csv
import os
import datetime
from openpyxl import Workbook

from PyQt5 import QtWidgets,QtGui,QtCore
from PyQt5.QtCore import pyqtSignal,pyqtSlot,QObject
from PyQt5.QtWidgets import QAbstractItemView

from Ui_alterData import *

from diagnosis import *
from dabaseTool import *


class AlterDatas(QtWidgets.QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.a = self.ui.setupUi(self)
        self.windowCenter()
        self.initSet()
        self.signalToSlot()

    def windowCenter(self):
    #使窗口居中
        screen = QtWidgets.QApplication.desktop()
        size = self.geometry()
        self.move((screen.width() - size.width())/2,(screen.height() - size.height())/2) 

    def initSet(self):
        self.icuBedsDic={0:'1',1:'2',2:'3',3:'4',4:'5',5:'6',6:'7',7:'8',8:'9',9:'10',10:'11',11:'12',12:'13',13:'14',14:'15',15:'16',16:'17',18:'18',19:'19',20:'20',21:'21',22:'22',23:'23',24:'24',25:'25',26:'26',27:'27',28:'J1',29:'J2',30:'J3'}
        self.fromWhereDic = {0:'急诊',1:'外科转入',2:'外科转入',3:'外科术后转入',4:'重症普通病房转入'}
        self.toWhereDic = {0:'自动出院',1:'死亡',2:'转外科',3:'转内科'}        
        try:
            ParametersFormDatabase = self.getParameterValues()
            self.icuBedsDic=ParametersFormDatabase[0]
            self.fromWhereDic = ParametersFormDatabase[1]
            self.toWhereDic = ParametersFormDatabase[2]
        except:
            QtWidgets.QMessageBox.warning(self,'参数设置读取错误','参数设置读取错误,使用默认参数。')
        self.icuBeds = dict.values(self.icuBedsDic)        
        self.fromWhere = dict.values(self.fromWhereDic)
        self.toWhere = dict.values(self.toWhereDic)
        self.ui.comboBox_5.addItems(self.icuBeds)  
        self.ui.comboBox_7.addItems(self.fromWhere)
        self.ui.comboBox_6.addItems(self.toWhere)
        self.ui.label_5.setStyleSheet('color:red')

    def signalToSlot(self):
        self.ui.pushButton_6.clicked.connect(self.diagWin) 
        self.ui.checkBox_2.toggled.connect(self.deleteButtonAction)       

    def getParameterValues(self):
        #获取三个comboBox设置参数
        a = Parameters().read_beds()
        b = Parameters().read_fromwhere()
        c = Parameters().read_towhere()
        return(a,b,c)
    def diagWin(self):
        self.d = DiagnosisWin()
        self.d.show()
        self.d.ui.textEdit.setText(self.ui.textEdit.toPlainText()) #将目前诊断填入诊断窗口
        self.d.ui.pushButton_2.clicked.connect(self.d.emit_diag)
        self.d.diagnosis.connect(self.slot_ckdiag_write)

    def slot_ckdiag_write(self,diag):   
    #槽函数插入诊断编辑窗口的内容 
        self.ui.textEdit.clear()               
        self.ui.textEdit.insertPlainText(diag)
    
    def deleteButtonAction(self):
        #删除键的激活和失活
        if self.ui.checkBox_2.isChecked():
            self.ui.pushButton_4.setEnabled(True)
        else:
            self.ui.pushButton_4.setEnabled(False)


def main():
    app = QtWidgets.QApplication(sys.argv)
    main = AlterDatas()
    main.show()
    sys.exit(app.exec_())
    

if __name__ == "__main__":
    main()