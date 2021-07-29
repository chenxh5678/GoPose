#  Author: Xihang Chen
#  Email: 786028450@qq.com

import sys,cv2,pickle,os,csv,math
from UI.Ui_GoPose import Ui_MainWindow
from PyQt5.QtWidgets import (QApplication,QMainWindow,QTableWidgetItem,QLineEdit,
                            QFileDialog,QMessageBox,QHeaderView,QInputDialog,QAbstractItemView)
from PyQt5.QtCore import Qt,QDir,QSize
from PyQt5.QtGui import QImage,QPixmap,QPalette,QIcon,QFont
from modules.mylabel import MyLabel
from modules.Analysis import analysis
from modules import calculation
import numpy as np
from UI.Dialog import Dialog

class GoPose(Ui_MainWindow,QMainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.default()
        self.MenuBar()
        self.Img_Label()
        self.button()

    def default(self):  # 一些默认值
        self.fps = 0  # 当前帧
        self.fpsMax = 0
        self.fpsRate = 1
        self.pc = None  # 比例系数
        self.pkl = False
        self.scale = False  # 比例尺开关
        self.long = False  # 测量长度开关
        self.longDic = {}  # 长度字典
        self.time = False  # 测量时间开关
        self.timePoint = []  # 时间存储
        self.timeDic = {}  # 时间字典
        self.level = False  # 水平仪开关
        self.levelPoint = []
        self.rotationAngle = 0  # 画面旋转角
        self.item = 0
        self.x = 0
        self.y = 0
        self.member_ = 3  # 默认显示3人棍图
        self.cut1 = None
        self.cut2 = None
        self.drawPoint = 0
        self.play2 = False  # 播放状态
        self.changFlag = 0  # 播放暂停图标
        self.cwd = os.getcwd() # 获取当前程序文件位置
        self.sli_label()  # 显示滑动条状态
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)
        # self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)
        self.tableWidget.horizontalHeader().setSectionResizeMode(0, QHeaderView.Interactive)  # 第一列可调整列宽
        self.tableWidget.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

    def MenuBar(self):  # 菜单栏、工具栏、状态栏
        self.actionExit.triggered.connect(QApplication.instance().quit)
        self.actionZoomIn.triggered.connect(self.onViewZoomIn)
        self.actionZoomOut.triggered.connect(self.onViewZoomOut)
        self.actionNormalSize.triggered.connect(self.onViewNormalSize)
        self.actionAnalysis.triggered.connect(self.analytic)
        self.actionOpen.triggered.connect(self.onFileOpen)
        self.actionFps.triggered.connect(self.realFPS)
        self.actionMember.triggered.connect(self.member)
        self.actionKey.triggered.connect(self.loadKeys)
        self.actionOne.triggered.connect(self.confirmSelection)
        self.actionscaledraw.triggered.connect(self.scaleButton)
        self.treeWidget.itemClicked.connect(self.treeClicked)
        self.actionSave.triggered.connect(self.save)
        self.actionOutVideo.triggered.connect(self.exportVideo)
        self.actionVideoNone.triggered.connect(self.exportPointlessVideo)
        self.actionOutPoint.triggered.connect(self.exportKeys)
        self.actionCam.triggered.connect(self.camera)
        self.actiondrawType.triggered.connect(self.pointType)
        self.actionmanager.triggered.connect(self.dockEvent)
        self.actionshowWin.triggered.connect(self.dockEvent)
        self.actionLevel.triggered.connect(self.levelButton)
        self.actionOutPara.triggered.connect(self.exportResults)
        self.actionFont.triggered.connect(self.fontSize)

    def button(self):
        self.pushButton.clicked.connect(self.last)
        self.pushButton_2.clicked.connect(self.next_)
        self.imgLabel.connect_customized_slot(self.modifyKey)
        self.imgLabel.connect_customized_slot(self.Scale)
        self.imgLabel.connect_customized_slot(self.length)
        self.imgLabel.connect_customized_slot(self.levelTool)
        self.pushButton_5.clicked.connect(self.workspaceClear)
        self.pushButton_3.clicked.connect(self.workspaceStart)
        self.pushButton_4.clicked.connect(self.workspaceEnd)
        self.pushButton_6.clicked.connect(self.timeButton)
        self.pushButton_7.clicked.connect(self.lengthButton)
        self.pushButton_8.clicked.connect(self.jumpToBeginning)
        self.pushButton_9.clicked.connect(self.jumpToEnd)
        self.pushButton_10.clicked.connect(self.play)

    '''-----图像显示界面-----'''
    def Img_Label(self):  # 创建显示图片的窗口
        self.scaleFactor = 0.0  # 缩放因子
        self.imgLabel = MyLabel()  
        self.imgLabel.setScaledContents(True)  # 大小自适应
        self.imgLabel.setAlignment(Qt.AlignCenter)  # 居中
        self.scrollArea.setWidget(self.imgLabel)
        self.scrollArea.setBackgroundRole(QPalette.Dark)
    
    def onViewZoomIn(self):  # 图像放大
        self.scaleIamge(1.2)   
    
    def onViewZoomOut(self):  # 图像缩小
        self.scaleIamge(0.8) 

    def scaleIamge(self, factor):  # 图像调整大小
        self.scaleFactor *= factor
        self.imgLabel.resize(self.scaleFactor * self.imgLabel.pixmap().size())
        self.adjustScrollBar(self.scrollArea.horizontalScrollBar(), factor)
        self.adjustScrollBar(self.scrollArea.verticalScrollBar(), factor)
        self.actionZoomIn.setEnabled(self.scaleFactor < 10.0)
        self.actionZoomOut.setEnabled(self.scaleFactor > 0.2)
    
    def adjustScrollBar(self, scrollBar, factor):  # 图像滚动轴
        scrollBar.setValue(int(factor * scrollBar.value() + ((factor - 1) * scrollBar.pageStep()/2)))

    def onViewNormalSize(self):  # 是图像原始尺寸
        self.imgLabel.adjustSize()
        self.scaleFactor = 1.0

    '''-----滑动条、逐帧播放-----'''
    def sli(self):  # 滑动条取值
        self.fps = self.horizontalSlider.value()
        self.sli_label()
        self.currentFrame()
        
    def next_(self):  # 下一帧
        if self.fps < self.fpsMax:
            self.fps += 1
            self.horizontalSlider.setSliderPosition(self.fps)
            self.sli_label()

    def last(self):  # 上一帧
        if self.fps > 0:
            self.fps -= 1
            self.horizontalSlider.setSliderPosition(self.fps)
            self.sli_label()
    
    def sli_label(self):  # 显示帧数状态
        time_now = round(self.fps/self.fpsRate,3)
        time_totle = round(self.fpsMax/self.fpsRate,3)
        slide_text = '总时长：{}秒（{}帧）      当前：{}秒（{}帧）'.format(time_totle,self.fpsMax,time_now,self.fps)
        self.label.setText(slide_text)
        range_text = '工作区开始：{}帧        工作区结束：{}帧'.format(self.cut1,self.cut2)
        self.label_4.setText(range_text)

    '''-----Openpose解析关键点-----'''
    def analytic(self):
        radio,ok= Dialog.getResult(self)
        if ok:
            try:
                analysis(self.video, self.cut1, self.cut2, zone = radio)
                QMessageBox.information(self, '消息', '解析点数据已存入data文件夹下')
            except Exception as e:
                QMessageBox.warning(self,'解析错误',str(e),QMessageBox.Yes|QMessageBox.No,QMessageBox.Yes)
    
    '''-----帧率、显示棍图人数-----'''
    def realFPS(self):
        fpsRate, okPressed = QInputDialog.getInt(self, '视频帧率', '输入实际拍摄帧率：', self.fpsRate, 1, 10000)
        if okPressed and fpsRate != '':
            self.fpsRate = fpsRate
            if self.pkl:
                self.text(i=1)
            else:
                self.text()

    def member(self):
        member_, okPressed = QInputDialog.getInt(self, '显示解析点人数', '输入需显示的解析点人数(>1)：', 3, 2, 10000)
        if okPressed and member_ != '':
            self.member_ = member_
            self.text(i=1)

    def text(self,i=0):
        if i:
            video_name = self.video.split('/')[-1]
            text = 'Video:{}        Size:{}        FPS:{}       解析点人数：{}      画面旋转角：{}°'.format(video_name,self.shape, self.fpsRate,self.member_, self.rotationAngle)
            self.label_2.setText(text)
        else:
            video_name = self.video.split('/')[-1]
            text = 'Video:{}        Size:{}        FPS:{}       画面旋转角：{}°'.format(video_name,self.shape, self.fpsRate, self.rotationAngle)
            self.label_2.setText(text)

    '''-----管理器属性-----'''
    def treeClicked(self):
        try:
            if self.item:
                item = self.item
            else:
                item = self.treeWidget.currentItem().text(0)
            if item == '测试对象':  # 测试对象信息
                try:
                    self.tableWidget.disconnect()
                except:
                    pass
                self.tableWidget.clear()
                self.tableWidget.setRowCount(0)
                self.tableWidget.setHorizontalHeaderLabels(['属性','值'])
                attribute = ['姓名：','性别：','年龄：','身高（米）：','体重（公斤）：']
                row = 0
                for a in attribute:
                    count = self.tableWidget.rowCount()
                    self.tableWidget.insertRow(count)  # 新增行
                    newItem=QTableWidgetItem(a)
                    self.tableWidget.setItem(row,0,newItem)
                    row += 1
            elif item == '选择单人解析点':
                self.tableWidget.clear()
                self.tableWidget.setRowCount(0)
                self.tableWidget.setHorizontalHeaderLabels(['点击选择','空格键确定'])
                # self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)  # 参数表格不可编辑
                if self.pkl:
                    self.tableWidget.clicked.connect(self.choosePerson)
                    self.currentKeys()
                else:
                    count = self.tableWidget.rowCount()
                    self.tableWidget.insertRow(count)  # 新增行
                    newItem=QTableWidgetItem('缺少解析点数据')
                    self.tableWidget.setItem(0,0,newItem)
            elif item == '比例尺信息':
                try:
                    self.tableWidget.disconnect()
                except:
                    pass
                self.tableWidget.clear()
                self.tableWidget.setRowCount(0)
                self.tableWidget.setHorizontalHeaderLabels(['属性','值'])
                if self.pc:
                    count = self.tableWidget.rowCount()
                    self.tableWidget.insertRow(count)  # 新增行
                    newItem=QTableWidgetItem('比例系数(像素/实际):')
                    self.tableWidget.setItem(0,0,newItem)
                    newItem = QTableWidgetItem(str(self.pc))
                    self.tableWidget.setItem(0,1,newItem)
                else:
                    count = self.tableWidget.rowCount()
                    self.tableWidget.insertRow(count)  # 新增行
                    newItem = QTableWidgetItem('未设置比例尺')
                    self.tableWidget.setItem(0,0,newItem)
            elif item == '解析点修正':
                try:
                    self.tableWidget.disconnect()
                except:
                    pass
                self.tableWidget.clear()
                self.tableWidget.setRowCount(0)
                self.tableWidget.setHorizontalHeaderLabels(['名称','编号'])
                if self.pkl:
                    point = ['0 鼻子', '1 脖子', '2 右肩', '3 右肘','4 右腕','5 左肩','6 左肘','7 左腕','8 中臀','9 右臀',
                            '10 右膝','11 右踝','12 左臀','13 左膝','14 左踝','15 右眼','16 左眼','17 右耳','18 左耳',
                            '19 左大拇指','20 左小拇指','21 左足跟','22 右大拇指','23 右小拇指','24 右足跟']
                    r = 0
                    for p in point:
                        row = p.split()
                        count = self.tableWidget.rowCount()
                        self.tableWidget.insertRow(count)  # 新增行
                        newItem=QTableWidgetItem(row[1])
                        self.tableWidget.setItem(r,0,newItem)
                        newItem = QTableWidgetItem(row[0])
                        self.tableWidget.setItem(r,1,newItem)
                        r += 1
                else:
                    count = self.tableWidget.rowCount()
                    self.tableWidget.insertRow(count)  # 新增行
                    newItem = QTableWidgetItem('缺少解析点数据')
                    self.tableWidget.setItem(0,0,newItem)
            elif item == '显示运动学结果':
                try:
                    self.tableWidget.disconnect()
                except:
                    pass
                self.tableWidget.clear()
                self.tableWidget.setHorizontalHeaderLabels(['结果','值'])
                self.showResult()
        except Exception as e:
            QMessageBox.warning(self,'管理器错误',str(e))

    '''----------打开视频文件----------'''
    def onFileOpen(self): 
        self.video,_ = QFileDialog.getOpenFileName(self, '打开视频文件', QDir.currentPath()) 
        if self.video:
            try:
                self.horizontalSlider.setSliderPosition(0)  # 滑动条归零
                self.cap = cv2.VideoCapture(self.video) 
                cap = self.cap
                self.fpsMax = cap.get(7) - 1
                self.horizontalSlider.setMaximum(self.fpsMax)
                self.horizontalSlider.valueChanged.connect(self.sli)
                # 状态栏内容
                self.fpsRate = round(cap.get(cv2.CAP_PROP_FPS), 2)  # 获取视频帧率
                width = int(cap.get(3))  # 获取视频宽度
                height = int(cap.get(4))  # 获取视频高度
                self.shape = str(width) + '×' + str(height)  # 获取视频size
                self.text()
                self.sli_label()
                # 显示图像
                rval,frame = cap.read()
                frame=cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
                self.image = QImage(frame.data,frame.shape[1],frame.shape[0],QImage.Format_RGB888)
                self.imgLabel.setPixmap(QPixmap.fromImage(self.image))
                self.imgLabel.setCursor(Qt.CrossCursor)
                self.scaleFactor = 1.0
                self.imgLabel.adjustSize()
                # 设置按钮可用
                self.actionAnalysis.setEnabled(True)  # 解析按钮可用
                self.actionKey.setEnabled(True)  # '载入关键点'可选中
                self.actionscaledraw.setEnabled(True)
                self.actionZoomIn.setEnabled(True)
                self.actionZoomOut.setEnabled(True)
                self.actionNormalSize.setEnabled(True)
                self.actionFps.setEnabled(True)
                self.actionVideoNone.setEnabled(True)
                self.actionLevel.setEnabled(True)
                self.pushButton_6.setEnabled(True)
                self.pushButton_7.setEnabled(True)
                self.pushButton_3.setEnabled(True)
                self.pushButton_4.setEnabled(True)
                self.pushButton_10.setEnabled(True)
                self.pushButton.setEnabled(True)
                self.pushButton_2.setEnabled(True)
                self.pushButton_8.setEnabled(True)
                self.pushButton_9.setEnabled(True)
            except Exception as e:
                QMessageBox.warning(self,'打开视频错误',str(e))

    # 显示指定帧的图像
    def currentFrame(self):
        if self.video:
            try:
                cap = self.cap
                cap.set(cv2.CAP_PROP_POS_FRAMES,self.fps)  # 显示指定帧的画面
                rval,frame = cap.read()
                if self.pkl:
                    if self.data:
                        now = self.currentKeys()
                        if type(now) == np.ndarray:
                            for d in now:  # 显示                              
                                calculation.draw(frame,d,type = self.drawPoint)
                            self.showResult()  # 计算参数
                frame=cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
                imge = QImage(frame.data,frame.shape[1],frame.shape[0],QImage.Format_RGB888)
                self.imgLabel.setPixmap(QPixmap(imge))
                self.imgLabel.setCursor(Qt.CrossCursor)
            except Exception as e:
                QMessageBox.warning(self,'显示图像错误',str(e))

    def camera(self):  # 摄像头
        ok = QMessageBox.information(self,'消息','打开摄像头',QMessageBox.Yes | QMessageBox.No,QMessageBox.Yes)
        if ok == 16384:
            path = QFileDialog.getSaveFileName(self, '录像保存位置', os.getcwd(), "MP4(*.mp4)")
            cap = cv2.VideoCapture(0)
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 设置写入视频的编码格式
            out = cv2.VideoWriter(path[0],fourcc, 20.0, (640,480))
            start = False
            while 1:
                ret, frame = cap.read()
                if cv2.waitKey(10) & 0xFF == ord('q'):
                    start = True
                elif cv2.waitKey(10) == ord('e'):
                    start = False
                if start == True:
                    out.write(frame)
                cv2.imshow('Press Q to Start Recording; E to Stop Recording, ESC to Exit',frame)
                key = cv2.waitKey(10)
                if key == 27:
                    break
            cap.release()
            out.release()
            cv2.destroyAllWindows()

    '''-----关键点事件-----'''
    def loadKeys(self):    # 载入解析点
        self.pkl,_ = QFileDialog.getOpenFileName(self, '载入关键点', QDir.currentPath()) 
        if self.pkl:
            try:
                with open(self.pkl, 'rb') as file0:
                    self.data = pickle.load(file0)  # 解析点数据
                if self.data != None:
                    cap = self.cap
                    cap.set(cv2.CAP_PROP_POS_FRAMES,self.fps)  # 显示指定帧的画面
                    rval,frame = cap.read()                 
                    now = self.currentKeys()  
                    if type(now) == np.ndarray:              
                        for d in now:  # 显示
                            calculation.draw(frame,d,type = self.drawPoint)
                    frame=cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
                    imge = QImage(frame.data,frame.shape[1],frame.shape[0],QImage.Format_RGB888)
                    self.imgLabel.setPixmap(QPixmap(imge))
                    self.imgLabel.setCursor(Qt.CrossCursor)
                    self.text(i=1)
                    self.actionMember.setEnabled(True)
                    self.actionOutPoint.setEnabled(True)
                    self.actionOutPara.setEnabled(True)
                    self.actionOne.setEnabled(True)
                    self.actionSave.setEnabled(True)
                    self.actionOutVideo.setEnabled(True)
                    self.showResult()
            except Exception as e:
                QMessageBox.warning(self,'载入解析点错误',str(e))
    
    def currentKeys(self):  # 获取当前帧25关键点数据
        try:     
            item = self.treeWidget.currentItem()
            if item:
                item = item.text(0)
                if item == '选择单人解析点':
                    self.tableWidget.setRowCount(0)
                    now = self.data[self.fps]
                    if type(now) == np.ndarray:
                        now = self.showPeople(now)  # 筛选出3人
                        choosePerson = [str(m) for m in range(len(now))]
                        row = 0
                        for a in choosePerson:
                            count = self.tableWidget.rowCount()
                            self.tableWidget.insertRow(count)  # 新增行
                            newItem=QTableWidgetItem(a)
                            self.tableWidget.setItem(row,1,newItem)
                            manItem = QTableWidgetItem('人物')
                            self.tableWidget.setItem(row,0,manItem)
                            row += 1
                else:
                    now = self.data[self.fps]
                    if type(now) == np.ndarray:
                        now = self.showPeople(now)  # 筛选出3人
            else:
                now = self.data[self.fps]
                if type(now) == np.ndarray:
                    now = self.showPeople(now)  # 筛选出3人
            return now
        except Exception as e:
            QMessageBox.warning(self,'当前解析点错误',str(e))
    
    def modifyKey(self):  # 修改解析坐标点
        try:
            item = self.treeWidget.currentItem().checkState(0)
            if item == 2 and self.pkl:
                if type(self.data[self.fps]) == np.ndarray:
                    if self.data[self.fps].shape[0] == 1:
                        i = self.tableWidget.currentRow()
                        x1 = self.imgLabel.x
                        y1 = self.imgLabel.y
                        x1 = int(x1 / self.scaleFactor + 0.5)
                        y1 = int(y1 / self.scaleFactor + 0.5)
                        now = self.currentKeys()[0]          
                        now[i][0] = x1  # 修改25坐标点数据
                        now[i][1] = y1
                        self.data[self.fps][0] = now
                        # 重新读取图像并画图
                        cap = self.cap
                        cap.set(cv2.CAP_PROP_POS_FRAMES,self.fps)  
                        rval,frame = cap.read()
                        calculation.draw(frame,now,type = self.drawPoint)
                        frame=cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
                        imge = QImage(frame.data,frame.shape[1],frame.shape[0],QImage.Format_RGB888)
                        self.imgLabel.setPixmap(QPixmap.fromImage(imge))
                        self.showResult()  # 计算结果
        except Exception as e:
            QMessageBox.warning(self,'修改解析点错误',str(e))

    '''-----选人事件-----'''
    def showPeople(self,now):  # 最大的前3人显示  
        long_dic = {}
        i = 0
        for pepo in now:
            try:
                neck = pepo[1]
                hip = pepo[8]
                long1 = ((neck[0] - hip[0]) ** 2 + (neck[1] - hip[1]) ** 2) ** 0.5
                long_dic[long1] = i
                i += 1
            except Exception as e:
                QMessageBox.warning(self,'显示解析点人数错误',str(e))
        long_key = sorted(long_dic.items(),key = lambda x:x[0],reverse=True)
        now_l = [] 
        show = self.member_
        for v in long_key[:show]:
            now_l.append(now[v[1]])
        now_select = np.array(now_l)
        return now_select
    
    def choosePerson(self):  # 选择单人解析点
        try:
            m = self.tableWidget.currentRow()
            cap = self.cap
            cap.set(cv2.CAP_PROP_POS_FRAMES,self.fps)  
            rval,frame = cap.read()
            now = self.currentKeys()
            if type(now) == np.ndarray:
                self.now = now[m]
                calculation.draw(frame,self.now,type = self.drawPoint)
            frame=cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
            imge = QImage(frame.data,frame.shape[1],frame.shape[0],QImage.Format_RGB888)
            self.imgLabel.setPixmap(QPixmap.fromImage(imge))
        except Exception as e:
            QMessageBox.warning(self,'选择单人解析点错误',str(e))

    def confirmSelection(self):  # 选择人物后确定
        row = self.tableWidget.rowCount()
        if row > 1:
            self.tableWidget.clearContents()
            self.tableWidget.setRowCount(1)
            newItem=QTableWidgetItem(str(0))
            self.tableWidget.setItem(0,1,newItem)
            manItem = QTableWidgetItem('人物')
            self.tableWidget.setItem(0,0,manItem)
            self.data[self.fps] = np.array([self.now])
            self.showResult()  # 计算参数
    
    '''-----结果事件-----'''
    def showResult(self):  # 显示结果      
        item = self.treeWidget.currentItem()
        if item:
            item = item.text(0)
            if item == '显示运动学结果':
                self.tableWidget.setRowCount(0)
                if self.longDic:  # 显示长度结果
                    for key,value in self.longDic.items():
                        count = self.tableWidget.rowCount()
                        self.tableWidget.insertRow(count)  # 新增行
                        newItem=QTableWidgetItem(key)
                        self.tableWidget.setItem(count,0,newItem)
                        newItem=QTableWidgetItem(str(value))
                        self.tableWidget.setItem(count,1,newItem)
                if self.timeDic:  # 显示时间结果
                    for key,value in self.timeDic.items():
                        count = self.tableWidget.rowCount()
                        self.tableWidget.insertRow(count)  # 新增行
                        newItem=QTableWidgetItem(key)
                        self.tableWidget.setItem(count,0,newItem)
                        newItem=QTableWidgetItem(str(value))
                        self.tableWidget.setItem(count,1,newItem)
                if self.pkl:  # 显示解析点
                    if self.data[self.fps].shape[0] == 1:  # 显示解析点结果
                        ind = self.data[self.fps][0]  # 当前帧的解析点
                        ind_l = 0
                        if self.fps > 0:
                            ind_l = self.data[self.fps-1][0]  # 前一帧解析点坐标
                        result = calculation.para(ind,ind_l,self.fpsRate,self.pc,self.rotationAngle) 
                        for key,value in result.items():
                            count = self.tableWidget.rowCount()
                            self.tableWidget.insertRow(count)  # 新增行
                            newItem=QTableWidgetItem(key)
                            self.tableWidget.setItem(count,0,newItem)
                            newItem=QTableWidgetItem(str(value))
                            self.tableWidget.setItem(count,1,newItem)
                if self.pkl or self.longDic or self.timeDic:
                    pass
                else:
                    self.tableWidget.setRowCount(1)
                    newItem = QTableWidgetItem('缺少解析点数据')
                    self.tableWidget.setItem(0,0,newItem)
                    
    '''-----比例尺-----'''
    def scaleButton(self):
        self.scale = True
        self.scale_point = []
        
    def Scale(self):  # 比例尺
        if self.scale == True:
            x1 = self.imgLabel.x
            y1 = self.imgLabel.y
            x1 = int(x1 / self.scaleFactor + 0.5)
            y1 = int(y1 / self.scaleFactor + 0.5)
            self.scale_point.append((x1,y1))
            # 重新读取图像并画图
            cap = self.cap
            cap.set(cv2.CAP_PROP_POS_FRAMES,self.fps)  
            rval,frame = cap.read()
            for p in self.scale_point:
                cv2.circle(frame,p,5,(200,200,0),3)
            frame=cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
            imge = QImage(frame.data,frame.shape[1],frame.shape[0],QImage.Format_RGB888)
            self.imgLabel.setPixmap(QPixmap.fromImage(imge))
            if len(self.scale_point) >= 2:
                self.scale = False
                length, ok = QInputDialog.getDouble(self, '比例尺', '输入比例尺实际长度（米）：', 1, 0.001 , 100, 3)
                if ok:
                    px = ((self.scale_point[0][0] - self.scale_point[1][0]) ** 2 + (self.scale_point[0][1] - self.scale_point[1][1]) ** 2) ** 0.5
                    self.pc = round(px / length, 2)  # 比例系数
                    self.item = '比例尺信息'
                    self.treeClicked() 
                    self.item = 0
    

    '''-----保存解析点、导出视频数据-----'''
    def save(self):  # 保存解析点
        radio,ok= Dialog.getResult(self)
        if ok:
            name = QFileDialog.getSaveFileName(self, 'Save File',self.pkl, "Pickle Files (*.pkl)")
            if name[0]:   
                if radio:
                    if self.cut1 != None and self.cut2:
                        data = self.data[self.cut1:self.cut2 + 1]
                        with open(name[0], 'wb') as file1:
                            pickle.dump(data,file1)
                    else:
                        QMessageBox.warning(self,'警告','未设置工作区')
                else:
                    with open(name[0], 'wb') as file1:
                        pickle.dump(self.data,file1)
    
    def exportVideo(self):  # 导出带解析点视频
        if self.video:      
            radio,ok= Dialog.getResult(self)
            if ok:
                path = QFileDialog.getSaveFileName(self, '保存视频', os.getcwd(), "MP4(*.mp4)")
                if path[0]:
                    cap = cv2.VideoCapture(self.video) 
                    fpsRate = cap.get(cv2.CAP_PROP_FPS)  # 获取视频帧率
                    fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # 设置写入视频的编码格式
                    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # 获取视频宽度
                    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 获取视频高度
                    videoWriter = cv2.VideoWriter(path[0], fourcc, fpsRate, (frame_width, frame_height))
                    i = 0
                    while cap:
                        ret,fram = cap.read()
                        if ret == True:
                            if radio:
                                if self.cut1 != None and self.cut2:
                                    if self.cut1 <= i <= self.cut2:
                                        if self.pkl:
                                            now = self.data[i]
                                            for d in now:                               
                                                calculation.draw(fram,d,type = self.drawPoint)
                                        videoWriter.write(fram)
                                        cv2.imshow('Video exporting...(Press ESC to Exit)',fram)
                                        if cv2.waitKey(20) & 0xFF == 27:
                                            break
                                else:
                                    QMessageBox.warning(self,'警告','未设置工作区')
                                    break
                            else:
                                if self.pkl:
                                    now = self.data[i]
                                    for d in now:                               
                                        calculation.draw(fram,d,type = self.drawPoint)
                                videoWriter.write(fram)
                                cv2.imshow('Video exporting...(Press ESC to Exit)',fram)
                                if cv2.waitKey(20) & 0xFF == 27:
                                    break
                        else:
                            break
                        i += 1
                    cap.release()
                    cv2.destroyAllWindows()

    def exportPointlessVideo(self):  # 导出无解析点视频
        if self.video:   
            path = QFileDialog.getSaveFileName(self, '保存视频', os.getcwd(), "MP4(*.mp4)")
            if path[0]:
                cap = cv2.VideoCapture(self.video) 
                fpsRate = cap.get(cv2.CAP_PROP_FPS)  # 获取视频帧率
                fourcc = cv2.VideoWriter_fourcc(*"mp4v")  # 设置写入视频的编码格式
                frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # 获取视频宽度
                frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # 获取视频高度
                videoWriter = cv2.VideoWriter(path[0], fourcc, fpsRate, (frame_width, frame_height))
                i = 0
                while cap:
                    ret,fram = cap.read()
                    if ret == True:
                        if self.cut1 != None and self.cut2:
                            if self.cut1 <= i <= self.cut2:                                  
                                videoWriter.write(fram)
                                cv2.imshow('Video exporting...(Press ESC to Exit)',fram)
                                if cv2.waitKey(20) & 0xFF == 27:
                                    break
                        else:
                            QMessageBox.warning(self,'警告','未设置工作区')
                            break
                    else:
                            break
                    i += 1
                cap.release()
                cv2.destroyAllWindows()

    def exportKeys(self):  # 导出解析点数据
        path = QFileDialog.getSaveFileName(self, '导出坐标点', os.getcwd(), "CSV(*.csv)")
        name = ['0 鼻子', '1 脖子', '2 右肩', '3 右肘','4 右腕','5 左肩','6 左肘','7 左腕','8 中臀','9 右臀',
                '10 右膝','11 右踝','12 左臀','13 左膝','14 左踝','15 右眼','16 左眼','17 右耳','18 左耳',
                '19 左大拇指','20 左小拇指','21 左足跟','22 右大拇指','23 右小拇指','24 右足跟']
        title = []
        for n in name:
            title.append(n + 'X')
            title.append(n + 'Y')
        with open(path[0], 'w', newline = '') as file1:
            f = csv.writer(file1)
            f.writerow(title)
            if self.data:
                for d in self.data:    
                    d1 = np.delete(d[0],-1,axis = 1)     
                    line = d1.flatten()  # 转成一维数组
                    f.writerow(line)        
        QMessageBox.information(self, '消息', '坐标点数据已导出')
    
    def exportResults(self):  # 导出结果
        name = QFileDialog.getSaveFileName(self, '导出运动学结果', self.cwd, "CSV Files (*.csv)")
        if name[0]:
            with open(name[0], 'w', newline='') as file1:
                file0 = csv.writer(file1)
                last = 0
                t = True
                f_num = 0
                if self.cut1 != None and self.cut2 != None:
                    for f in range(self.cut1,self.cut2 + 1):
                        try:
                            now  = self.data[f][0]
                            if f > 0:
                                last = self.data[f-1][0]
                            result = calculation.para(now, last, self.fpsRate, self.pc, self.rotationAngle) 
                            if t == True:
                                title = ['帧数']
                                for key in result.keys():
                                    title.append(key)
                                file0.writerow(title)
                                t = False
                            row_v = [f_num]
                            for value in result.values():
                                row_v.append(value)
                            file0.writerow(row_v)
                            f_num += 1
                        except Exception as e:
                            print(e)
                            break
                            
                else:
                    for f in range(len(self.data)):
                        try:
                            now  = self.data[f][0]
                            if f > 0:
                                last = self.data[f-1][0]
                            result = calculation.para(now, last, self.fpsRate, self.pc, self.rotationAngle) 
                            if f == 0:
                                title = ['帧数']
                                for key in result.keys():
                                    title.append(key)
                                file0.writerow(title)
                            row_v = [f]
                            for value in result.values():
                                row_v.append(value)
                            file0.writerow(row_v)
                        except Exception as e:
                            print(e)
                            break

    '''-----选择工作区-----'''
    def workspaceStart(self):
        cut = self.fps
        if self.cut2 == None or cut < self.cut2:
            self.cut1 = cut
            range_text = '工作区开始：{}帧        工作区结束：{}帧'.format(self.cut1,self.cut2)
            self.label_4.setText(range_text)
        if self.cut1 and self.cut2:
            self.pushButton_5.setEnabled(True)
    def workspaceEnd(self):
        cut = self.fps
        if self.cut1 == None or cut > self.cut1:
            self.cut2 = cut
            range_text = '工作区开始：{}帧        工作区结束：{}帧'.format(self.cut1,self.cut2)
            self.label_4.setText(range_text)
        if self.cut1 and self.cut2:
            self.pushButton_5.setEnabled(True)

    def workspaceClear(self):
        self.cut1 = None
        self.cut2 = None
        range_text = '工作区开始：{}帧        工作区结束：{}帧'.format(self.cut1,self.cut2)
        self.label_4.setText(range_text)
        self.pushButton_5.setEnabled(False)
    
    def jumpToBeginning(self):
        if self.cut1 != None:
            self.horizontalSlider.setSliderPosition(self.cut1)
            self.sli_label()

    def jumpToEnd(self):
        if self.cut2:
            self.horizontalSlider.setSliderPosition(self.cut2)
            self.sli_label()

    def play(self):  # 播放
        if self.play2:
            self.play2 = False
            icon7 = QIcon()
            icon7.addPixmap(QPixmap("Icon/播放(1).png"), QIcon.Normal, QIcon.Off)
            self.pushButton_10.setIcon(icon7)
            self.pushButton_10.setIconSize(QSize(48, 48))
        else:
            self.play2 = True 
            icon72 = QIcon()
            icon72.addPixmap(QPixmap("Icon/暂停.png"), QIcon.Normal, QIcon.Off)
            self.pushButton_10.setIcon(icon72)
            self.pushButton_10.setIconSize(QSize(48, 48))
        cap = self.cap
        cap.set(cv2.CAP_PROP_POS_FRAMES,self.fps)  # 显示指定帧的画面 
        while cap:
            rval,frame = cap.read()
            if rval:
                if self.play2:
                    f = cap.get(1) -1
                    if f >= self.fps:
                        self.horizontalSlider.setSliderPosition(f)
                        if cv2.waitKey(20) & 0xFF == 27:
                            break  
                else:
                    break
            else:
                self.horizontalSlider.setSliderPosition(0)
                self.play2 = False
                icon7 = QIcon()
                icon7.addPixmap(QPixmap("Icon/播放(1).png"), QIcon.Normal, QIcon.Off)
                self.pushButton_10.setIcon(icon7)
                self.pushButton_10.setIconSize(QSize(48, 48))
                break

    '''-----测量-----'''
    def lengthButton(self):  # 测量长度
        self.long = True
        self.lengthPoint = []
        
    def length(self):  # 测量长度
        if self.long == True:
            x1 = self.imgLabel.x
            y1 = self.imgLabel.y
            x1 = int(x1 / self.scaleFactor + 0.5)
            y1 = int(y1 / self.scaleFactor + 0.5)
            self.lengthPoint.append((x1,y1))
            # 重新读取图像并画图
            cap = self.cap
            cap.set(cv2.CAP_PROP_POS_FRAMES,self.fps)  
            rval,frame = cap.read()
            for p in self.lengthPoint:
                cv2.circle(frame,p,5,(200,200,0),3)
            frame=cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
            imge = QImage(frame.data,frame.shape[1],frame.shape[0],QImage.Format_RGB888)
            self.imgLabel.setPixmap(QPixmap.fromImage(imge))
            if len(self.lengthPoint) >= 2:
                self.long = False
                long = ((self.lengthPoint[0][0] - self.lengthPoint[1][0]) ** 2 + (self.lengthPoint[0][1] - self.lengthPoint[1][1]) ** 2) ** 0.5  # 像素长度
                unit = 'Px'
                if self.pc:
                    long = long/self.pc  # 真实长度
                    unit = '米'
                text = '当前测量长度：{}{}'.format(round(long,2),unit)
                name, ok = QInputDialog.getText(self, '测量长度', text, QLineEdit.Normal, '输入该长度名称并在结果中显示')
                if ok:
                    self.longDic[name] = round(long,2)
                    self.showResult()
          
    def timeButton(self):  # 测量时间点
        now = self.fps
        self.timePoint.append(now)
        if len(self.timePoint) >= 2:
            time = (self.timePoint[1] - self.timePoint[0])/self.fpsRate
            self.timePoint = []
            text = '当前测量时间：{}秒'.format(round(time,2))
            name, ok = QInputDialog.getText(self, '测量时间', text, QLineEdit.Normal, '输入该时间名称并在结果中显示')
            if ok:
                self.timeDic[name] = round(time,2)
                self.showResult()

    def levelButton(self):  # 标定水平、垂直线
        self.level = True
        self.levelPoint = []
        
    def levelTool(self):  # 画水平、垂直点
        if self.level == True:
            x1 = self.imgLabel.x
            y1 = self.imgLabel.y
            x1 = int(x1 / self.scaleFactor + 0.5)
            y1 = int(y1 / self.scaleFactor + 0.5)
            self.levelPoint.append((x1,y1))
            # 重新读取图像并画图
            cap = self.cap
            cap.set(cv2.CAP_PROP_POS_FRAMES,self.fps)  
            rval,frame = cap.read()
            for p in self.levelPoint:
                cv2.circle(frame,p,5,(200,200,0),-1)
                if len(self.levelPoint) >= 2:
                    cv2.line(frame,self.levelPoint[0],p,(200,200,0),2)
            frame=cv2.cvtColor(frame,cv2.COLOR_RGB2BGR)
            imge = QImage(frame.data,frame.shape[1],frame.shape[0],QImage.Format_RGB888)
            self.imgLabel.setPixmap(QPixmap.fromImage(imge))
            if len(self.levelPoint) >= 2:
                self.level = False
                p1 = self.levelPoint[0]
                p2 = self.levelPoint[1]
                x = p2[0] - p1[0]
                y = p2[1] - p1[1]
                angle = math.atan2(y,x)
                angle = round(angle * 180/math.pi, 2)  # 与水平线夹角
                items = ['水平线','垂直线']
                Item, ok = QInputDialog.getItem(self,'水平仪','当前测量的是：',items,0,False)
                if ok and Item:
                    select = items.index(Item)
                    if select == 0:
                        self.rotationAngle = angle
                    else:
                        self.rotationAngle = round(90 - angle, 2)
                    self.showResult()
                    self.text(i = 1)

    def pointType(self):  # 显示图像类型
        items = ['线','点']
        item,ok = QInputDialog.getItem(self,'类型','选择：',items,0,False)
        if ok and item:
            self.drawPoint = items.index(item)

    '''-----dockwidget-----'''
    def dockEvent(self):
        if self.actionmanager.isChecked():
            self.dockWidget.setVisible(True)
        else:
            self.dockWidget.setVisible(False)
        if self.actionshowWin.isChecked():
            self.dockWidget_2.setVisible(True)
        else:
            self.dockWidget_2.setVisible(False)
    
    '''-----字体大小-----'''
    def fontSize(self):
        size,ok = QInputDialog.getInt(self,'字体大小','',15,5,200,1)
        if ok and size:
            font = QFont()
            font.setPointSize(size)
            self.tableWidget.setFont(font)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = GoPose()
    win.showMaximized()
    # win.show()
    sys.exit(app.exec_())