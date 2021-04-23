import sys
import os

from PyQt5 import QtWidgets,QtGui,QtCore
from PyQt5.QtCore import pyqtSignal,pyqtSlot,QObject

from Ui_alterData import *

class AlterDatas(QtWidgets.QWidget):
    def __init__(self,parent=None):
        super().__init__(parent)
        self.ui = Ui_Form()
        self.a = self.ui.setupUi(self)
        self.windowCenter()
        self.initSet()

    def windowCenter(self):
    #使窗口居中
        screen = QtWidgets.QApplication.desktop()
        size = self.geometry()
        self.move((screen.width() - size.width())/2,(screen.height() - size.height())/2) 
    def initSet(self):
        self.icuBeds=['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','16','17','18','19','20','21','22','23','24','25','26','27','J1','J2','J3']
        self.fromWhere = ['急诊','外科转入','内科转入','外科术后转入','重症普通病房转入']
        self.toWhere = ['自动出院','死亡','转外科','转内科']
        self.ui.comboBox_5.addItems(self.icuBeds)  
        self.ui.comboBox_7.addItems(self.fromWhere)
        self.ui.comboBox_6.addItems(self.toWhere)


    # def getTheData(self):
    #     #获取数据



def main():
    app = QtWidgets.QApplication(sys.argv)
    main = AlterDatas()
    main.show()
    sys.exit(app.exec_())
    

if __name__ == "__main__":
    main()