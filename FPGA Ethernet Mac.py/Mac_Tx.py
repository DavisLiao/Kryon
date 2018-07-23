from Globals import *
from CRC32 import CRC32
TxS = enum('IDLE', 'ETH', 'ARP', 'IP', 'UDP', 'DATA', 'CRC','GAP', encoding="one_hot")

def ToChar(a):
    #b = Signal(modbv(0)[4:])
    b = 0
    if a <= 9:
        b = a + 17
    else:
        b = a + 24
    return b

@block
def Mac_Tx(clk,TxEn, TxErr, TxData, TxEnd, SendEn, SendData, SendDataEn, srcMac, desMac, EtherType, IP_Total_Length, IP_Protocal,
           srcIP, desIP, srcPort, desPort, UDP_Length, Data_Length, GapLength,TxCNT, Ram, IDLE):
    State, StateReg  = (Signal(TxS.IDLE) for i in range(2))
    CNT = Signal(modbv(0)[12:0])
    EthHeader, IPHeader, UDPHeader,ARP_Data, PktData, TxDataReg = (Signal(modbv(0)[8:]) for frog in range(6))
    TxEnReg,TxEnReg1 = (Signal(bool(0)) for frog in range(2))
    CrcReset, CrcEnable = (Signal(bool(0)) for i in range(2))
    Crc, CrcNext = (Signal(modbv(0xffffffff)[32:]) for i in range(2))
    IPHeader_CheckSum = Signal(modbv(0)[32:])


    iCRC32 = CRC32(clk, CrcReset, TxDataReg, CrcEnable, Crc, CrcNext)

    @always_seq(clk.posedge, reset=None)
    def Seq():
        if State == TxS.IDLE:
            IDLE.next = 1
            CNT.next = 0
            EthHeader.next = 0
            IPHeader.next = 0
            UDPHeader.next = 0
            TxEnReg.next = 0
            TxErr.next = 0
            Ram.we.next = 0
            Ram.addr.next = 0
            Ram.din.next = 0
            TxEnd.next = 0
            CrcReset.next = 0
            SendDataEn.next = 0
            IPHeader_CheckSum.next = 0
            if SendEn:
                State.next = TxS.ETH
                IDLE.next = 0

        if State == TxS.ETH:
            if CNT < Ether_Header_Len - 1:
                CNT.next = CNT + 1
            else:
                CNT.next = 0
                if EtherType == EtherType_IPv4:
                    State.next = TxS.IP
                elif EtherType == EtherType_ARP:
                    State.next = TxS.ARP
                else:
                    TxErr.next = 1
                    State.next = TxS.GAP

            if CNT == 0:  TxEnReg.next = 1
            if CNT <= 6:  EthHeader.next = 0x55
            if CNT == 7:  EthHeader.next = 0xd5
            if CNT == 8:  EthHeader.next = desMac[48:40]
            if CNT == 9:  EthHeader.next = desMac[40:32]
            if CNT == 10: EthHeader.next = desMac[32:24]
            if CNT == 11: EthHeader.next = desMac[24:16]
            if CNT == 12: EthHeader.next = desMac[16:8]
            if CNT == 13: EthHeader.next = desMac[8:]
            if CNT == 14: EthHeader.next = srcMac[48:40]
            if CNT == 15: EthHeader.next = srcMac[40:32]
            if CNT == 16: EthHeader.next = srcMac[32:24]
            if CNT == 17: EthHeader.next = srcMac[24:16]
            if CNT == 18: EthHeader.next = srcMac[16:8]
            if CNT == 19: EthHeader.next = srcMac[8:]
            if CNT == 20: EthHeader.next = EtherType[16:8]
            if CNT == 21: EthHeader.next = EtherType[8:]

            if CNT == 1: Ram.din.next = 53 #T   #For Gui
            if CNT == 2: Ram.din.next = 89 #x
            if CNT == 3: Ram.din.next = 27 #:
            if CNT >= 1 and CNT <= 3:
                Ram.we.next = 1
                if CNT > 1:
                    Ram.addr.next = Ram.addr + 1
            else:
                Ram.we.next = 0
            if CNT == 9: CrcEnable.next = 1

        if State == TxS.ARP:
            if CNT < ARP_Len + 4 - 1:
                CNT.next = CNT + 1
            else:
                CNT.next = 0
                State.next = TxS.GAP

            ARP_Data.next = 0xab
            if CNT == 1: Ram.din.next = 34 #A  #For Gui
            if CNT == 2: Ram.din.next = 51 #R
            if CNT == 3: Ram.din.next = 49 #P
            if CNT >= 1 and CNT <= 3:
                Ram.we.next = 1
                Ram.addr.next = Ram.addr + 1
            else:
                Ram.we.next = 0

        if State == TxS.IP:
            EthHeader.next = 0
            if CNT < IP_Header_Len - 1:
                CNT.next = CNT + 1
            else:
                CNT.next = 0
                State.next = TxS.UDP

            if CNT == 0:  IPHeader.next = IP_Version_HeaderLen
            if CNT == 1:  IPHeader.next = TypeofService
            if CNT == 2:  IPHeader.next = IP_Total_Length[16:8]
            if CNT == 3:  IPHeader.next = IP_Total_Length[8:]
            if CNT == 4:  IPHeader.next = 0  #标识 Identification
            if CNT == 5:  IPHeader.next = 0
            if CNT == 6:  IPHeader.next = 0  #Flags, Fragment Offset
            if CNT == 7:  IPHeader.next = 0
            if CNT == 8:  IPHeader.next = 0x40 #Time to Live
            if CNT == 9:  IPHeader.next = IP_Protocal   #Protocol UDP,TCP
            if CNT == 10: IPHeader.next = IPHeader_CheckSum[16:8] #Header Checksum
            if CNT == 11: IPHeader.next = IPHeader_CheckSum[8:0]
            if CNT == 12: IPHeader.next = srcIP[32:24]
            if CNT == 13: IPHeader.next = srcIP[24:16]
            if CNT == 14: IPHeader.next = srcIP[16:8]
            if CNT == 15: IPHeader.next = srcIP[8:]
            if CNT == 16: IPHeader.next = desIP[32:24]
            if CNT == 17: IPHeader.next = desIP[24:16]
            if CNT == 18: IPHeader.next = desIP[16:8]
            if CNT == 19: IPHeader.next = desIP[8:]

            if CNT == 0: IPHeader_CheckSum.next = IPHeader_CheckSum + TypeofService + IP_Version_HeaderLen << 8
            if CNT == 1: IPHeader_CheckSum.next = IPHeader_CheckSum + IP_Total_Length
            if CNT == 2: IPHeader_CheckSum.next = IPHeader_CheckSum + IP_Protocal + 0x4000
            if CNT == 3: IPHeader_CheckSum.next = IPHeader_CheckSum + srcIP[32:16] + srcIP[16:]
            if CNT == 4: IPHeader_CheckSum.next = IPHeader_CheckSum + desIP[32:16] + desIP[16:]
            if CNT == 5:
                if IPHeader_CheckSum[32:16] == 0:
                    IPHeader_CheckSum.next[16:] = ~IPHeader_CheckSum[16:]
                else:
                    IPHeader_CheckSum.next[16:] = ~(IPHeader_CheckSum[16:] + IPHeader_CheckSum[32:16])


            if CNT == 10:
                if IP_Protocal == IP_Protocal_TCP:  Ram.din.next = 53 #T
                elif IP_Protocal == IP_Protocal_UDP:  Ram.din.next = 54 #U
                else: Ram.din.next = 57 #X
            if CNT == 11:
                if IP_Protocal == IP_Protocal_TCP:  Ram.din.next = 36 #C
                elif IP_Protocal == IP_Protocal_UDP:  Ram.din.next = 37 #D
                else: Ram.din.next = 57 #X
            if CNT >= 10 and CNT <= 11:
                Ram.we.next = 1
                Ram.addr.next = Ram.addr + 1
            else:
                Ram.we.next = 0

        if State == TxS.UDP:
            IPHeader.next = 0
            if CNT < UDP_Header_Len - 1:
                CNT.next = CNT + 1
            else:
                CNT.next = 0
                State.next = TxS.DATA

            if CNT == 0:  UDPHeader.next = srcPort[16:8]
            if CNT == 1:  UDPHeader.next = srcPort[8:]
            if CNT == 2:  UDPHeader.next = desPort[16:8]
            if CNT == 3:  UDPHeader.next = desPort[8:]
            if CNT == 4:  UDPHeader.next = UDP_Length[16:8]   #UDP Length
            if CNT == 5:  UDPHeader.next = UDP_Length[8:]
            if CNT == 6:  UDPHeader.next = 0  #UDP Header Checksum
            if CNT == 7:  UDPHeader.next = 0

            if CNT == 6:  SendDataEn.next = 1


        if State == TxS.DATA:
            UDPHeader.next = 0

            if CNT < Data_Length - 1 or CNT < 18 - 1: #UDP_Length - UDP_Header_Len
                CNT.next = CNT + 1
            else:
                CNT.next = 0
                State.next = TxS.CRC

            # if CNT == 0: PktData.next = TxCNT[24:16]
            # if CNT == 1: PktData.next = TxCNT[16: 8]
            # if CNT == 2: PktData.next = TxCNT[8 : 0]

            if CNT < Data_Length: #and CNT > 2:
                PktData.next = SendData
                #SendDataEn.next = 1

            elif CNT >= Data_Length:
                PktData.next = 0 #CRC
                #SendDataEn.next = 0

            if CNT >= Data_Length - 2:
                SendDataEn.next = 0

            if CNT == 0: Ram.din.next = 0
            if CNT == 1: Ram.din.next = ToChar(int(TxCNT[24:20]))
            if CNT == 2: Ram.din.next = ToChar(int(TxCNT[20:16]))
            if CNT == 3: Ram.din.next = ToChar(int(TxCNT[16:12]))
            if CNT == 4: Ram.din.next = ToChar(int(TxCNT[12:8 ]))
            if CNT == 5: Ram.din.next = ToChar(int(TxCNT[8 : 4]))
            if CNT == 6: Ram.din.next = ToChar(int(TxCNT[4 : 0]))

            if CNT >= 0 and CNT <= 6:
                Ram.we.next = 1
                Ram.addr.next = Ram.addr + 1
            else:
                Ram.we.next = 0


        if State == TxS.CRC:
            SendDataEn.next = 0
            if CNT < Ether_CRC_LEN + 2 - 1:
                CNT.next = CNT + 1
            else:
                CNT.next = 0
                State.next = TxS.GAP
            if CNT == 1:
                CrcEnable.next = 0
            if CNT == 4:
                TxEnReg.next = 0

        if State == TxS.GAP:
            PktData.next = 0
            if CNT < InterframeGap_Len - 1 + GapLength:
                CNT.next = CNT + 1
            else:
                CNT.next = 0
                State.next = TxS.IDLE
                TxEnd.next = 1
                CrcReset.next = 1


        StateReg.next = State
        if StateReg == TxS.IDLE : TxDataReg.next = 0
        if StateReg == TxS.ETH  : TxDataReg.next = EthHeader
        if StateReg == TxS.ARP  : TxDataReg.next = ARP_Data
        if StateReg == TxS.IP   : TxDataReg.next = IPHeader
        if StateReg == TxS.UDP  : TxDataReg.next = UDPHeader
        if StateReg == TxS.DATA : TxDataReg.next = PktData
        if StateReg == TxS.CRC  : TxDataReg.next = 0
        if StateReg == TxS.GAP  : TxDataReg.next = 0
        TxEnReg1.next = TxEnReg


    @always_seq(clk.posedge, reset=None)
    def Seq1():
        if State == TxS.CRC and CNT >= 2 and CNT <= 5:
           if CNT == 2: TxData.next = Crc[32:24]
           if CNT == 3: TxData.next = Crc[24:16]
           if CNT == 4: TxData.next = Crc[16:8]
           if CNT == 5: TxData.next = Crc[8:]

        else:
           TxData.next = TxDataReg
        TxEn.next = TxEnReg1



    return instances()