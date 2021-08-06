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
import cv2
import math
from modules.center import core

# 3点求角度
def degree(A,B,C):  # A上端点，B中间点夹角点，C下端点
    BA = ((A[0] - B[0]) ** 2 + (A[1] - B[1]) ** 2) ** 0.5
    BC = ((C[0] - B[0]) ** 2 + (C[1] - B[1]) ** 2) ** 0.5
    cosB = ((A[0] - B[0]) * (C[0] - B[0]) + (A[1] - B[1]) * (C[1] - B[1]))/(BA * BC)
    rB = math.acos(cosB)
    degree = math.degrees(rB)
    return degree

# 4点求角度
def angle(v1, v2, v3, v4):  # v1上端中，v2上远，v3下中，v4下远 
    dx1 = v2[0] - v1[0]
    dy1 = v2[1] - v1[1]
    dx2 = v4[0] - v3[0]
    dy2 = v4[1] - v3[1]
    angle1 = math.atan2(dy1, dx1)
    angle1 = round(angle1 * 180/math.pi, 2)
    angle2 = math.atan2(dy2, dx2)
    angle2 = round(angle2 * 180/math.pi, 2)
    if angle1*angle2 >= 0:
        included_angle = abs(angle1-angle2)
    else:
        included_angle = abs(angle1) + abs(angle2)
        if included_angle > 180:
            included_angle = 360 - included_angle
    return included_angle

# 与水平线、垂线夹角
def level(p1,p2,r,line = 0):
    x = p2[0] - p1[0]
    y = p2[1] - p1[1]
    angle = math.atan2(y,x)
    angle = angle * 180/math.pi  # 与水平线夹角
    if angle > 90 or angle < -90:
        angle = 180 - angle
        if angle > 180:
            angle = 360-angle
    if line:  # 与垂线夹角
        angle = 90 - angle
    angle = round(abs(angle - r),2)
    return angle

# 计算参数
def para(frame_now,frame_last,fps_video,pc,r):  # 当前帧，上一帧，帧率，比例尺,r画面旋转角
        ind = frame_now  # 当前帧的关键点
        # 关节角
        r_hip = round(angle(ind[8],ind[1],ind[9],ind[10]),2)
        l_hip = round(angle(ind[9],ind[1],ind[12],ind[13]),2)
        r_knee = round(degree(ind[9],ind[10],ind[11]),2)
        l_knee = round(degree(ind[12],ind[13],ind[14]),2)
        rAnkle = round(angle(ind[11],ind[10],ind[24],ind[22]))
        lAnkle = round(angle(ind[14],ind[13],ind[21],ind[19]))
        # r_elbow = round(degree(ind[2],ind[3],ind[4]),2)
        # l_elbow = round(degree(ind[5],ind[6],ind[7]),2)
        # 空间夹角
        bodyV = level(ind[1],ind[8],r,line = 1)
        rThighH = level(ind[9],ind[10],r)
        lThighH = level(ind[12],ind[13],r)
        rShankH = level(ind[10],ind[11],r)
        lShankH = level(ind[13],ind[14],r)
        # 质心距离
        core1 = core(ind)  # 当前帧质心坐标
        if pc != None:
            rCoreFoot = round(abs(core1[0] - ind[22][0])/pc, 2)
            lCoreFoot = round(abs(core1[0] - ind[19][0])/pc, 2)
            
        else:
            rCoreFoot = '比例尺缺失'
            lCoreFoot = '比例尺缺失'
        speed_x = None
        speed_y = None
        r_hip_w = None
        l_hip_w = None
        r_knee_w = None
        l_knee_w = None
        rToeHSpeed = None  # 右足尖速度
        lToeHSpeed = None
        # ax = None
        # ay = None
        # Fx = None
        # Fy = None
        # Px = None
        if type(frame_last) != int and frame_last is not None:  # 如果不是整型，说明不是第一帧
            ind_l = frame_last  # 前一帧关键点坐标
            core0 = core(ind_l) 
            # 角速度
            r_hip0 = round(angle(ind_l[8],ind_l[1],ind_l[9],ind_l[10]),2)
            l_hip0 = round(angle(ind_l[9],ind_l[1],ind_l[12],ind_l[13]),2)
            r_knee0 = round(degree(ind_l[9],ind_l[10],ind_l[11]),2)
            l_knee0 = round(degree(ind_l[12],ind_l[13],ind_l[14]),2)
            # r_elbow0 = round(degree(ind_l[2],ind_l[3],ind_l[4]),2)
            # l_elbow0 = round(degree(ind_l[5],ind_l[6],ind_l[7]),2)
            r_hip_w = round((r_hip - r_hip0) * fps_video, 2) # 角速度
            l_hip_w = round((l_hip - l_hip0) * fps_video, 2)
            r_knee_w = round((r_knee - r_knee0) * fps_video, 2)
            l_knee_w = round((l_knee - l_knee0) * fps_video, 2)
            if pc != None:
                speed_x = round((core1[0] - core0[0]) * fps_video / pc, 2)  # 瞬时水平速度
                speed_y = round((core1[1] - core0[1]) * fps_video / pc, 2)  # 瞬时水平速度
                rToeHSpeed = round((ind[22][0] - ind_l[22][0]) * fps_video / pc, 2)
                lToeHSpeed = round((ind[19][0] - ind_l[19][0]) * fps_video / pc, 2)
            else:
                speed_x = '比例尺缺失'
                speed_y = '比例尺缺失'
                rToeHSpeed = '比例尺缺失'
                lToeHSpeed = '比例尺缺失'
        result = {'质心坐标':core1,
                '右髋角(°)':r_hip, '右膝角(°)':r_knee, '右踝角(°)':rAnkle, '左髋角(°)':l_hip, '左膝角(°)':l_knee, '左踝角(°)':lAnkle, 
                '躯干-垂线角(°)':bodyV, '右大腿-水平角(°)':rThighH, '右小腿-水平角(°)':rShankH, '左大腿-水平角(°)':lThighH, '左小腿-水平角(°)':lShankH, 
                '右髋角速度(°/s)':r_hip_w, '左髋角速度(°/s)':l_hip_w, '右膝角速度(°/s)':r_knee_w, '左膝角速度(°/s)':l_knee_w,
                '质心-右足水平距离(m)':rCoreFoot, '质心-左足水平距离(m)':lCoreFoot, 
                '质心水平速度(m/s)':speed_x, '质心垂直速度(m/s)':speed_y,
                '右足尖水平速度(m/s)':rToeHSpeed, '左足尖水平速度(m/s)':lToeHSpeed
                }   #  '水平加速度(m/s2)':ax, '垂直加速度(m/s2)':ay, '地面水平力(N)':Fx, '地面垂直力(N)':Fy, 'x功率(W)':Px
                #  '右肘角(°)':r_elbow, '左肘角(°)':l_elbow,  
        return result

