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
