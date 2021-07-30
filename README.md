# GoPose
GoPose是人体姿态关键点自动识别、编辑软件，同时可作为运动学分析软件  
## Background
那年做毕业论文，用北体的**视讯**软件，半年时间逐帧逐点手动标记运动员的关键点，最终顺利完成论文，非常感谢视讯  
但手动标点工作会耗费大量时间、使人疲惫，“如果有自动识别关键点的功能该多好”的想法那时诞生  
最近闲，实现一下当年的想法  
## Installation
1 首先需要安装好OpenPose（[官方文档](https://github.com/CMU-Perceptual-Computing-Lab/openpose)、[bilibili](https://www.bilibili.com/video/BV1WV411v7aj)）  
2 进入openpose中自己build的文件夹，将里面的bin文件夹复制到'GoPose/resource/'中，替换同名文件  
3 将openpose文件夹中，models文件夹复制到'GoPose/resource/'中，替换同名文件  
4 'openpose/build/python/openpose/Release/'内3个文件复制到'GoPose/resource/'内替换  
5 'openpose/build/x64/Release/'内的openpose.dll复制到'GoPose/resource/'内替换  

## Usage
## Comming soon
## Related Efforts
自动识别功能来源  
[OpenPose](https://github.com/CMU-Perceptual-Computing-Lab/openpose)

## License
