import sys
from PyQt5 import QtWidgets,QtGui,QtCore

# import micudatabasetool
import time
from PyQt5.QtCore import pyqtSignal
from Ui_diagnosis import *

class DiagnosisWin(QtWidgets.QWidget):
    diagnosis = pyqtSignal(str)
    def __init__(self,parent=None):
        super().__init__(parent)
        self.ui = Ui_diagnosis()
        self.ui.setupUi(self)
        self.center()
        self.ui.pushButton.clicked.connect(self.diag_ins)

    def center(self):
        screen = QtWidgets.QApplication.desktop()
        size = self.geometry()
        self.move((screen.width() - size.width())/2,(screen.height() - size.height())/2)  

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

