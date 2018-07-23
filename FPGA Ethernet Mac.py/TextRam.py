from Globals import *
from PIL import Image

Frog = np.array(Image.open('64x32.bmp'))
TextRamData = np.zeros(2048)
for i in range(2048):
    if Frog.flat[i * 3] == 0:
        TextRamData[i] = 11


@block
def TextRam(clk, RamA, RamB):

    @always_seq(clk.posedge, reset=None)
    def RW():
        RamA.dout.next = int(TextRamData[int(RamA.addr)])
        RamB.dout.next = int(TextRamData[int(RamB.addr)])

        if RamA.we:
            TextRamData[int(RamA.addr)] = int(RamA.din)
        if RamB.we:
            TextRamData[int(RamB.addr)] = int(RamB.din)





    return instances()