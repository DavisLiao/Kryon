from Globals import *

@block
def Arbiter(clk, RGBO, En0, C0, En1, C1, En2, C2, En3, C3, En4, C4, En5, C5, bgColor):

    @always_seq(clk.posedge, reset=None)
    def Seq():
        if En0:
            RGBO.R.next = C0.R
            RGBO.G.next = C0.G
            RGBO.B.next = C0.B
        elif En1:
            RGBO.R.next = C1.R
            RGBO.G.next = C1.G
            RGBO.B.next = C1.B
        elif En2:
            RGBO.R.next = C2.R
            RGBO.G.next = C2.G
            RGBO.B.next = C2.B
        elif En3:
            RGBO.R.next = C3.R
            RGBO.G.next = C3.G
            RGBO.B.next = C3.B
        elif En4:
            RGBO.R.next = C4.R
            RGBO.G.next = C4.G
            RGBO.B.next = C4.B
        elif En5:
            RGBO.R.next = C5.R
            RGBO.G.next = C5.G
            RGBO.B.next = C5.B
        else:
            RGBO.R.next = bgColor.R
            RGBO.G.next = bgColor.G
            RGBO.B.next = bgColor.B

    return  instances()




