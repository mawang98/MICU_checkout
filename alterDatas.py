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
    winclosed = pyqtSignal(bool)
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
        self.ui.label_5.setStyleSheet('color:red')
        self.ui.lineEdit.setValidator(QtGui.QIntValidator(0,100000000))
        self.ui.lineEdit_3.setValidator(QtGui.QIntValidator(0,100000000))

    def signalToSlot(self):
        self.ui.pushButton_6.clicked.connect(self.diagWin) 
        self.ui.checkBox_2.toggled.connect(self.deleteButtonAction)   
        self.ui.pushButton_5.clicked.connect(self.saveTheNewDatas)    
        self.ui.pushButton_4.clicked.connect(self.deleteThisPatientData)
    def emit_sig_close(self):
        #发送窗口关闭信号
        self.winclosed.emit(True)

    def diagWin(self):
        #调用诊断编辑器窗口
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

    def checkTheBlank(self):
        #检查数据完整性
        a = [1,1,1,1,1,1,1,1]  #设置8个必填项目初始为0
        b = []
        if self.ui.lineEdit_7.text()== '':
            a[0]=0  #患者来源
            b.append('患者来源')
        if self.ui.lineEdit.text() == '':
            a[1]=0  #住院号
            b.append('住院号')
        if self.ui.lineEdit_2.text() == '':
            a[2]=0  #姓名
            b.append('姓名')
        if self.ui.comboBox_2.currentText() =='':
            a[3]=0  #性别
            b.append('性别')
        if self.ui.lineEdit_3.text() == '':
            a[4]=0 #年龄
            b.append('年龄')
        if self.ui.lineEdit_8.text()== '':
            a[5]=0  #床位号
            b.append('床位号')
        if self.ui.lineEdit_9.text() == '':
            a[6]=0  #去向
            b.append('去向')
        if self.ui.textEdit.toPlainText() == '':
            a[7]=0  #诊断
            b.append('诊断')
        # print(a,b)
        sumlist = sum(a)
        if sumlist < 8:
            blanks = '存在空白的必填项目：'
            for i in b:
                blanks = blanks+i+','
            QtWidgets.QMessageBox.warning(self,'存在空白项目',blanks)
            return(False)
        else:
            return(True)
    def checkDate(self):
        #检查入出科日期逻辑正确性
        a = self.ui.dateEdit.date()
        b = self.ui.dateEdit_2.date()
        if a>b:
            QtWidgets.QMessageBox.warning(self,'日期错误','入科时间大于出科时间') 
            return(False) 
        else:
            return(True)   
    
    def saveTheNewDatas(self):
        #收集新数据 并 更新 数据库：

        icunum = int(self.ui.label_3.text()[-7:])
        self.fromWhere = self.ui.lineEdit_7.text()
        checkinTip = self.ui.lineEdit_4.text()
        checkinTime = self.ui.dateEdit.text()
        admNum = self.ui.lineEdit.text()
        patientName = self.ui.lineEdit_2.text()
        gender = self.ui.comboBox_2.currentText()
        age = self.ui.lineEdit_3.text()
        bedNum = self.ui.lineEdit_8.text()
        self.toWhere = self.ui.lineEdit_9.text()
        checkoutTip = self.ui.lineEdit_5.text()
        checkoutTime = self.ui.dateEdit_2.text()
        diagnosis = self.ui.textEdit.toPlainText()
        isSpecial = 1 if self.ui.checkBox.isChecked() else 0
        comment = self.ui.lineEdit_6.text()
        nowtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        patientDatas = (
            self.fromWhere,
            checkinTip,
            checkinTime,
            admNum,
            patientName,
            gender,
            age,
            bedNum,
            self.toWhere,
            checkoutTip,
            checkoutTime,
            diagnosis,
            isSpecial,
            comment,
            nowtime
        )
        ##########################################
        checkblank = self.checkTheBlank() #检查空项
        if checkblank:
            checkDate = self.checkDate() #检查日期逻辑
            if checkDate:
                confirmDatas = QtWidgets.QMessageBox.information(    #调用对话窗口确认保存数据
                    self,
                    '请确认修改','是否修改数据？',
                    QtWidgets.QMessageBox.Ok|QtWidgets.QMessageBox.Cancel)
                if confirmDatas == QtWidgets.QMessageBox.Ok:
                    self.updateTheNewDatas(icunum,patientDatas) 
                    QtWidgets.QMessageBox.information(self,'修改成功','数据修改成功')
                    self.emit_sig_close() #发送信号
                    self.close()                   
                else:
                    pass
        ##########################################
 
    def updateTheNewDatas(slef,icunum,patientDatas):
        #向数据库更新数据
        icunumA = icunum
        patientDatasA = patientDatas
        try:
            updateData = UpdateTableDischarge().updateDischargeValues(icunumA,patientDatasA)
        except :
            QtWidgets.QMessageBox.warning(self,'更新数据错误','更新数据失败！！')
    
    def deleteThisPatientData(self):
        icunum = int(self.ui.label_3.text()[-7:])
        confirm = QtWidgets.QMessageBox.warning(self,
        '请确认数据删除','数据删除后无法恢复，请确认删除该数据！',
        QtWidgets.QMessageBox.Ok|QtWidgets.QMessageBox.Cancel)
        if confirm == QtWidgets.QMessageBox.Ok:
            try:
                deleteData = DeletePatientData().deleteOnePatientData(icunum)
                QtWidgets.QMessageBox.information(self,'数据已删除','该条数据已成功删除')
                self.emit_sig_close()
                self.close()
            except :
                QtWidgets.QMessageBox.warning(self,'删除数据错误','从数据库删除数据错误')
        else:
            pass

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = AlterDatas()
    main.show()
    sys.exit(app.exec_())
    

if __name__ == "__main__":
    main()