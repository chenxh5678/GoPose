'''
设置：单点的动画移动
'''
from typing import Text
import numpy as np
from matplotlib.lines import Line2D
import matplotlib.pyplot as plt
from matplotlib.widgets import Button,TextBox
from modules.filter import butter_lowpass_filtfilt
from PyQt5.QtWidgets import QDialog
from UI.Ui_table import Ui_Dialog

class Point_Move(QDialog,Ui_Dialog):
    showverts = True
    offset = 3 # 距离偏差设置
    plt.rcParams['font.sans-serif']=['SimHei'] #用来正常显示中文标签
    plt.rcParams['axes.unicode_minus']=False #用来正常显示负号

    def __init__(self,value,parent=None):  # df:0列x值，1列y值
        # 父类初始化方法
        super(Point_Move,self).__init__(parent)
        self.setupUi(self)
        
        self.cutOff = 10
        self.fps = 30
        # 创建figure（绘制面板）、创建图表（axes）
        self.fig,self.ax = plt.subplots()
        # 设置标题
        self.ax.set_title('拖动坐标点以修改它')
        # 设置初始值
        self.x = [x for x in range(len(value))]
        self.y = value
        self.yNew = None
        # 设置坐标轴范围
        maxX = len(value)
        minY = value.min()
        maxY = value.max()
        self.ax.set_xlim((0, maxX))
        self.ax.set_ylim((minY - 20, maxY + 20))
        # 设置按钮
        self.pushButton.clicked.connect(self.filter)
        self.pushButton_2.clicked.connect(self.saveData)
        # 绘制2D的动画line
        self.line = Line2D(self.x, self.y, color = 'r', 
                           marker='.', markerfacecolor='r',
                           animated=True)  #   ls="",
        self.ax.add_line(self.line)
        # 标志值设为none
        self._ind = None
        # 设置画布，方便后续画布响应事件
        canvas = self.fig.canvas
        canvas.mpl_connect('draw_event', self.draw_callback)
        canvas.mpl_connect('button_press_event', self.button_press_callback)
        canvas.mpl_connect('button_release_event', self.button_release_callback)
        canvas.mpl_connect('motion_notify_event', self.motion_notify_callback)
        self.canvas = canvas
        
        # 设置布局
        self.verticalLayout.addWidget(self.canvas)

    #该方法在父类方法中调用，直接打开了子窗体，返回值则用于向父窗体数据的传递
    def get(self,value,parent=None):
        dialog=Point_Move(value,parent)
        out = dialog.y
        ok=dialog.exec_()
        return out,ok
        
    # 滤波平滑
    def filter(self, event):  
        try:
            t = int(self.lineEdit.text())
            f = int(self.lineEdit_2.text())
            if 0 < t < 1000:
                self.cutOff = t
            if 0 < f < 1500:
                self.fps = f
            
            wn = 2*self.cutOff/self.fps
            if 0 < wn < 1:
                pass
            else:
                self.cutOff = 0.5 * self.fps - 1
            # 开始滤波
            self.yNew = butter_lowpass_filtfilt(self.y,self.cutOff, self.fps)
            self.line = Line2D(self.x, self.yNew, color = 'r', 
                            marker='.', markerfacecolor='r',
                            animated=True)  #   ls="",
            self.ax.add_line(self.line)
            self.canvas.restore_region(self.background)
            self.ax.draw_artist(self.line)
            self.canvas.blit(self.ax.bbox)
        except:
            pass

    def saveData(self,event):
        self.y = self.yNew
        
    # 界面重新绘制
    def draw_callback(self, event):
        self.background = self.canvas.copy_from_bbox(self.ax.bbox)
        self.ax.draw_artist(self.line)
        self.canvas.blit(self.ax.bbox)

    def get_ind_under_point(self, event):
        'get the index of the vertex under point if within epsilon tolerance'
        # 在公差允许的范围内，求出鼠标点下顶点坐标的数值
        xt,yt = np.array(self.x),np.array(self.y)
        d = np.sqrt((xt-event.xdata)**2 + (yt-event.ydata)**2)
        indseq = np.nonzero(np.equal(d, np.amin(d)))[0]
        ind = indseq[0]
        # 如果在公差范围内，则返回ind的值
        if d[ind] >=self.offset:
            ind = None
        return ind

    # 鼠标被按下，立即计算最近的顶点下标
    def button_press_callback(self, event):
        'whenever a mouse button is pressed'
        if not self.showverts: return
        if event.inaxes==None: return
        if event.button != 1: return
        self._ind = self.get_ind_under_point(event)

    # 鼠标释放后，清空、重置
    def button_release_callback(self, event):
        'whenever a mouse button is released'
        if not self.showverts: return
        if event.button != 1: return
        self._ind = None

    # 鼠标移动的事件
    def motion_notify_callback(self, event):
        'on mouse movement'
        if not self.showverts: return
        if self._ind is None: return
        if event.inaxes is None: return
        if event.button != 1: return
        # 更新数据
        y = event.ydata
        self.y[self._ind] = y
        # 根据更新的数值，重新绘制图形
        self.line = Line2D(self.x, self.y, color = 'r', 
                           marker='.', markerfacecolor='r',
                           animated=True)                
        self.ax.add_line(self.line)
        # 恢复背景
        self.canvas.restore_region(self.background)
        self.ax.draw_artist(self.line)
        self.canvas.blit(self.ax.bbox)


