from Rectangle import *
from Arbiter import Arbiter
from Char import Char
from Label import Label
from TextBox import *

@block
def FPGA_GUI(clk, X_5, Y, Width, Height, RGBO, Rom, RamText,Clear, Dkey1Down):
    X_3,X_2,X_1 = (Signal(modbv(0)[WHb:]) for i in range(3))
    OEnRect1, OEnRect2, OEnChar,OEnLabel1,OEnTextBox = (Signal(bool(0)) for i in range(5))
    OColorRect1, OColorRect2, OColorChar, charColor,charColorLabel1,charColorTextBox = (COLOR() for i in range(6))
    charLoc,charLocLabel1,charLocTextBox = (LOC(2000,2000) for i in range(3))
    char,charLabel1,charTextBox = (Signal(modbv(0)[8:]) for i in range(3))
    Rect1Size = SIZE(0, 0)
    Rect1bgColor = COLOR(0,0,0)
    Rect2bgColor = COLOR(0,0,0)
    iLabel1Text = Text('Clear')

    iRect1 = Rectangle(clk, X_3, Y, LOC(0, 0), Rect1Size, Signal(modbv(0)[2:]), BLUE, Rect1bgColor, OEnRect1, OColorRect1)
    iRect2 = Rectangle(clk, X_3, Y, LOC(6, 8), SIZE(100,24), Signal(modbv(0)[2:]), RED, Rect2bgColor, OEnRect2, OColorRect2)

    iChar1 = Char(clk,X_2,Y,charLoc,char,charColor,OEnChar,OColorChar,Rom)

    iLabel1 = Label(clk,X_1,Y, LOC(16,12),iLabel1Text, RED,charLocLabel1, charLabel1 ,charColorLabel1, OEnLabel1)

    iTextBox = TextBox(clk,X_1,Y,LOC(6,38),GREEN,charLocTextBox, charTextBox,charColorTextBox,OEnTextBox ,RamText,Clear)

    iArbiter = Arbiter(clk, RGBO, OEnChar,OColorChar, OEnRect1, OColorRect1,OEnRect2, OColorRect2,
                        Signal(bool(0)), COLOR(0,0,0), Signal(bool(0)), COLOR(0,0,0), Signal(bool(0)), COLOR(0,0,0), COLOR(0,0,0))

    @always_seq(clk.posedge, reset=None)
    def Seq():
        if Dkey1Down:
            Rect2bgColor.R.next = 128
            Rect2bgColor.G.next = 0
            Rect2bgColor.B.next = 0
        elif Clear:
            Rect2bgColor.R.next = 0
            Rect2bgColor.G.next = 0
            Rect2bgColor.B.next = 0

    @always_comb
    def Comb():
        X_3.next = X_5 - 3
        X_2.next = X_5 - 2
        X_1.next = X_5 - 1
        Rect1Size.W.next = Width
        Rect1Size.H.next = Height


        if OEnTextBox:
            charLoc.x.next   = charLocTextBox.x
            charLoc.y.next   = charLocTextBox.y
            char.next      = charTextBox
            charColor.R.next = charColorTextBox.R
            charColor.G.next = charColorTextBox.G
            charColor.B.next = charColorTextBox.B
        else:
            charLoc.x.next   = charLocLabel1.x
            charLoc.y.next   = charLocLabel1.y
            char.next      = charLabel1
            charColor.R.next = charColorLabel1.R
            charColor.G.next = charColorLabel1.G
            charColor.B.next = charColorLabel1.B


    return  instances()