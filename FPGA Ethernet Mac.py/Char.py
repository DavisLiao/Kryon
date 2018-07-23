from Globals import *

@block
def Char(clk, X, Y, Loc, char, charColor, OEn, OColor, Rom):
    x,x1, y = (Signal(modbv(0)[WHb:]) for i in range(3))
    Start = Signal(bool(0))
    SF15 = Signal(modbv(0)[15:])


    @always_seq(clk.posedge, reset = None)
    def Seq():
        x1.next = x
        if x1 == 0 and y < 16:
            SF15.next = Rom.dout[15:]
            if Rom.dout[15]:
                OEn.next = 1
                OColor.R.next = charColor.R
                OColor.G.next = charColor.G
                OColor.B.next = charColor.B
            else:
                OEn.next = 0
        elif x1 > 0 and x1 < 16 and y < 16:
            SF15.next[15:1] = SF15[14:]
            if SF15[14]:
                OEn.next = 1
                OColor.R.next = charColor.R
                OColor.G.next = charColor.G
                OColor.B.next = charColor.B
            else:
                OEn.next = 0
        else:
            OEn.next = 0

    @always_comb
    def Comb():
        x.next = X - Loc.x
        y.next = Y - Loc.y


    @always_comb
    def Comb2():
        Rom.we.next = Start
        if y < 16 and Start == 1:
            Rom.addr.next = (char << 4) + y

    @always_comb
    def Comb3():
        Start.next = x == 0 and y < 16
        Rom.din.next = 0


    return instances()