# 显示棍图
def draw(frame, now, lineSize, type = 0):
    try:
        circleSize = lineSize * 2
        def line(frame,p0,p1,color):  # 画线
            if p0 != (0.0,0.0) and p1 != (0.0,0.0):
                cv2.line(frame,p0,p1,color, lineSize)
                cv2.circle(frame, p1, circleSize, color, -1)
        def p(num):  # 取25坐标点
            return (now[num][0],now[num][1])  # 把self.now改为now   
        if type == 0:
                core1 = core(now)
                cv2.circle(frame, core1, circleSize + 1, (255,200,0), lineSize)  # 重心
                body = (255,255,255)  # 躯干颜色  RGB51,204,153  BGR
                rUpperLimb = (255,102,0)  # 右上肢颜色
                lUpperLimb = (0,255,102)  # 左上肢颜色
                rLeg = (51,0,255)  # 右腿颜色
                lLeg = (0,255,255)  # 左腿颜色
                line(frame,p(0),p(1),body)  # 躯干
                line(frame,p(1),p(8),body)
                line(frame,p(1),p(2),rUpperLimb)  # 右手
                line(frame,p(2),p(3),rUpperLimb)
                line(frame,p(3),p(4),rUpperLimb) 
                line(frame,p(1),p(5),lUpperLimb)  # 左手
                line(frame,p(5),p(6),lUpperLimb)
                line(frame,p(6),p(7),lUpperLimb)
                line(frame,p(8),p(9),rLeg)  # 右腿
                line(frame,p(9),p(10),rLeg)
                line(frame,p(10),p(11),rLeg)
                line(frame,p(11),p(22),rLeg)
                line(frame,p(11),p(24),rLeg)              
                line(frame,p(22),p(24),rLeg)
                line(frame,p(8),p(12),lLeg)  # 左腿
                line(frame,p(12),p(13),lLeg)
                line(frame,p(13),p(14),lLeg)
                line(frame,p(14),p(19),lLeg)
                line(frame,p(14),p(21),lLeg)               
                line(frame,p(19),p(21),lLeg) 
                # line(frame,p(22),p(23),rLeg)  # 右小拇指 不重要
                # line(frame,p(19),p(20),lLeg)  # 左小拇指 不重要
                # line(frame,p(0),p(15),(51,0,204))  # 右眼   不重要
                # line(frame,p(15),p(17),(51,0,204))  # 不重要
                # line(frame,p(0),p(16),(0,102,0))  # 左眼   不重要
                # line(frame,p(16),p(18),(0,102,0))  # 不重要         
        elif type == 1:  # 选择画点 
            core1 = core(now)
            cv2.circle(frame,core1,4,(20,200,0),2)  # 质心
            for o in range(24):
                cv2.circle(frame,p(o),2,(0,255,0),2)
    except:
        print('画图错误')