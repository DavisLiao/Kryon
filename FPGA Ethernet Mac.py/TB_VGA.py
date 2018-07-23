from VGA_HDMI import *
from FPGA_GUI import *
from FontRom import FontRom
import time
from PIL import Image,ImageDraw,ImageFont
from TextRam import *
from KeyDetect import KeyDetect
from Mac_Ctrl import *


ImgArray = np.zeros((TestHeight, TestWidth, 3), np.uint8)

@block
def test_vga(Convert = False):
    clk, Vsync, Hsync, DataEn, key1,key2, key3, key4, Clear, Dkey1Down,TxEn,TxErr,SendEn,RxEn = (Signal(bool(0)) for i in range(14))
    Dkey1, Dkey2, Dkey3, Dkey4 =  (Signal(bool(1)) for i in range(4))
    X, X_5, Y, Width, Height = (Signal(modbv(0)[WHb:]) for i in range(5))
    ResolutionSel = Signal(modbv(4)[3:])
    RGBI, RGBO = COLOR(), COLOR()
    Rom = RAM(11,16)
    RamA,Ram_MacText = (RAM(11,9) for i in range(2))
    TxData,RxData = (Signal(modbv(0)[8:]) for i in range(2))
    TxCNT, RxCNT, TxLimit = (Signal(modbv(0)[24:]) for i in range(3))
    Data_Length, GapLength = (Signal(modbv(20)[16:]) for i in range(2))
    FrameRate = Signal(modbv(0)[8:])

    iVGA_HDMI = VGA_HDMI(clk, Vsync, Hsync, DataEn, X, X_5, Y, Width, Height, RGBI, RGBO, ResolutionSel)
    iFPGA_GUI = FPGA_GUI(clk, X_5, Y, Width, Height, RGBI, Rom , RamA, Clear,Dkey1Down)
    iFontRom = FontRom(clk,Rom)
    iTextRam = TextRam(clk,RamA,Ram_MacText)
    iKeyDetect = KeyDetect(clk, key1, key2, key3, key4, Dkey1, Dkey2, Dkey3, Dkey4, Clear, Dkey1Down)
    iMac_Ctrl = Mac_Ctrl(clk, TxEn, TxErr, TxData, RxEn, RxData, SendEn, Dkey2, Clear, Ram_MacText, Data_Length, GapLength, TxCNT, RxCNT, TxLimit, FrameRate)

    if Convert:
        iVGA_HDMI.convert(hdl="Verilog", initial_values=True)
        iFPGA_GUI.convert(hdl="Verilog", initial_values=True)
        iKeyDetect.convert(hdl="Verilog", initial_values=True)
        iMac_Ctrl.convert(hdl="Verilog", initial_values=True)

    @instance
    def clkgen():
        while True:
            clk.next = not clk
            yield  delay(5)


    FrameCNT = Signal(intbv(0)[5:])
    @always_seq(Vsync.posedge, reset = None)
    def FCNT():
        FrameCNT.next = FrameCNT + 1

    @always_seq(clk.posedge, reset=None)
    def SampleImage():
        if DataEn:
            #print(int(X),int(Y))
            ImgArray[int(Y),int(X)] = np.array([int(RGBO.R), int(RGBO.G), int(RGBO.B)])


    @instance
    def stimulus_vga():
       yield clk.negedge
       yield clk.negedge
       SendEn.next = 1
       yield clk.negedge
       SendEn.next = 0
       while FrameCNT < 2:
           yield clk.negedge

       for i in range(10):
           yield clk.negedge
       raise StopSimulation()

    if Convert:
        return iVGA_HDMI,iFPGA_GUI,iKeyDetect,iMac_Ctrl
    else:
        return instances()



tb = test_vga(Convert = True)
#tb = test_vga()

#tb.config_sim(trace = True)  #dump VCD

time_start = time.time()
tb.run_sim()

time_end = time.time()
print('Time:{}s'.format(time_end - time_start))

img1 = Image.fromarray(ImgArray)
img1.show()



