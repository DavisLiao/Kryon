#This code comes from: https://github.com/becomequantum/kryon
#下面这篇文章介绍了该算法的思路,The following article introduces the idea of the algorithm,it's in Chinese, but Google translate is good enough:
#http://blog.sina.com.cn/s/blog_539ee1ae0102xtod.html
from DrawVideo import *
import random
import time    #在出动画结果之前需要大约50s的时间运行. It may take 50s runtime before results show out.
import pygame  #如果动画不流畅,原因是内存不足.If the animation is not fluent, the reason is the lack of memory
import moviepy.editor as MovieEditor
#连通域识别算法动画演示代码. 本代码演示了两种连通域识别算法:
#一是用递归的方法实现, 这种方法需要随机读取数据, 在PC上很容易实现, 但并不适合FPGA并行流水线算法的实现.
#二是适合FPGA并行流水线实现的连通域识别算法, 只需缓存两行图像即可实现连通域识别. 不需要外接DDR
#Connected component labeling algorithm animation demo code. This code demonstrates two kinds of connected component labeling algorithm:
#The first is implemented by recursion. This method needs to read data randomly, it is easy to implement on PC, but it is not suitable for parallel pipeline processing on FPGA.
#The second one is suitable for FPGA parallel pipeline processing. It only needs to cache one lines of image data to implement connected component labeling algorithm. No DDR Needed.

time_start = time.time()
LabelColor = ((66, 55, 255), (55, 177, 211), (33, 144, 33), (211, 122, 66), (177, 199, 44), (255, 111, 177),(11, 211, 99), (122, 22, 119),
              (166, 155, 55), (155, 77, 211), (133, 44, 33), (211, 122, 166), (177, 99, 144), (55, 111, 177),(11, 11, 99), (22, 122, 199))
TestBMP = '48x36.bmp'
ExampleImage = np.array(Image.open(TestBMP))      #加载示例图片. Load example image
if ExampleImage.shape[0] != DemoImageSize[1] or ExampleImage.shape[1] != DemoImageSize[0]:
    print("算法演示图片尺寸必须是The Size of the demo image has to be: {}x{}!".format(DemoImageSize[0], DemoImageSize[1]))
    quit()

RecursionScanList = [1,2,4,10,16,21]    #控制要扫描多少行. Control how many lines to scan
FPGAScanList = list(range(1, min(DemoImageSize[1] - 1, 30)))
#---------------------------递归法 Recursive Method------------------------
bg_image = InitBackGround(ExampleImage,'连通域标记递归法演示 Connected Component Labeling Recursive Method Demo','该方法需要随机读取数据\nThis method needs random\nread data')
LabelCount = 1   #用来标记连通域的标号计数
DirectionList = [(0,1),(0,-1),(1,0),(1,1),(1,-1),(-1,-1),(-1,0),(-1,1)]       #8邻域. 8 Neighbourhoods Right,Left,Down...
random.shuffle(DirectionList)   #You can shuffle it for fun
Sum, XYmax, XYmin, Color  = 0, 1, 2, 3     #[Sum, [Xmax,Ymax],[Xmin,Ymin], color]

def LabelBlackDot(x, y, ShapeInfo):
    ExampleImage[y, x] = ShapeInfo[Color]                               #给该点标上颜色. Color this dot
    Neighbourhood3x3 = ExampleImage[y - 1 : y + 2, x - 1 : x + 2]
    ShapeInfo[Sum]   += 1                                               #统计信息. Get Statistics
    ShapeInfo[XYmax][0] = max(ShapeInfo[XYmax][0], x)
    ShapeInfo[XYmax][1] = max(ShapeInfo[XYmax][1], y)
    ShapeInfo[XYmin][0] = min(ShapeInfo[XYmin][0], x)
    ShapeInfo[XYmin][1] = min(ShapeInfo[XYmin][1], y)
    AddClip(bg_image, x, y, Neighbourhood3x3, LabelColor= ShapeInfo[Color], duration = ScanTime,
            注释1="黑点就来分析\nAnalise black dot",
            注释2="Number: {} 号连通域\n点数Num of dots: {}\n"
                    "XYmax: {} XYmin: {}".format(LabelCount, ShapeInfo[Sum], tuple(ShapeInfo[XYmax]), tuple(ShapeInfo[XYmin])))
    for D in DirectionList:
        x1, y1 = x + D[1],y + D[0]
        if ExampleImage[y1, x1, 0] == 0 :        #If there is any black dot in Neighbourhood, then recursively call 'LabelBlackDot'
            LabelBlackDot(x1, y1, ShapeInfo)     #如果该点邻域中还有其它未标记黑点,就递归调用 'LabelBlackDot'


