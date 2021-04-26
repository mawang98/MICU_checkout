import sys
from PyQt5 import QtWidgets,QtGui,QtCore

# import micudatabasetool
import time
from PyQt5.QtCore import pyqtSignal
from Ui_diagnosis import *
from dabaseTool import *

class DiagnosisWin(QtWidgets.QWidget):
    diagnosis = pyqtSignal(str)
    def __init__(self,parent=None):
        super().__init__(parent)
        self.ui = Ui_diagnosis()
        self.ui.setupUi(self)
        self.center()
        self.ui.pushButton.clicked.connect(self.diag_ins)
        self.fillInDiagnosisToCombox()

    def center(self):
        screen = QtWidgets.QApplication.desktop()
        size = self.geometry()
        self.move((screen.width() - size.width())/2,(screen.height() - size.height())/2)  
    
    def fillInDiagnosisToCombox(self):
        b = ['肺炎','ARDS','AECOPD','肺栓塞','呼吸衰竭','心力衰竭','急性心肌梗死','心源性休克','心肺复苏后','肾功能衰竭','肝功能衰竭','脓毒症休克']
        a = Parameters().read_diagnosis()
        b = list(dict.values(a))
        self.ui.comboBox.clear()
        self.ui.comboBox.addItems(b)
        self.ui.comboBox.setCurrentIndex(-1)

    def diag_ins(self):           #槽函数，将下拉列表内的内容加入文本框
        self.ui.textEdit.insertPlainText(self.ui.comboBox.currentText()+',')
    
    def emit_diag(self):      #信号发出，将文本框内容写入出院诊断
        self.diagnosis.emit(self.ui.textEdit.toPlainText())
        
def main():
    app = QtWidgets.QApplication(sys.argv)
    main = DiagnosisWin()
    main.show()
    sys.exit(app.exec_())
if __name__ == "__main__":
    main()

