from PIL import Image,ImageDraw,ImageFont
import numpy as np
from bitstring import BitArray
import pickle

def ToDataStr(array, data):
    str = ''
    for i in range(array.shape[0]):
        #print(array[i])
        temp = ''
        for each in array[i]:
            if each:
                temp += '0'
            else:
                temp += '1'
        data.append(BitArray(bin = temp).uint)
        str += temp + '\n'

    return str

FontImage = Image.open('font.bmp')
ImageArray = np.array(FontImage)
print(ImageArray.shape,ImageArray.dtype)
str = ''
data = []
#str = ToDataStr(ImageArray[1:17, 1 + 17:17 + 17])


for i in range(96):
    str += ToDataStr(ImageArray[1:17, 1 + 17 * i:17 * i + 17], data)

Tdata = tuple(data)
#print(str)
#print(Tdata)

wfile = open('Font.dat','wb')

pickle.dump(Tdata,wfile)
wfile.close()

rfile = open('Font.dat','rb')
Rdata = pickle.load(rfile)

print(type(Rdata))
print(Rdata)

rfile.close()









#FontImage.show()