#循环遍历图片寻找未标记黑点并标记它们. Loop traversing the image to find unlabeled black dots and label them.
for y in RecursionScanList:
    for x in range(1, DemoImageSize[0] - 1):
        Neighbourhood3x3 = ExampleImage[y - 1 : y + 2, x - 1 : x + 2]   #取3x3邻域
        if ExampleImage[y, x, 0] == ExampleImage[y, x, 1] ==  ExampleImage[y, x, 2] == 0:
            ShapeInfo = [0, [x, y], [x, y], LabelColor[int(LabelCount % len(LabelColor))]]  #标记并统计该连通域的点数以及最大最小坐标等信息. [Sum, [Xmax,Ymax],[Xmin,Ymin], color]
            LabelBlackDot(x, y, ShapeInfo)      #Label and Statistics the number of points and maximum and minimum coordinates of this connected component.
            AddClip(bg_image, x, y, Neighbourhood3x3, LabelColor = ShapeInfo[Color], Shape_info = ShapeInfo, duration = FinishTime,
                    注释1="完成一个标记\nFinish one labeling",
                    注释2="Number: {} 号连通域\n总点数Total Num of dots: {}\n"
                          "XYmax: {} XYmin: {}".format(LabelCount, ShapeInfo[Sum], tuple(ShapeInfo[XYmax]), tuple(ShapeInfo[XYmin])))
            print("Recursion: Label:{} Sum: {} XYmax: {} XYmin: {}".format(LabelCount, ShapeInfo[Sum],ShapeInfo[XYmax],ShapeInfo[XYmin] ))
            LabelCount += 1     #标完一个连通域后就+1. After finish one labeling, the LabelCount will += 1
        else:
            AddClip(bg_image, x, y ,Neighbourhood3x3, 注释1="白点或已标点就飘过\nSkip white and \nlabeled dot")


#----------------------------并行流水线法 FPGA Parallel Pipeline Method----------------------------
ExampleImage = np.array(Image.open(TestBMP))      #重新加载示例图片. Load example image again
bg_image = InitBackGround(ExampleImage, "连通域标记并行流水线法演示 FPGA Parallel Pipeline Method Demo",
                          "该方法只需顺序扫描一次\nThis method only sequentially\nscan once\n"
                          "More suitable for FPGA", textcolor= (77, 99 ,111), subtitlecolor = 'red', FPGA= True)
LabelCount = 1  #标记数组初值为0,所以标记不能为从0开始. Can not be Zero, because init value of LabelArray is 0
LabelArray = np.zeros((ExampleImage.shape[0], ExampleImage.shape[1]), np.int32) #新建一个用来存放标记值的数组. New array for storing labels
ShapeInfoList = [[0, [0, 0], [0, 0],(),0,0]]                                    #[Sum, [Xmax,Ymax],[Xmin,Ymin], color, RealLabel]
RealLabel, XLmax = 4, 5

def LabelThisDot(x, y, ShapeInfo):
    LabelArray[y, x] = ShapeInfo[RealLabel]             #在标记数组上做标记. Label this dot in Label Array
    ExampleImage[y, x] = ShapeInfo[Color]
    ShapeInfo[Sum] += 1                                 #统计信息. Get Statistics  [Sum, [Xmax,Ymax],[Xmin,Ymin], color]
    ShapeInfo[XYmax][0] = max(ShapeInfo[XYmax][0], x)
    ShapeInfo[XYmax][1] = max(ShapeInfo[XYmax][1], y)
    ShapeInfo[XYmin][0] = min(ShapeInfo[XYmin][0], x)
    ShapeInfo[XYmin][1] = min(ShapeInfo[XYmin][1], y)
    ShapeInfo[XLmax] = x                                #记录该行的x最大值,用于判断形状结束 Use this value to tell if a shape's labeling has been completed

