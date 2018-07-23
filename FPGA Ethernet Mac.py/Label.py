from Globals import *

@block
def Label(clk, X, Y, Loc, labellist, labelColor, charLoc, char, charColor, OEn):
    x, y = (Signal(modbv(0)[WHb:]) for i in range(2))

    @always_seq(clk.posedge, reset=None)
    def Seq():
        if (x[4:] == 0 and (x >> 4) < len(labellist)) and y < 16:
            charLoc.x.next = Loc.x + x
            charLoc.y.next = Loc.y


        if ( (x >> 4) < len(labellist)) and y < 16:
            OEn.next = 1
            char.next = labellist[int(x >> 4)]
        else:
            OEn.next = 0




    @always_comb
    def Comb():
        x.next = X - Loc.x
        y.next = Y - Loc.y
        charColor.R.next = labelColor.R
        charColor.G.next = labelColor.G
        charColor.B.next = labelColor.B

    return instances()
