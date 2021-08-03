'''
GoPose:Artificial intelligence motion analysis software
Copyright (C) <2021>  <Xihang Chen>

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as published
by the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
Email: 786028450@qq.com
'''
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