from Globals import *
from Rectangle import Rectangle

PicS = enum('IDLE', 'WAIT_TX', 'TX', 'TXING', 'TX_END', encoding="one_hot")
PicRxPort = 57766
PicTxPort = 57788
PicRxDataLen = 7
PicWidth = 1024
PicHeight = 512
PktLength = PicWidth
PktNum = PicHeight * 3 #PicWidth * PicHeight * 3 / PktLength
PicEndGap = 1024


@block
def TxPic(clk, RxEnd, RxIP_Protocol, RxdesPort, RxDataLength, TxIDLE, TxEnd, PicTxEn, PicTxing, TxdesPort, SendDataEn, PicTxData, PicTxDataLength, PicGapLength, FrameRate):
    State = Signal(PicS.IDLE)
    PktCNT, EndCNT = (Signal(modbv(0)[16:]) for i in range(2))
    FrameCNT = Signal(modbv(0)[32:])
    EndPktCNT = Signal(modbv(0)[2:])
    TxingCNT = Signal(modbv(0)[16:])
    CNTx3, CNTy3 = (Signal(modbv(0)[2:]) for i in range(2))
    X, Y = (Signal(modbv(0)[WHb:]) for i in range(2))
    Rect1OEn = Signal(bool(0))
    Rect1OColor = COLOR()
    Rect1Size = SIZE(PicWidth,PicHeight)
    CNT1S = (Signal(modbv(0)[28:]))
    FrameRateCNT = Signal(modbv(0)[8:])



    @always_seq(clk.posedge, reset=None)
    def Seq():
        if State == PicS.IDLE:
            PicTxEn.next = 0
            #PicTxData.next = 2
            PktCNT.next = 0
            EndCNT.next = 0
            PicGapLength.next = 0
            EndPktCNT.next = 0
            PicTxing.next = 0
            CNTx3.next = 0
            X.next = 0
            Y.next = 0

            if RxEnd == 1 and RxIP_Protocol == IP_Protocal_UDP and RxdesPort == PicRxPort and RxDataLength == PicRxDataLen:
                State.next = PicS.TX
                PicTxing.next = 1

        if State == PicS.TX:
            PicTxDataLength.next = PktLength
            if TxIDLE and PktCNT < PktNum:
                PicTxEn.next = 1
                #PktCNT.next = PktCNT + 1
                State.next = PicS.TXING
            else:
                if PktCNT == PktNum:
                    State.next = PicS.TX_END
                    PktCNT.next = 0
                PicTxEn.next = 0

        if State == PicS.TXING:
            PicTxEn.next = 0
            TxingCNT.next = TxingCNT + 1
            if TxingCNT > 64 and TxIDLE == 1:
                State.next = PicS.TX
                PktCNT.next = PktCNT + 1
                TxingCNT.next = 0
                if CNTy3 == 2:
                    CNTy3.next = 0
                    Y.next = Y + 1
                else:
                    CNTy3.next = CNTy3 + 1

            if SendDataEn:
                if CNTx3 == 2:
                    CNTx3.next = 0
                    if X == PicWidth - 1:
                        X.next = 0
                    else:
                        X.next = X + 1
                else:
                    CNTx3.next = CNTx3 + 1




        if State == PicS.TX_END:
            Y.next = 0
            PicTxDataLength.next = 1
            PicGapLength.next = PicEndGap
            EndCNT.next = EndCNT + 1
            if EndCNT > PicEndGap and TxIDLE and EndPktCNT < 2:
                PicTxEn.next = 1
            else:
                PicTxEn.next = 0

            if TxEnd == 1:
                EndPktCNT.next = EndPktCNT + 1

            if TxIDLE and EndPktCNT >= 2:
                State.next = PicS.IDLE
                FrameCNT.next = FrameCNT + 1
                PicTxEn.next = 0
                EndPktCNT.next = 0
                FrameRateCNT.next = FrameRateCNT + 1
                if FrameCNT > 20:
                    if Rect1Size.W < 10:
                        Rect1Size.W.next = PicWidth
                    else:
                        Rect1Size.W.next = Rect1Size.W - 5

        if CNT1S == 125000000 - 1:
            CNT1S.next = 0
            FrameRateCNT.next = 0
            FrameRate.next = FrameRateCNT
        else:
            CNT1S.next = CNT1S + 1


    iRect1 = Rectangle(clk, X, Y, LOC(0, 0), Rect1Size, 0, COLOR(255,0,255), COLOR(0,0,0), Rect1OEn, Rect1OColor)


    @always_comb
    def assign():
        if PicTxing:
            TxdesPort.next = PicTxPort
        if CNTx3 == 1: PicTxData.next = Rect1OColor.R
        if CNTx3 == 2: PicTxData.next = Rect1OColor.G
        if CNTx3 == 0: PicTxData.next = Rect1OColor.B



    return instances()