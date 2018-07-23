from Mac_Tx import *
from Mac_Rx import Mac_Rx
from TxPic import TxPic

@block
def Mac_Ctrl(clk, TxEn, TxErr, TxData, RxEn, RxData, SendEn, Dkey2, Clear, Ram_MacText, DataLength, GapLength, TxCNT, RxCNT, TxLimit, FrameRate):
    EtherType = Signal(modbv(EtherType_IPv4)[16:])
    IP_Total_Length, Tx_UDP_Length, RxEtherType, RxDataLength, PicTxDataLength  = (Signal(modbv(0)[16:]) for j in range(5))
    RxIP_Total_Length, Rx_UDP_Length, Rx_srcPort, Rx_desPort = (Signal(modbv(0)[16:]) for i in range(4))
    Tx_srcPort, Tx_desPort = (Signal(modbv(57766)[16:]) for i in range(2))
    RxSourceMac, RxDestinationMAC = (Signal(modbv(0)[48:]) for i in range(2))
    RxSourceIP, RxDestinationIP = (Signal(modbv(0)[32:]) for i in range(2))
    Tx_IP_Protocol = Signal(modbv(IP_Protocal_UDP)[8:])
    Tx_Ram, Rx_Ram = (RAM(11, 9) for i in range(2))
    SendData, ReceiveData, Rx_IP_Protocol, PicTxData = (Signal(modbv(0)[8:]) for i in range(4))
    ReceiveEn, TxEnd, RxEnd, TxSendEn, TxIDLE, PicTxEn, PixTxing, SendDataEn = (Signal(bool(0)) for i in range(8))
    RxTextPointer = Signal(modbv(0)[6:])
    TxTextPointer  = Signal(modbv(1)[6:])
    PicGapLength, TxDataLength, TxGapLength = (Signal(modbv(0)[16:]) for i in range(3))


    @always_seq(clk.posedge, reset=None)
    def Seq():
        if Clear == 1:
            TxCNT.next = 0
            RxCNT.next = 0
        else:
            if TxEnd:
                TxCNT.next = TxCNT + 1
            if RxEnd:
                RxCNT.next = RxCNT + 1


        if Clear == 1:
            TxTextPointer.next = 1
            RxTextPointer.next = 0
        elif TxEnd == 1:
            TxTextPointer.next = TxTextPointer + 2
        elif RxEnd == 1:
            RxTextPointer.next = RxTextPointer + 2

        if Rx_Ram.we == 1 and RxEn:
            Ram_MacText.we.next = Rx_Ram.we
            Ram_MacText.addr.next = Rx_Ram.addr + (RxTextPointer << 5)
            Ram_MacText.din.next = Rx_Ram.din
        elif Tx_Ram.we == 1:
            Ram_MacText.we.next = Tx_Ram.we
            Ram_MacText.addr.next = Tx_Ram.addr + (TxTextPointer << 5)
            Ram_MacText.din.next = Tx_Ram.din
        else:
            Ram_MacText.we.next = 0

    @always_comb
    def Comb():
        TxSendEn.next = SendEn or (Dkey2 and TxCNT < TxLimit - 1) or PicTxEn
        RxDataLength.next = Rx_UDP_Length - UDP_Header_Len
        if PixTxing:
            TxDataLength.next = PicTxDataLength
            TxGapLength.next = PicGapLength
            SendData.next = PicTxData
        else:
            TxDataLength.next = DataLength
            TxGapLength.next = GapLength
            SendData.next = 1

    @always_comb
    def Comb2():
        Tx_UDP_Length.next = TxDataLength + UDP_Header_Len
        IP_Total_Length.next = TxDataLength + UDP_Header_Len + IP_Header_Len


    iMac_Tx = Mac_Tx(clk, TxEn, TxErr, TxData, TxEnd, TxSendEn, SendData,SendDataEn, SourceMac, DestinationMAC, EtherType, IP_Total_Length,
                     Tx_IP_Protocol, SourceIP, DestinationIP, Tx_srcPort, Tx_desPort, Tx_UDP_Length, TxDataLength, TxGapLength, TxCNT, Tx_Ram, TxIDLE)
    iMac_Rx = Mac_Rx(clk, RxEn, RxData, RxEnd, ReceiveEn, ReceiveData, RxSourceMac, RxDestinationMAC, RxEtherType,
                     RxIP_Total_Length, Rx_IP_Protocol, RxSourceIP, RxDestinationIP, Rx_srcPort, Rx_desPort, Rx_UDP_Length, Rx_Ram)

    iTxPic = TxPic(clk, RxEnd, Rx_IP_Protocol, Rx_desPort, RxDataLength, TxIDLE, TxEnd, PicTxEn, PixTxing, Tx_desPort,SendDataEn, PicTxData, PicTxDataLength, PicGapLength, FrameRate)

    return instances()