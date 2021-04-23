import sys
import json
import csv
import os
import datetime
from openpyxl import Workbook

from PyQt5 import QtWidgets,QtGui,QtCore
from PyQt5.QtCore import pyqtSignal,pyqtSlot,QObject

from  Ui_micuCheckOut import *
from  diagnosis import *

class CheckinOut(QtWidgets.QMainWindow):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.a = self.ui.setupUi(self)
        self.windowCenter()
        self.set_time()
        self.signalToSlot()
        self.initSet()
        # self.checkCsvFile()
        self.fillInTheList()
        # self.checkDate()
    
    def initSet(self):
        #各项初始设置
        icuBeds=['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','J1','J2','J3']
        fromWhere = ['急诊','外科转入','内科转入','外科术后转入','重症普通病房转入']
        toWhere = ['自动出院','死亡','转外科','转内科']
        self.firstrow=['ICU编码','病人来源','入科注释','入院时间','住院号','姓名','性别','年龄','床号','去向','去向备注','出科时间','诊断','重点病历标记','备注']
        self.ui.comboBox_5.addItems(icuBeds)  
        self.ui.comboBox_5.setCurrentIndex(-1)
        self.ui.comboBox_7.addItems(fromWhere)
        self.ui.comboBox_7.setCurrentIndex(-1)
        self.ui.comboBox_6.addItems(toWhere)
        self.ui.comboBox_6.setCurrentIndex(-1)
        self.ui.lineEdit_8.setValidator(QtGui.QIntValidator(0,100000000))
        self.ui.tableWidget.setColumnCount(len(self.firstrow))    #初始化检索结果表头并填入表头内容
        self.ui.tableWidget.setHorizontalHeaderLabels(self.firstrow)
    
    def checkCsvFile(self):
        #检查数据库文件datas.csv是否正常
        findCsv = 0
        for fileName in os.listdir():
            if fileName == 'datas.csv':
                findCsv = 1
            else:
                pass
        if findCsv == 0:
            QtWidgets.QMessageBox.warning(self,'缺少数据库文件','缺少数据库文件')
        else:
            pass

    def signalToSlot(self):
        #所有槽函数和信号的链接
        self.ui.pushButton_6.clicked.connect(self.diag_win)
        self.ui.pushButton_5.clicked.connect(self.getTheDatas)
        self.ui.pushButton_4.clicked.connect(self.clearAll)
        self.ui.radioButton.toggled.connect(self.selectSearchContent)
        self.ui.radioButton_2.toggled.connect(self.selectSearchContent)
        self.ui.radioButton_3.toggled.connect(self.selectSearchContent)
        self.ui.pushButton.clicked.connect(self.beginSearch)
        self.ui.pushButton_2.clicked.connect(self.save_to_excel)
    def windowCenter(self):
    #使窗口居中
        screen = QtWidgets.QApplication.desktop()
        size = self.geometry()
        self.move((screen.width() - size.width())/2,(screen.height() - size.height())/2) 

    def set_time(self):  
    #设置时间为当前时间
        self.ui.dateEdit.setDate(QtCore.QDate.currentDate())
        self.ui.dateEdit_2.setDate(QtCore.QDate.currentDate())
        self.ui.dateEdit_3.setDate(QtCore.QDate.currentDate().addDays(-30))
        self.ui.dateEdit_4.setDate(QtCore.QDate.currentDate())

    def diag_win(self):
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
    
    def csv_init(self):
        #datas.csv文件初始化
        with open('datas.csv','w', encoding='utf-8') as f:
            datawriter = csv.writer(f)
            datawriter.writerow(self.firstrow)
    
    def icuNumMaker(self):
        #获取文件记录的ICU编码病创造新的编码
        with open('icunumMaker.txt','r',encoding='utf-8') as f:
            icunumNow = json.load(f)[0]  #读取文件中最新的ICU编码
        self.icunumNew = icunumNow+1     #计算得出新的ICU编码

    def icuNumWriter(self):
        # 将新的ICU编码重新写入文件
        with open('icunumMaker.txt','w',encoding='utf-8') as fi:
            json.dump([self.icunumNew],fi)
    
    def checkTheBlank(self):
        #检查数据完整性
        a = [1,1,1,1,1,1,1,1]  #设置8个必填项目初始为0
        b = []
        if self.ui.comboBox_7.currentText()== '':
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
        if self.ui.comboBox_5.currentText()== '':
            a[5]=0  #床位号
            b.append('床位号')
        if self.ui.comboBox_6.currentText() == '':
            a[6]=0  #去向
            b.append('去向')
        if self.ui.textEdit.toPlainText() == '':
            a[7]=0  #诊断
            b.append('诊断')
        print(a,b)
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

    def fillInTheList(self):
        #填写30天内出科患者列表
        self.ui.listWidget.clear()
        self.forList = []
        try:
            with open('datas.csv','r',encoding='utf-8') as f:
                next(f)
                rows = csv.reader(f)
                for row in rows:
                    daysnum =(datetime.datetime.now()-datetime.datetime.strptime(row[11],'%Y/%m/%d')).days
                    if daysnum <= 30:
                        self.forList.append([row[11],row[8],row[5]])
            for i in self.forList:
                self.ui.listWidget.addItem(i[0]+' '+i[1]+'床'+' '+i[2])
        except:
            QtWidgets.QMessageBox.warning(self,'30天列表读取数据错误','填充30天出科列表时出现读取数据错误！')
    
    def clearAll(self):
    #清空输入表中的数据
        self.ui.comboBox_7.setCurrentIndex(-1)
        self.ui.lineEdit_4.clear()
        self.ui.lineEdit.clear()
        self.ui.lineEdit_2.clear()
        self.ui.comboBox_2.setCurrentIndex(-1)
        self.ui.lineEdit_3.clear()
        self.ui.comboBox_5.setCurrentIndex(-1)
        self.ui.comboBox_6.setCurrentIndex(-1)
        self.ui.textEdit.clear()
        self.ui.checkBox.setChecked(False)
        self.ui.lineEdit_6.clear()
        self.ui.lineEdit_5.clear()
        self.ui.dateEdit.setDate(QtCore.QDate.currentDate())
        self.ui.dateEdit_2.setDate(QtCore.QDate.currentDate())
    
    def searchTheAdmnum(self,admnum,dischargeDate):
        #搜索相同住院号的患者
        adnmumToSearch = admnum
        dischargeDateToSearch = dischargeDate
        theDischargeDates = []  #列表容纳相同住院号的不同出院时间列表
        theSamePatients =[] #列表容纳返回的患者和住院时间信息
        try:
            with open('datas.csv','r',encoding='utf-8') as f:
                rows = csv.reader(f)
                for row in rows:
                    if adnmumToSearch == row[4]:
                        theDischargeDates.append(row[11])
                        theSamePatients.append(row[5]+' '+row[11])
            if len(theDischargeDates)>0:
                if (dischargeDateToSearch not in theDischargeDates):
                    return(theSamePatients)
                else :
                    return(True)
            else:
                return(False)
        except:
            QtWidgets.QMessageBox.warning(self,'搜索数据错误','保存数据前查重住院号时出现错误！')

    def saveThePatientMessage(self,message):
        #保存患者数据到datas.csv中
        patientMessage = message
        try:
            with open('datas.csv','a',encoding='utf-8') as f:
                dataWriter = csv.writer(f)
                dataWriter.writerow(patientMessage)
            self.icuNumWriter()   #保存数据后更新最新icunum
            self.fillInTheList()
            self.clearAll()
        except:
            QtWidgets.QMessageBox.warning(self,'保存数据错误','保存数据出现错误！请联系开发者。')

    def getTheDatas(self):
        #收集所填入的数据
        self.icuNumMaker()
        icunum = self.icunumNew
        fromWhere = self.ui.comboBox_7.currentText()
        checkinTip = self.ui.lineEdit_4.text()
        checkinTime = self.ui.dateEdit.text()
        admNum = self.ui.lineEdit.text()
        patientName = self.ui.lineEdit_2.text()
        gender = self.ui.comboBox_2.currentText()
        age = self.ui.lineEdit_3.text()
        bedNum = self.ui.comboBox_5.currentText()
        toWhere = self.ui.comboBox_6.currentText()
        checkoutTip = self.ui.lineEdit_5.text()
        checkoutTime = self.ui.dateEdit_2.text()
        diagnosis = self.ui.textEdit.toPlainText()
        isSpecial = 1 if self.ui.checkBox.isChecked() else 0
        comment = self.ui.lineEdit_6.text()
        nowtime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        patientDatas = [
            icunum,
            fromWhere,
            checkinTip,
            checkinTime,
            admNum,
            patientName,
            gender,
            age,
            bedNum,
            toWhere,
            checkoutTip,
            checkoutTime,
            diagnosis,
            isSpecial,
            comment,
            nowtime
            ]
        print(patientDatas)
        checkblank = self.checkTheBlank() #检查空项
        if checkblank:
            checkDate = self.checkDate() #检查日期逻辑
            if checkDate:
                confirmDatas = QtWidgets.QMessageBox.information(    #调用对话窗口确认保存数据
                    self,
                    '请确认保存','是否保存数据？',
                    QtWidgets.QMessageBox.Ok|QtWidgets.QMessageBox.Cancel)
                if confirmDatas == QtWidgets.QMessageBox.Ok:
                    a = self.searchTheAdmnum(admNum,checkoutTime)
                    if a == False:  # 无重复数据直接保存
                        self.saveThePatientMessage(patientDatas)
                    elif a == True: #住院号和日期均重复警告并且不保存
                        QtWidgets.QMessageBox.warning(self,'重复登记','住院号和出院日期均重复')
                    else:           #有相同住院号，确认后保存
                        sameDates = ';'.join(a)
                        c = QtWidgets.QMessageBox.information(
                            self,
                            '有重复的住院号',
                            '''可能为多次住院,请确认后保存
                            住院时间分别为：'''+sameDates,
                            QtWidgets.QMessageBox.Save|QtWidgets.QMessageBox.Cancel)
                        if c == QtWidgets.QMessageBox.Save:
                            self.saveThePatientMessage(patientDatas)
                        else:
                            pass
                else:
                    pass
