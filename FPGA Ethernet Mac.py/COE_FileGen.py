import pickle
import random
from PIL import Image
import numpy as np
from Globals import *

#Generate Xilinx Block Ram data init file *.coe
rfile = open('Font.dat', 'rb')
RomData = pickle.load(rfile)
rfile.close()

FontRomFile = open('FontRom.coe','w')
FontRomFile.write("memory_initialization_radix = 2;\n")
FontRomFile.write("memory_initialization_vector =\n")
for i in range(len(RomData)):
    if i < len(RomData) - 1:
        FontRomFile.write("{0:b}".format(RomData[i]) + ',\n')
    else:
        FontRomFile.write("{0:b}".format(RomData[i]) + ';')
FontRomFile.close()


TextRamFile = open('TextRam.coe','w')
TextRamFile.write("memory_initialization_radix = 10;\n")
TextRamFile.write("memory_initialization_vector =\n")
Frog = np.array(Image.open('64x32.bmp'))

for i in range(2048):
    if i < 2048 - 1:
        if(Frog.flat[i * 3] == 0):
            TextRamFile.write("{0:d}".format(Txt('*')[0]) + ',\n')
        else:
            TextRamFile.write("{0:d}".format(0) + ',\n')
    else:
        TextRamFile.write("{0:d}".format(1) + ';')


TextRamFile.close()