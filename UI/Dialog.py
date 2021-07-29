from PyQt5.QtWidgets import QDialog
from UI.Ui_dialog import Ui_Dialog

class Dialog(QDialog,Ui_Dialog):
    def __init__(self,parent=None):
        super(Dialog,self).__init__(parent)
        self.setupUi(self)

    #该方法在父类方法中调用，直接打开了子窗体，返回值则用于向父窗体数据的传递
    def getResult(self,parent=None):
        dialog=Dialog(parent)
        result=dialog.exec_()
        if dialog.radioButton.isChecked():
            i = 0
        elif dialog.radioButton_2.isChecked():
            i = 1
        return (i,result)