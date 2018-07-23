from PIL import Image,ImageDraw,ImageFont


def 微软雅黑(Size):
    return ImageFont.truetype("msyh.ttf", Size)
def consola(Size):
    return ImageFont.truetype("consola.ttf", Size)
def CalibriL(Size):
    return ImageFont.truetype("CalibriL.ttf", Size)

def calibri(Size):
    return ImageFont.truetype("calibri.ttf", Size)

def simsun(Size):
    return ImageFont.truetype("simsun.ttc", Size)

def 方框(x, y, 位置, 比例):
    左上 = (位置[0] + x * 比例, 位置[1] + y * 比例)
    右下 = (位置[0] + x * 比例 + 比例, 位置[1] + y * 比例 + 比例)
    return [左上, 右下]


ASCII = ''
for i in range(33, 128):
    ASCII += chr(i)

Size = 16

FontImage = Image.new("1", (1660,300), "white")
Draw = ImageDraw.Draw(FontImage)

for i in range(33, 129):
    Draw.rectangle([((i - 33) * (Size + 1), 0), ((i - 32) * (Size + 1), (Size + 1))], outline='black')
    if i >= 33 + 2:
        Draw.text(((i - 33) * (Size + 1) + 1, 1), chr(i-2), fill="black", font=CalibriL(17))


#DrawFont.line([(4,4 + 3),(1000,4 + 3)],fill='black')
# DrawFont.line([(4,4+16 + 5),(1000,4+16 + 5)],fill='black')
# DrawFont.text((4,4),ASCII,fill = "black", font = 微软雅黑(16))

#DrawFont.line([(4,30 + 3),(1000,30 + 3)],fill='black')
# DrawFont.line([(4,25+18 + 5),(1000,25+18 + 5)],fill='black')
# DrawFont.text((4,25),ASCII,fill = "black", font = 微软雅黑(18))

# DrawFont.text((4,50),ASCII,fill = "black", font = consola(16))
# DrawFont.text((4,70),ASCII,fill = "black", font = consola(17))
#DrawFont.text((4,90),ASCII,fill = "black", font = consola(18))

#DrawFont.text((4,110),ASCII,fill = "black", font = CalibriL(16))
# DrawFont.text((4,130),ASCII,fill = "black", font = CalibriL(17))
# DrawFont.text((4,150),ASCII,fill = "black", font = CalibriL(18))

# DrawFont.text((4,170),ASCII,fill = "black", font = calibri(16))
# DrawFont.text((4,190),ASCII,fill = "black", font = calibri(17))
# DrawFont.text((4,210),ASCII,fill = "black", font = calibri(18))

# DrawFont.text((4,170),ASCII,fill = "black", font = simsun(16))
# DrawFont.text((4,190),ASCII,fill = "black", font = simsun(17))
# DrawFont.text((4,210),ASCII,fill = "black", font = simsun(18))


FontImage.show()