for y in FPGAScanList:
    for x in range(1, DemoImageSize[0] - 1):
        Neighbourhood3x3 = ExampleImage[y - 1: y + 2, x - 1: x + 2]  # 取3x3邻域,仅用于动画显示. Only used for animation
        if ExampleImage[y, x, 0] == ExampleImage[y, x, 1] == ExampleImage[y, x, 2] == 0:  #black dot
            Left, UpLeft, Up, UpRight = LabelArray[y, x - 1], LabelArray[y - 1, x - 1], LabelArray[y - 1, x], LabelArray[y - 1, x + 1]  #左,左上,上,右上四点 4 dots: Left, Left Up, Up, Up Right
            Left, UpLeft, Up, UpRight = ShapeInfoList[Left][RealLabel], ShapeInfoList[UpLeft][RealLabel], ShapeInfoList[Up][RealLabel], ShapeInfoList[UpRight][RealLabel]
            NumOfLabeled = int(bool(Left)) + int(bool(UpLeft)) + int(bool(Up)) + int(bool(UpRight))  #统计这4点中有几个点是已经被标记了的. How many have already been Labeled in these 4 dots

            if NumOfLabeled == 0:
                ShapeInfo = [0, [x, y], [x, y], LabelColor[int(LabelCount % len(LabelColor))], LabelCount, x]
                LabelThisDot(x, y, ShapeInfo)
                ShapeInfoList.append(ShapeInfo)
                AddClip(bg_image, x, y, Neighbourhood3x3, LabelColor = ShapeInfo[Color], duration =ScanTime,
                        注释1="黑点就来分析\nAnalise black dot\nNew Start Dot!",
                        注释2="新黑点,周围没有已标记点\n用新标号标上\nNo Labeled dot around\nTag it with new Label: {}\n"
                              "总点数Total Num of dots: {}\nXYmax: {} XYmin: {}".format(LabelCount, ShapeInfo[Sum], tuple(ShapeInfo[XYmax]), tuple(ShapeInfo[XYmin])))
                LabelCount += 1

            elif ((Left != UpRight and Left > 0) or (UpLeft != UpRight and UpLeft > 0)) and UpRight > 0:  #Two different labeled dot around
                ShapeInfoLater = ShapeInfoList[UpRight]
                ShapeInfo = []
                if Left != UpRight and  Left > 0:
                    ShapeInfoList[UpRight][RealLabel] = ShapeInfoList[Left][RealLabel]
                    ShapeInfo = ShapeInfoList[Left]
                else:
                    ShapeInfoList[UpRight][RealLabel] = ShapeInfoList[UpLeft][RealLabel]
                    ShapeInfo = ShapeInfoList[UpLeft]

                ShapeInfo[Sum] += ShapeInfoLater[Sum]                                      #当一个黑点的左上4邻域中有两个标号不同的标记点时,就要把后面的标号改为前面的标号,
                ShapeInfo[XYmax][0] = max(ShapeInfo[XYmax][0], ShapeInfoLater[XYmax][0])   #并合把后面的数据合并到前面去
                ShapeInfo[XYmax][1] = max(ShapeInfo[XYmax][1], ShapeInfoLater[XYmax][1])   #When there are Two different labeled dot around a black dot, it needs to change later Label to formal Label,
                ShapeInfo[XYmin][0] = min(ShapeInfo[XYmin][0], ShapeInfoLater[XYmin][0])   #and combine later data to formal ones. This is a Key Step.
                ShapeInfo[XYmin][1] = min(ShapeInfo[XYmin][1], ShapeInfoLater[XYmin][1])
                ShapeInfo[XLmax]    = max(ShapeInfo[XLmax], ShapeInfoLater[XLmax])
                LabelThisDot(x, y, ShapeInfo)
                AddClip(bg_image, x, y, Neighbourhood3x3, LabelColor = ShapeInfo[Color], diff = True,
                        duration=ScanTime,
                        注释1="黑点就来分析\nAnalise black dot",
                        注释2="周围有两个标号不同的已标记点\n需把后面的标号映射到前面的标号\n把统计数据也合并过去\n并把这个点标上前面的标号\n"
                              "Two Labeled dot around\nNeeds map later label to\nprevious one and combine data\nand Tag it with pre label: {}\n"
                              "总点数Total Num of dots: {}\nXYmax: {} XYmin: {}".format(ShapeInfo[RealLabel],ShapeInfo[Sum], tuple(ShapeInfo[XYmax]), tuple(ShapeInfo[XYmin])))

            else:  #Only One Label value around
                if Left != 0:     ShapeInfo = ShapeInfoList[Left]
                elif UpLeft != 0: ShapeInfo = ShapeInfoList[UpLeft]
                elif Up != 0:     ShapeInfo = ShapeInfoList[Up]
                else:             ShapeInfo = ShapeInfoList[UpRight]
                LabelThisDot(x, y, ShapeInfo)
                AddClip(bg_image, x, y, Neighbourhood3x3, LabelColor = ShapeInfo[Color], duration= ScanTime,
                        注释1="黑点就来分析\nAnalise black dot",
                        注释2="该黑点周围只有一种已标标号\n用该标号标上\nOnly One Label value around\nTag it with this Label: {}\n"
                              "总点数Total Num of dots: {}\nXYmax: {} XYmin: {}".format(ShapeInfo[RealLabel], ShapeInfo[Sum], tuple(ShapeInfo[XYmax]), tuple(ShapeInfo[XYmin])))

        else:  #white dot
            if ExampleImage[y, x - 1, 0] == ExampleImage[y, x - 1, 1] == ExampleImage[y, x - 1, 2] == \
               ExampleImage[y, x + 1, 0] == ExampleImage[y, x + 1, 1] == ExampleImage[y, x + 1, 2] == 255 and \
               ExampleImage[y - 1, x + 1, 0] == ExampleImage[y - 1, x + 1, 1] == ExampleImage[y - 1, x + 1, 2] == 255 and \
               ExampleImage[y - 1, x, 0] != 0:   #该白点的左右两边和右上也是白点,上方不是白点. Left, right and up right dots are white too, and not white on top
                ShapeInfo = ShapeInfoList[ShapeInfoList[LabelArray[y - 1, x]][RealLabel]]  #取出正上方点的信息来判断它是不是一个连通域的最后结束点.
                                                                                           #Get the info of the dot on top and judge if it is the lass ending dot of a connected area
                if ShapeInfo[XLmax] == x and  ShapeInfo[XYmax][1] == y - 1:
                    AddClip(bg_image, x, y, Neighbourhood3x3, LabelColor = "grey", Shape_info = ShapeInfo, duration = FinishTime,
                            注释1 = "白点时需要检查\n其上方的形状\n有无标记完成",
                            注释2 = "Check if any shape has\nfinished labeling\n"
                                    "有形状完成啦!\nNo. {} has Finished: \n"
                                    "总点数Total Num of dots: {}\nXYmax: {} XYmin: {}".format(ShapeInfo[RealLabel],ShapeInfo[Sum], tuple(ShapeInfo[XYmax]), tuple(ShapeInfo[XYmin])))
                    print("FPGA: Label:{} Sum: {} XYmax: {} XYmin: {}".format(LabelCount, ShapeInfo[Sum],ShapeInfo[XYmax], ShapeInfo[XYmin]))
                    continue
            AddClip(bg_image, x, y, Neighbourhood3x3, 注释1="白点时需要检查\n其上方的形状\n有无标记完成",
                    注释2="Check if any shape has\nfinished labeling")



