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
def core(data):  # 输入一帧25点数据
    # 25点名称与索引值
    name = ['0 鼻子', '1 脖子', '2 右肩', '3 右肘','4 右腕','5 左肩','6 左肘','7 左腕','8 中臀','9 右臀',
                '10 右膝','11 右踝','12 左臀','13 左膝','14 左踝','15 右眼','16 左眼','17 右耳','18 左耳',
                '19 左大拇指','20 左小拇指','21 左足跟','22 右大拇指','23 右小拇指','24 右足跟']

    # 重心计算有小错误，待修正，待添加女子重心模型
    #所有的x
    headx=data[0][0]  
    neckx=data[1][0]  # 第1号点的x，脖子
    bodyx=data[1][0]-(data[1][0]-data[8][0])*0.52
    
    rightupperarmx=data[2][0]-(data[2][0]-data[3][0])*0.46
    rightforearmx=data[3][0]-(data[3][0]-data[4][0])*0.41
    righthandx = data[4][0]
    
    leftupperarmx=data[5][0]-(data[5][0]-data[6][0])*0.46
    leftforearmx=data[6][0]-(data[6][0]-data[7][0])*0.41
    lefthandx = data[7][0]

    leftthighx=data[12][0]-(data[12][0]-data[13][0])*0.42
    leftcalfx=data[13][0]-(data[13][0]-data[14][0])*0.41  
    leftfootx=data[21][0]-(data[21][0]-data[19][0])*0.5

    rightthighx=data[9][0]-(data[9][0]-data[10][0])*0.42
    rightcalfx=data[10][0]-(data[10][0]-data[11][0])*0.41
    rightfootx=data[24][0]-(data[24][0]-data[22][0])*0.5
    #所有的y
    heady=data[0][1]
    necky=data[1][1]  # 第1号点的y，脖子
    bodyy=data[1][1]-(data[1][1]-data[8][1])*0.52

    rightupperarmy=data[2][1]-(data[2][1]-data[3][1])*0.46
    rightforearmy=data[3][1]-(data[3][1]-data[4][1])*0.41
    righthandy = data[4][1]
    
    leftupperarmy=data[5][1]-(data[5][1]-data[6][1])*0.46
    leftforearmy=data[6][1]-(data[6][1]-data[7][1])*0.41
    lefthandy = data[7][1]

    leftthighy=data[12][1]-(data[12][1]-data[13][1])*0.42
    leftcalfy=data[13][1]-(data[13][1]-data[14][1])*0.41
    leftfooty=data[21][1]-(data[21][1]-data[19][1])*0.5

    rightthighy=data[9][1]-(data[9][1]-data[10][1])*0.42
    rightcalfy=data[10][1]-(data[10][1]-data[11][1])*0.41
    rightfooty=data[24][1]-(data[24][1]-data[22][1])*0.5
    
    centerofgravityx=0.044*headx+0.033*neckx+0.479*bodyx+0.0265*(rightupperarmx+leftupperarmx)+0.015*(rightforearmx+leftforearmx)+0.009*(righthandx+lefthandx)+0.1*(rightthighx+leftthighx)+0.0535*(rightcalfx+leftcalfx)+0.019*(rightfootx+leftfootx)
    centerofgravityy=0.044*heady+0.033*necky+0.479*bodyy+0.0265*(rightupperarmy+leftupperarmy)+0.015*(rightforearmy+leftforearmy)+0.009*(righthandy+lefthandy)+0.1*(rightthighy+leftthighy)+0.0535*(rightcalfy+leftcalfy)+0.019*(rightfooty+leftfooty)
    
    # 重心
    x = int(centerofgravityx)
    y = int(centerofgravityy)
    core = (x,y)  
    return core  