######### 检索 ##########################################################################
    def beginSearch(self):
    #按条件检索
        self.ui.tableWidget.clearContents()
        fromDateB = self.ui.dateEdit_3.text()
        toDateB = self.ui.dateEdit_4.text()
        nameB = self.ui.lineEdit_7.text()
        admnumB = self.ui.lineEdit_8.text()
        diagnosB = self.ui.lineEdit_9.text()
        print(fromDateB,toDateB,nameB,admnumB,diagnosB)
        a = self.conditionSearch(fromDateB,toDateB,name=nameB,admNum=admnumB,diagnos=diagnosB)
        print(a)
        self.ui.tableWidget.setRowCount(len(a))
        for i in range(len(a)) :
            for n in range(len(self.firstrow)):
                print(a[i][n],type(a[i][n]))
                b = QtWidgets.QTableWidgetItem(a[i][n])
                print(b)
                
                self.ui.tableWidget.setItem(i,n,b)
                self.ui.lineEdit_7.clear()
                self.ui.lineEdit_8.clear()
                self.ui.lineEdit_9.clear()

    def conditionSearch(self,fromDate,toDate,name='',admNum='',diagnos=''):
    # 获取检索条件-检索-返回数据
        fromDateA = fromDate
        toDateA = toDate
        nameA = name
        admNumA = admNum
        diagnosA = diagnos
        print(fromDateA,toDateA,nameA,admNumA,diagnosA)
        result = []
        try:
            with open('datas.csv','r',encoding='utf-8') as f:
                rows = csv.reader(f)
                next(f)
                for row in rows:
                    print(row)
                    if (datetime.datetime.strptime(fromDateA,'%Y/%m/%d')<datetime.datetime.strptime(row[11],'%Y/%m/%d')<datetime.datetime.strptime(toDateA,'%Y/%m/%d')):
                        if nameA != '' :                            
                            if nameA in row[5]:
                                result.append(row)
                        elif admNumA != '' :
                            if admNumA == row[4]:
                                result.append(row)
                        elif diagnosA != '' :
                            if diagnosA in row[12]:
                                result.append(row)
                        else:
                            result.append(row)
            return(result)
        except :
            QtWidgets.QMessageBox.warning(self,'检索错误','检索错误！')

    def selectSearchContent(self):
    #RadioButton控制输入框可用性
        if self.ui.radioButton.isChecked()==True:
            self.ui.lineEdit_7.setEnabled(True)
            self.ui.lineEdit_8.setEnabled(False)
            self.ui.lineEdit_9.setEnabled(False)
        elif self.ui.radioButton_2.isChecked()==True:
            self.ui.lineEdit_7.setEnabled(False)
            self.ui.lineEdit_8.setEnabled(True)
            self.ui.lineEdit_9.setEnabled(False)
        else:
            self.ui.lineEdit_7.setEnabled(False)
            self.ui.lineEdit_8.setEnabled(False)
            self.ui.lineEdit_9.setEnabled(True)    
  
    def save_to_excel(self):
    #保存数据到excel格式
        wb = Workbook()
        ws = wb.active
        title= []
        for c in range(self.ui.tableWidget.columnCount()):
            title.append(self.ui.tableWidget.horizontalHeaderItem(c).text())
        ws.append(title)
        for r in range(self.ui.tableWidget.rowCount()):
            row_data =[]
            for col in range(self.ui.tableWidget.columnCount()):
                row_data.append(self.ui.tableWidget.item(r,col).text())
            ws.append(row_data)        
        now_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        filepath = QtWidgets.QFileDialog.getSaveFileName(self,'保存文件','result'+'_%s.xlsx'%now_time,'xlsx files (*.xlsx)')
        print(filepath)
        wb.save(filepath[0]+'_%s.xlsx'%now_time)  

def main():
    app = QtWidgets.QApplication(sys.argv)
    main = CheckinOut()
    main.show()
    main.checkCsvFile()   #在窗口出现后检查数据库文件是否存在
    sys.exit(app.exec_())
    

if __name__ == "__main__":
    main()