time_end = time.time()
print('Total time:{}s'.format(time_end - time_start))
print('Total frame', len(frame_list))


#预览视频. Preview video
if len(frame_list) == 0:
    print("Nothing to Preview")
    quit()
pygame.init()
screen = pygame.display.set_mode(VideoSize)
pygame.display.set_caption("按键KEY: 空格暂停'SPACE': pause. 'W S A D': 上下左右Up Down Left Right. "
                           "'ENTER': 跳到结尾 Jump to End 'F1': 保存当前图片(暂停时) Save current image when pause")
clock = pygame.time.Clock()
frame_index = 0
QuitPreview = False
Pause = False
Tip = 0
pygame.key.set_repeat(150,10)

def show_text(surface_handle, pos, text, color, font_size = 20):
    cur_font = pygame.font.Font("msyh.ttf", font_size)
    text_fmt = cur_font.render(text, 1, color, (255,255,255)) # 设置文字内容,白色背景
    surface_handle.blit(text_fmt, pos)                        # 绘制文字

def NextFrame(n):
    global frame_index
    if frame_index < len(frame_list) - n - 1: frame_index += n
    else: frame_index = 0
def PreFrame(n):
    global frame_index
    if frame_index > n: frame_index -= n
    else: frame_index = len(frame_list) - 1

while not QuitPreview:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:       QuitPreview = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE: Pause = not Pause
            if event.key == pygame.K_d or event.key == pygame.K_RIGHT:     NextFrame(1)
            if event.key == pygame.K_a or event.key == pygame.K_LEFT :     PreFrame(1)
            if event.key == pygame.K_s or event.key == pygame.K_DOWN :     NextFrame(46)
            if event.key == pygame.K_w or event.key == pygame.K_UP   :     PreFrame(46)
            if event.key == pygame.K_F1:
                if Pause:
                    Image.fromarray(frame_list[frame_index]).save("Frog" + str(frame_index) + ".bmp", format = "bmp" )
                    Tip = 25
            if event.key == pygame.K_RETURN:
                frame_index = len(frame_list) - 1
                Pause = True

    if not Tip:
        pygame.surfarray.blit_array(screen,frame_list[frame_index].transpose((1,0,2)))  #此处图像矩阵需要转置
    else:
        show_text(screen, 标题位置,  "图片已保存为Image Saved as: Frog" + str(frame_index) + ".bmp", (0, 0, 177), 40)
        Tip -= 1
    if not Pause:
        NextFrame(1)
    pygame.display.update()
    clock.tick(10)
pygame.quit()





