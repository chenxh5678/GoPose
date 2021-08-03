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
from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import pyqtSignal
# 视频手动打点
class MyLabel(QLabel):
    button_clicked_signal = pyqtSignal()
    def __init__(self, parent=None):
        super(MyLabel, self).__init__((parent))
        self.flag = False
        self.isShow = False
        self.clk_pos=None
        self.x=None
        self.y=None

    def mousePressEvent(self, event):
        QLabel.mousePressEvent(self, event)
        self.clk_pos = event.globalPos()
        self.x = event.x()
        self.y = event.y()
        self.isShow = True
        if self.isShow==True:
            self.update()
            
    def mouseReleaseEvent(self, event):
        QLabel.mouseReleaseEvent(self, event)
        self.button_clicked_signal.emit()
        self.isShow = False
    
    def connect_customized_slot(self, func):
        self.button_clicked_signal.connect(func)
 
    def getPointGlobalPos(self):
        return self.clk_pos
