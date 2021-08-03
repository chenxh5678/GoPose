# GoPose人工智能运动分析软件
GoPose人工智能运动分析软件  
可完成人体姿态25个关键点自动识别、编辑、导出结果等工作  
![image](https://github.com/chenxh5678/GoPose/blob/main/README/Image/1.gif)
## 项目背景
- 那年做毕业论文，用北体的视讯软件，半年时间逐帧逐点手动标记运动员的关键点，最终顺利完成论文，非常感谢视讯  
- 但手动标点使人非常疲惫，并且会耗费大量时间，不利于运动训练中给运动员即时反馈。“如果有自动识别关键点的功能该多好”的想法那时诞生  
- 最近闲，实现一下当年的想法  
## 安装配置
### 1 环境
推荐Window10、python3.7、CUDA11.2
### 2 下载GoPose项目
- Windows：Download ZIP或使用GitHub桌面或从Powershell克隆  
- cmd控制台，按需求文档`GoPose/requirements.txt`安装库
### 3 配置姿态估计模块
- 下载安装OpenPose（[官方文档](https://github.com/CMU-Perceptual-Computing-Lab/openpose)、[bilibili](https://www.bilibili.com/video/BV1WV411v7aj)）  
- 进入自己建的`build`文件夹，将`openpose/build/`内的bin文件夹复制到`GoPose/resource/`中，替换同名文件  
- 将openpose文件夹中，`models`文件夹复制到`GoPose/resource/`中，替换同名文件,目前只用到`pose/body25/pose_iter_584000.caffemodel`  
- `openpose/build/python/openpose/Release/`内3个文件复制到`GoPose/resource/`内替换  
- `openpose/build/x64/Release/`内的openpose.dll复制到`GoPose/resource/`内替换  

![image](https://github.com/chenxh5678/GoPose/blob/main/README/Image/bin.png)  
<center>bin文件夹图示</center>   


![image](https://github.com/chenxh5678/GoPose/blob/main/README/Image/models.png)  
<center>models文件夹图示</center>   


![image](https://github.com/chenxh5678/GoPose/blob/main/README/Image/resource.png)  
<center>resource文件夹图示</center>   

## 使用方法
运行GoPose.py文件  
[演示](https://www.bilibili.com/video/BV1QP4y1s76N/)
## 姿态估计结果  
Results on COCO test-dev 2015:  

| Method | AP @0.5:0.95 | AP @0.5 | AP @0.75 | AP medium | AP large  
| :----: | :----: | :----: | :----: | :----: | :----: 
| OpenPose (CMU-Pose)	| 61.8 | 84.9 | 67.5 | 57.1 | 68.2  


Results on MPII full test set:  
| Method	|Head	|Shoulder	|Elbow	|Wrist	|Hip	|Knee	|Ankle	|Ave
|:----: | :----: | :----: | :----: | :----: | :----: | :----: | :----: | :----:  
|OpenPose (CMU-Pose)	|91.2	|87.6	|77.7	|66.8	|75.4	|68.9	|61.7	|75.6  

## 未来要做的
- [ ] 滤波平滑功能
- [ ] 手动标点功能
- [ ] 更多的运动学结果
- [ ] 合成三维坐标点功能
- [ ] 完善摄像头采集功能
- [ ] 显示坐标点轨迹模式
- [ ] 更多的人体惯性参数模型
- [ ] '测试对象'信息栏的应用
- [ ] 根据硬件情况，可选增加手部和面部关键点识别，全部135个关键点
- [ ] 更精确、速度更快的姿态估计
## 相关项目
- 姿态估计功能来源： [OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose)
## 版权许可协议
免费使用，但必须遵守[版权许可协议](https://github.com/chenxh5678/GoPose/blob/main/LICENSE)