from Globals import *

@block
def TextBox(clk, X, Y, Loc, TextColor, charLoc, char, charColor, OEn, Ram, Clear):
    x, y,rowNum = (Signal(modbv(0)[WHb:]) for i in range(3))
    clrCNT = Signal(modbv(0)[12:0])

    @always_seq(clk.posedge, reset=None)
    def Seq():
        if (x[4:] == 0 and (x >> 4) < 64) and y < 16 * 32:
            charLoc.x.next = Loc.x + x
            charLoc.y.next = Loc.y + (rowNum << 4)

        if (x >> 4) < 64 and y < 16 * 32:
            OEn.next = 1
        else:
            OEn.next = 0


        if clrCNT == 2048:
            clrCNT.next = 0
        elif Clear or clrCNT > 0:
            clrCNT.next = clrCNT + 1
        else:
            clrCNT.next = 0



    @always_comb
    def Comb():
        x.next = X - Loc.x
        y.next = Y - Loc.y
        charColor.R.next = TextColor.R
        charColor.G.next = TextColor.G
        charColor.B.next = TextColor.B

    @always_comb
    def Comb1():
        rowNum.next = y >> 4


    @always_comb
    def Comb2():
        if clrCNT > 0:
            Ram.we.next = 1
            Ram.addr.next = clrCNT - 1
        else:
            Ram.addr.next = (x >> 4) + (rowNum << 6)
            Ram.we.next = 0
        char.next = Ram.dout[8:]
        Ram.din.next = 0

    return instances()
