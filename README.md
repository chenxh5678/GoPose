# GoPose人工智能运动分析系统
GoPose人工智能运动分析系统,可完成人体姿态25个关键点自动识别、编辑、导出结果等工作  
![image](https://github.com/chenxh5678/GoPose/blob/main/README/Image/1.gif)
## 项目背景
- 那年做毕业论文，用北体的视讯软件，半年时间逐帧逐点手动标记运动员的关键点，最终顺利完成论文，非常感谢视讯  
- 但手动标点使人非常疲惫，并且会耗费大量时间，不利于运动训练中给运动员即时反馈，应用局限在了科学研究。“如果有自动识别关键点的功能该多好”的想法那时诞生  
- 最近闲，实现一下当年的想法  
## 安装配置
### 1 环境
推荐Window10、python3.7、CUDA11.2
### 2 下载GoPose项目
- Windows：可以Download ZIP或使用GitHub桌面或从Powershell克隆  
- cmd控制台，按需求文档`GoPose/requirements.txt`安装库
### 3 配置OpenPose
- 下载安装好OpenPose（[官方文档](https://github.com/CMU-Perceptual-Computing-Lab/openpose)、[bilibili](https://www.bilibili.com/video/BV1WV411v7aj)）  
- 进入openpose中自己`build`的文件夹，将`openpose/build/`内的bin文件夹复制到`GoPose/resource/`中，替换同名文件  
- 将openpose文件夹中，`models`文件夹复制到`GoPose/resource/`中，替换同名文件,目前只用到`pose/body25/pose_iter_584000.caffemodel`  
- `openpose/build/python/openpose/Release/`内3个文件复制到`GoPose/resource/`内替换  
- `openpose/build/x64/Release/`内的openpose.dll复制到`GoPose/resource/`内替换  
![image](https://github.com/chenxh5678/GoPose/blob/main/README/Image/bin.png)  
![image](https://github.com/chenxh5678/GoPose/blob/main/README/Image/models.png)  
![image](https://github.com/chenxh5678/GoPose/blob/main/README/Image/resource.png)  
## 使用方法
执行GoPose.py文件  
[示例]()
## 人体姿态识别精度
## 即将到来
- [ ] 滤波平滑功能
- [ ] 手动标点功能
- [ ] 更多的运动学结果
- [ ] 合成三维坐标点功能
- [ ] 完善摄像头采集功能
- [ ] 显示坐标点轨迹模式
- [ ] 更多的人体惯性参数模型
- [ ] 测试对象信息栏的应用
- [ ] 可选增加手部和面部关键点识别，全身
## 相关项目
自动姿态识别功能来源：
- [OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose)
## 许可证
