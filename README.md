# GoPose人工智能运动分析软件  
- GoPose可以自动进行人体姿态25个关键点识别，方便进行运动技术分析，提供关节角度、位移速度等常用运动学结果，帮助运动员、教练员及体育科研工作者快速得到基础分析结果。
- GoPose可用于比赛、训练、科研等场景，其优势是无接触式测量、快速反馈、免费开源等，解决QUA..SYS等实验室设备需复杂穿戴、F***move人工智能运动分析系统等软件使用价格高昂等问题，帮助广大基层教练员、运动员科学化训练。GoPose存在的劣势主要是软件安装使用需要一定电脑知识、对电脑系统CPU显卡等有一定要求、更多功能需要完善更新。 

![image](https://github.com/chenxh5678/GoPose/blob/main/README/Image/1.gif)
## 项目背景
- 那年做毕业论文，用北体的视迅软件，半年时间逐帧逐点手动标记运动员的关键点，最终顺利完成论文，非常感谢视迅  
- 但手动标点使人非常疲惫，并且会耗费大量时间，不利于运动训练中给运动员即时反馈。“如果有自动识别关键点的功能该多好”的想法那时诞生  
- 最近闲，实现一下当年的想法  
## 安装配置
### 1 环境
- python3.7(其他版本会报错 2021年8月)  
- 推荐Window10、CUDA11.2
### 2 下载GoPose
- Windows：Download ZIP或使用GitHub桌面等 
- cmd控制台，按需求文档`GoPose/requirements.txt`安装库
### 3 配置姿态估计模块
- 下载安装OpenPose（[官方文档](https://github.com/CMU-Perceptual-Computing-Lab/openpose)、[bilibili](https://www.bilibili.com/video/BV1WV411v7aj)、[bilibili快速安装](https://www.bilibili.com/video/BV1uK411w74E)）  
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
- 运行GoPose.py文件  
- [使用演示](https://www.bilibili.com/video/BV1QP4y1s76N/)
- 查看坐标点折线图、快速修正坐标点、对坐标点进行滤波平滑：  
  ![image](https://github.com/chenxh5678/GoPose/blob/main/README/Image/%E4%BF%AE.png) 
- 可将运动学结果导出，用于统计记录：  
  ![image](https://github.com/chenxh5678/GoPose/blob/main/README/Image/%E7%BB%93%E6%9E%9Ccsv.png) 
- 可将坐标点导出用于进一步分析：  
  ![image](https://github.com/chenxh5678/GoPose/blob/main/README/Image/%E5%9D%90%E6%A0%87.png) 
- 运动训练监控：训练场上快速查看技术动作及运动学结果，及时反馈给教练员、运动员：  
  ![image](https://github.com/chenxh5678/GoPose/blob/main/README/Image/%E7%BB%93%E6%9E%9C.png)
## 姿态估计结果  
Results on COCO test-dev 2015:  

| AP @0.5:0.95 | AP @0.5 | AP @0.75 | AP medium | AP large  
| :----: | :----: | :----: | :----: | :----: 
| 61.8 | 84.9 | 67.5 | 57.1 | 68.2  


Results on MPII full test set:  
|Head	|Shoulder	|Elbow	|Wrist	|Hip	|Knee	|Ankle	|Ave
| :----: | :----: | :----: | :----: | :----: | :----: | :----: | :----:  
|91.2	|87.6	|77.7	|66.8	|75.4	|68.9	|61.7	|75.6  

## 未来要做的
- [X] 滤波平滑功能：管理器-单击解析点修正并勾选-显示窗口-右键解析点名称
- [X] 坐标点折线图中快速修改功能：管理器-勾选解析点修正-显示窗口-右键解析点名称
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
- [OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose)
## 版权许可协议
免费使用，但须遵守[版权许可协议](https://github.com/chenxh5678/GoPose/blob/main/LICENSE)
## 赞赏
如果对您有帮助，可以[请开发者喝一杯](https://github.com/chenxh5678/GoPose/blob/main/README/Image/%E8%AF%B7%E5%BC%80%E5%8F%91%E8%80%85%E5%96%9D%E4%B8%80%E6%9D%AF.jpg)吗^_^