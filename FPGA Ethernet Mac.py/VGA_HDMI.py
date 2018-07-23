from Globals import *

@block
def VGA_HDMI(clk, Vsync, Hsync, DataEn, X, X_5, Y, Width, Height, RGBI, RGBO, ResolutionSel):
    '''VGA or HDMI video output

    :param clk: Different resolution has different clock frequency
    :param Vsync: Output Vertical Sync
    :param Hsync: Output Horizontal Sync
    :param DataEn: To indicate other module the data output is enabled
    :param X: Current pixel data X coordinate
    :param X_5: 5 clock cycle before X, for other module to prepare RGB data
    :param Y: Current pixel data Y coordinate
    :param Width: Video Width
    :param Height: Video Height
    :param RGBI: RGB Data in from other module
    :param RGBO: RGB Data output
    :param ResolutionSel: Select Resolution
    '''
    #注意不能使用a = b = c = 0这样的连等,翻译成Verilog时会报错.信号要注明宽度
    H_SYNC  = Signal(modbv(0)[8:])
    H_B_PORCH = Signal(modbv(0)[9:])
    V_TOTAL, V_ADDR ,H_TOTAL, H_ADDR, HCNT, VCNT = (Signal(modbv(0)[WHb:]) for i in range(6))
    V_SYNC, V_B_PORCH = (Signal(modbv(0)[7:]) for i in range(2))

    @always_seq(clk.posedge, reset = None)
    def Seq():
        if HCNT == H_TOTAL - 1:
            HCNT.next = 0
        else:
            HCNT.next = HCNT + 1

        if(HCNT == H_TOTAL - 1):
            if(VCNT == V_TOTAL - 1):
                VCNT.next = 0
            else:
                VCNT.next = VCNT + 1

        if VCNT >= 0 and VCNT < V_SYNC:
            Vsync.next = 0
        else:
            Vsync.next = 1

        if HCNT >= 0 and HCNT < H_SYNC or (VCNT < V_SYNC + V_B_PORCH or VCNT >= V_SYNC + V_B_PORCH + V_ADDR):
            Hsync.next = 0
        else:
            Hsync.next = 1

        if Hsync:
            X_5.next = HCNT + 5 - (H_SYNC + H_B_PORCH)
            X.next = HCNT - (H_SYNC + H_B_PORCH)

        Y.next = VCNT - (V_SYNC + V_B_PORCH)
        DataEn.next = Hsync and (HCNT >= H_SYNC + H_B_PORCH) and (HCNT < H_SYNC + H_B_PORCH + H_ADDR)

    @always_comb
    def Comb():
        Width.next = H_ADDR
        Height.next = V_ADDR

    @always_comb
    def R_Sel():
        RGBO.R.next = RGBI.R
        RGBO.G.next = RGBI.G
        RGBO.B.next = RGBI.B

        if ResolutionSel == 0:
            '''
            1280x1024@60Hz  108.0M
            '''
            H_TOTAL.next    = 1688
            H_ADDR.next     = 1280
            H_SYNC.next     = 112
            H_B_PORCH.next  = 248
            V_TOTAL.next    = 1066
            V_ADDR.next     = 1024
            V_SYNC.next     = 3
            V_B_PORCH.next  = 38
        elif ResolutionSel == 1:
            '''
            1440x900@60Hz 106.5M
            '''
            H_TOTAL.next    = 1904
            H_ADDR.next     = 1440
            H_SYNC.next     = 152
            H_B_PORCH.next  = 232
            V_TOTAL.next    = 934
            V_ADDR.next     = 900
            V_SYNC.next     = 6
            V_B_PORCH.next  = 25
        elif ResolutionSel == 2:
            '''
            1600x900@60Hz 108.0M
            '''
            H_TOTAL.next    = 1800
            H_ADDR.next     = 1600
            H_SYNC.next     = 80
            H_B_PORCH.next  = 96
            V_TOTAL.next    = 1000
            V_ADDR.next     = 900
            V_SYNC.next     = 3
            V_B_PORCH.next  = 96
        elif ResolutionSel == 3:
            '''
            1920*1080@60Hz 148.5M
            '''
            H_TOTAL.next    = 2200
            H_ADDR.next     = 1920
            H_SYNC.next     = 44
            H_B_PORCH.next  = 148
            V_TOTAL.next    = 1125
            V_ADDR.next     = 1080
            V_SYNC.next     = 5
            V_B_PORCH.next  = 36
        else:
            '''
            Test
            '''
            H_TOTAL.next    = TestWidth + 3 + 7 + 4
            H_ADDR.next     = TestWidth
            H_SYNC.next     = 3
            H_B_PORCH.next  = 7
            V_TOTAL.next    = TestHeight + 5 + 6 + 7
            V_ADDR.next     = TestHeight
            V_SYNC.next     = 5
            V_B_PORCH.next  = 6


    return instances()