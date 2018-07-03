#This code comes from: https://github.com/becomequantum/kryon
from PIL import Image,ImageDraw,ImageFont
import numpy as np
#This code is only about animation. 本代码只是和做演示动画相关.
VideoSize = (1280, 720)
DemoImageSize = (48, 36)
标题位置 = (60, 16)
注释1位置 = (1000, 76)
网格位置 = (32, 76)
比例 = 17
网格颜色 = (230, 230, 230)
网三位置 = (网格位置[0] + 比例 * DemoImageSize[0] + 比例 * 2, 网格位置[1])
网三比例 = 比例 * 2
坐标位置 = (网三位置[0], 网三位置[1] + 网三比例 * 3 + 5)
注释2位置 = (坐标位置[0], 坐标位置[1] + 比例 + 18)
副标题位置 = (注释2位置[0],注释2位置[1] + 350)
UnitTime = 0.1
ScanTime = 0.1
FinishTime = 0.1
frame_list = []

def 微软雅黑(Size):
    return ImageFont.truetype("msyh.ttf", Size)

def 方框(x, y, 位置, 比例):
    左上 = (位置[0] + x * 比例, 位置[1] + y * 比例)
    右下 = (位置[0] + x * 比例 + 比例, 位置[1] + y * 比例 + 比例)
    return [左上, 右下]

def 小方框(x, y, 位置, 比例):
    左上 = (位置[0] + x * 比例 + 2, 位置[1] + y * 比例 + 2)
    右下 = (位置[0] + x * 比例 + 比例 - 2, 位置[1] + y * 比例 + 比例 - 2)
    return [左上, 右下]

def 方块(x, y, 位置, 比例):
    左上 = (位置[0] + x * 比例 + 1, 位置[1] + y * 比例 + 1)
    右下 = (位置[0] + x * 比例 + 比例 - 1, 位置[1] + y * 比例 + 比例 - 1)
    return [左上, 右下]

def 完成框(ShapeInfo):
    左上 = (网格位置[0] + ShapeInfo[2][0] * 比例 - 1, 网格位置[1] + ShapeInfo[2][1] * 比例 - 1)
    右下 = (网格位置[0] + ShapeInfo[1][0] * 比例 + 比例 + 1, 网格位置[1] + ShapeInfo[1][1] * 比例 + 比例 + 1)
    return [左上, 右下]

def 反色(color):
    rcolor = (255 - color[0], 255 - color[1], 255 - color[2])
    return rcolor

def InitBackGround(ExampleImage, Title, subtitle, textcolor = (0, 162, 232), subtitlecolor = "orange", BgColor = (255, 255, 255), FPGA = False):
    back_ground_image = Image.new("RGB", VideoSize, BgColor)
    画 = ImageDraw.Draw(back_ground_image)
    画.text(标题位置,Title, fill = textcolor, font = 微软雅黑(30))
    画.text(副标题位置, subtitle, fill = subtitlecolor, font=微软雅黑(25))
    for y in range(DemoImageSize[1]):
        for x in range(DemoImageSize[0]):
            画.rectangle(方框(x, y, 网格位置, 比例), outline = 网格颜色)         #画大背景网格
            if not(ExampleImage[y, x ,0] == ExampleImage[y, x ,1] == ExampleImage[y, x ,0] == 255):
                画.rectangle(方块(x, y, 网格位置, 比例), fill = "black")         #画示例图片中的黑点
                ExampleImage[y, x] = [0, 0, 0]                                   #不是白点的都变成黑点
            if x<= 2 and y <= 2 :
                画.rectangle(方框(x, y, 网三位置, 网三比例), outline = 网格颜色) #画右边3x3小邻域网格
                if FPGA and (y == 1 or (y == 2 and x == 0)):
                    画.rectangle(方框(x, y - 1, 网三位置, 网三比例), outline = "blue")
    画.rectangle(方框(1, 1, 网三位置, 网三比例), outline = "red")
    return back_ground_image

def AddClip(bg_image, x, y, Neighbourhood3x3, LabelColor = None, diff = False, duration = UnitTime, Shape_info = None, 注释1 =" ", 注释2 =" "):
    标记 = ImageDraw.Draw(bg_image)
    if LabelColor != None :
        标记.rectangle(方块(x, y, 网格位置, 比例), fill = LabelColor, outline = None)  #画标记色块
    if diff:                                                                           #周围有两个不同标号点时
        标记.rectangle(小方框(x, y , 网格位置, 比例), outline = 反色(LabelColor))
    temp_image = bg_image.copy()
    画 = ImageDraw.Draw(temp_image)
    if Shape_info != None :
        标记.rectangle(完成框(Shape_info), outline = "red")
        画.rectangle(完成框(Shape_info), outline = "red")
    画.rectangle(方框(x, y, 网格位置, 比例), outline = "red")                          #画小红框
    画.text(注释1位置, 注释1, fill = "purple", font = 微软雅黑(25))
    画.text(注释2位置, 注释2, fill = LabelColor if (LabelColor != None) else "purple", font = 微软雅黑(25))
    画.text(坐标位置, str((x, y)), fill = "black", font = 微软雅黑(25))
    for y in range(3):
        for x in range(3):
            画.rectangle(方块(x, y, 网三位置, 网三比例), fill = tuple(Neighbourhood3x3[y, x]))
    [frame_list.append(np.array(temp_image)) for n in range (int(duration / UnitTime))]






    