from Globals import *

@block
def Rectangle(clk, X, Y, Loc, Size, LineWidth, LineColor, FillColor, OEn, OColor):
    '''Draw a Rectangle on FPGA GUI

    :param clk: VGA or HDMI clk
    :param X: From 'VGA_HDMI' module, current output pixel coordinates
    :param Y:
    :param Loc:
    :param Size:
    :param LineWidth:
    :param LineColor:
    :param FillColor:
    :param OEn:
    :param OColor:
    :return:
    '''
    NoFill = Signal(bool(0))
    x, y = (Signal(modbv(0)[WHb:]) for i in range(2))

    @always_seq(clk.posedge, reset=None)
    def Seq():
        if (x < Size.W and y < Size.H):
            if((y <= LineWidth or y >= Size.H - LineWidth - 1) or (x <= LineWidth or x >= Size.W - LineWidth - 1)):
                OColor.R.next = LineColor.R
                OColor.G.next = LineColor.G
                OColor.B.next = LineColor.B
                OEn.next = 1
            elif NoFill == 0:
                OColor.R.next = FillColor.R
                OColor.G.next = FillColor.G
                OColor.B.next = FillColor.B
                OEn.next = 1
            else:
                OEn.next = 0
                OColor.R.next = 0
                OColor.G.next = 0
                OColor.B.next = 0

        else:
            OEn.next = 0
            OColor.R.next = 0
            OColor.G.next = 0
            OColor.B.next = 0

    @always_comb
    def Comb():
        if FillColor.R == 0 and FillColor.G == 0 and FillColor.B == 0:
            NoFill.next = 1
        else:
            NoFill.next = 0
        x.next = X - Loc.x
        y.next = Y - Loc.y


    return  instances()