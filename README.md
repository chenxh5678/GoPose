# GoPose
GoPose是人体姿态关键点自动识别、编辑软件；人工智能运动分析软件
## Background
- 那年做毕业论文，用北体的**视讯**软件，半年时间逐帧逐点手动标记运动员的关键点，最终顺利完成论文，非常感谢视讯  
- 但手动标点工作会耗费大量时间、使人疲惫，“如果有自动识别关键点的功能该多好”的想法那时诞生  
- 最近闲，实现一下当年的想法  
## Installation
### 1 环境
推荐Window10、python3.7、CUDA11.2
### 2 下载GoPose存储库
- Windows：可以Download ZIP或使用GitHub桌面或从Powershell克隆  
- cmd控制台，按需求文档requirements.txt安装库
### 3 配置OpenPose
- 首先需要安装好OpenPose（[官方文档](https://github.com/CMU-Perceptual-Computing-Lab/openpose)、[bilibili](https://www.bilibili.com/video/BV1WV411v7aj)）  
- 进入openpose中自己`build`的文件夹，将里面的bin文件夹复制到`GoPose/resource/`中，替换同名文件  
- 将openpose文件夹中，`models`文件夹复制到`GoPose/resource/`中，替换同名文件,目前只用到`pose/body25/pose_iter_584000.caffemodel`  
- `openpose/build/python/openpose/Release/`内3个文件复制到`GoPose/resource/`内替换  
- `openpose/build/x64/Release/`内的openpose.dll复制到`GoPose/resource/`内替换  
## Usage
执行GoPose.py文件  
[示例]()
## Comming soon
- [ ] 滤波平滑功能
- [ ] 手动标点功能
- [ ] 更多的运动学结果
- [ ] 合成三维坐标点功能
- [ ] 完善摄像头采集功能
- [ ] 显示坐标点轨迹模式
- [ ] 更多的人体惯性参数模型
- [ ] 测试对象信息栏的应用
## Related Efforts
自动姿态识别功能来源：
- [OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose)
## License
