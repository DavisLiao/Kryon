from Globals import *

@block
def KeyDetect(clk, key1, key2, key3, key4, Dkey1, Dkey2, Dkey3, Dkey4, Clear, Dkey1Down):
    msCNT = Signal(modbv(0)[17:])
    key1Reg,key2Reg,key3Reg,key4Reg = (Signal(modbv(0xff)[8:]) for i in range(4))
    clrCNT = Signal(modbv(0)[8:])
    regDkey1 = Signal(bool(1))

    @always_comb
    def Comb():
        Dkey1Down.next = regDkey1 & ~Dkey1

    @always_seq(clk.posedge, reset=None)
    def Seq():
        if msCNT == 100000:
            msCNT.next = 0
        else:
            msCNT.next = msCNT + 1

        if msCNT == 0:
            key1Reg.next[8:1] = key1Reg.next[7:]
            key1Reg.next[0] = key1
            key2Reg.next[8:1] = key2Reg.next[7:]
            key2Reg.next[0] = key2
            key3Reg.next[8:1] = key3Reg.next[7:]
            key3Reg.next[0] = key3
            key4Reg.next[8:1] = key4Reg.next[7:]
            key4Reg.next[0] = key4

        regDkey1.next = Dkey1

        if regDkey1 == 0 and Dkey1 == 1 and clrCNT > 30:
            Clear.next = 1
        else:
            Clear.next = 0

        if Clear:
            clrCNT.next = 0
        elif msCNT == 0 and Dkey1 == 0 and clrCNT < 255:
             clrCNT.next = clrCNT + 1


        if key1Reg == 0:
            Dkey1.next = 0
        elif key1Reg == 0xff:
            Dkey1.next = 1

        if key2Reg == 0:
            Dkey2.next = 0
        elif key2Reg == 0xff:
            Dkey2.next = 1

        if key3Reg == 0:
            Dkey3.next = 0
        elif key3Reg == 0xff:
            Dkey3.next = 1

        if key4Reg == 0:
            Dkey4.next = 0
        elif key4Reg == 0xff:
            Dkey4.next = 1


    return instances()