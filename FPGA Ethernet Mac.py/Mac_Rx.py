from Globals import *
RxS = enum('IDLE', 'ETH', 'ARP', 'IP', 'UDP', 'DATA', 'GAP', encoding="one_hot")

def ToChar(a):
    #b = Signal(modbv(0)[4:])
    b = 0
    if a <= 9:
        b = a + 17
    else:
        b = a + 24
    return b

@block
def Mac_Rx(clk, RxEn, RxData, RxEnd, ReceiveEn, ReceiveData, srcMac, desMac, EtherType, IP_Total_Length, IP_Protocol, srcIP, desIP, srcPort, desPort, UDP_Length, Ram):
    State = Signal(RxS.IDLE)
    CNT = Signal(modbv(0)[12:0])
    RxEnReg   = Signal(bool(0))
    RxDataReg = Signal(modbv(0)[8:])
    RxText = Signal(modbv(0)[32:])

    @always_seq(clk.posedge, reset=None)
    def Seq():
        if State == RxS.IDLE:
            CNT.next = 0
            ReceiveData.next = 0
            ReceiveEn.next = 0
            Ram.we.next = 0
            Ram.addr.next = 0
            Ram.din.next = 0
            RxEnd.next = 0
            if RxEnReg and RxDataReg == 0x55:
                State.next = RxS.ETH
                CNT.next = CNT + 1

        if State == RxS.ETH:
            if RxEnReg == 0:
                State.next = RxS.IDLE
            elif CNT < Ether_Header_Len - 1:
                CNT.next = CNT + 1
            else:
                CNT.next = 0
                if EtherType[16:8] == 0x08 and  RxDataReg == 0x00:
                    State.next = RxS.IP
                elif EtherType[16:8] == 0x08 and RxDataReg ==0x06:
                    State.next = RxS.ARP
                else:
                    State.next = RxS.IDLE

            if CNT <= 6 and RxDataReg != 0x55: State.next = RxS.IDLE
            if CNT == 7 and RxDataReg != 0xd5: State.next = RxS.IDLE
            if CNT == 8:  desMac.next[48:40]   = RxDataReg
            if CNT == 9:  desMac.next[40:32]   = RxDataReg
            if CNT == 10: desMac.next[32:24]   = RxDataReg
            if CNT == 11: desMac.next[24:16]   = RxDataReg
            if CNT == 12: desMac.next[16:8]    = RxDataReg
            if CNT == 13: desMac.next[8:]      = RxDataReg
            if CNT == 14: srcMac.next[48:40]   = RxDataReg
            if CNT == 15: srcMac.next[40:32]   = RxDataReg
            if CNT == 16: srcMac.next[32:24]   = RxDataReg
            if CNT == 17: srcMac.next[24:16]   = RxDataReg
            if CNT == 18: srcMac.next[16:8]    = RxDataReg
            if CNT == 19: srcMac.next[8:]      = RxDataReg
            if CNT == 20: EtherType.next[16:8] = RxDataReg
            if CNT == 21: EtherType.next[8:]   = RxDataReg

            if CNT == 1: Ram.din.next = 51 #R #For Gui
            if CNT == 2: Ram.din.next = 89 #x
            if CNT == 3: Ram.din.next = 27 #:
            if CNT >= 1 and CNT <= 3:
                Ram.we.next = 1
                if CNT > 1:
                    Ram.addr.next = Ram.addr + 1
            else:
                Ram.we.next = 0

        if State == RxS.ARP:
            if RxEnReg == 0:
                State.next = RxS.IDLE
            elif CNT < ARP_Len + 4 - 1:
                CNT.next = CNT + 1
            else:
                CNT.next = 0
                State.next = RxS.GAP

            if CNT == 1: Ram.din.next = 34 #A #For Gui
            if CNT == 2: Ram.din.next = 51 #R
            if CNT == 3: Ram.din.next = 49 #P
            if CNT >= 1 and CNT <= 3:
                Ram.we.next = 1
                Ram.addr.next = Ram.addr + 1
            else:
                Ram.we.next = 0


        if State == RxS.IP:
            if RxEnReg == 0:
                State.next = RxS.IDLE
            elif CNT < IP_Header_Len - 1:
                CNT.next = CNT + 1
            else:
                CNT.next = 0
                State.next = RxS.UDP

            if CNT == 0:  pass #IP_Version_HeaderLen
            if CNT == 1:  pass #TypeofService
            if CNT == 2:  IP_Total_Length.next[16:8] = RxDataReg
            if CNT == 3:  IP_Total_Length.next[8:]   = RxDataReg
            if CNT == 4:  pass #标识 Identification
            if CNT == 5:  pass
            if CNT == 6:  pass #Flags, Fragment Offset
            if CNT == 7:  pass
            if CNT == 8:  pass #Time to Live
            if CNT == 9:  IP_Protocol.next  = RxDataReg   #Protocol UDP,TCP
            if CNT == 10: pass  #Header Checksum
            if CNT == 11: pass
            if CNT == 12: srcIP.next[32:24] = RxDataReg
            if CNT == 13: srcIP.next[24:16] = RxDataReg
            if CNT == 14: srcIP.next[16:8]  = RxDataReg
            if CNT == 15: srcIP.next[8:]    = RxDataReg
            if CNT == 16: desIP.next[32:24] = RxDataReg
            if CNT == 17: desIP.next[24:16] = RxDataReg
            if CNT == 18: desIP.next[16:8]  = RxDataReg
            if CNT == 19: desIP.next[8:]    = RxDataReg

            if CNT == 10:
                if IP_Protocol == IP_Protocal_TCP:  Ram.din.next = 53 #T
                elif IP_Protocol == IP_Protocal_UDP:  Ram.din.next = 54 #U
                else: Ram.din.next = 57 #X
            if CNT == 11:
                if IP_Protocol == IP_Protocal_TCP:  Ram.din.next = 36 #C
                elif IP_Protocol == IP_Protocal_UDP:  Ram.din.next = 37 #D
                else: Ram.din.next = 57 #X
            if CNT >= 10 and CNT <= 11:
                Ram.we.next = 1
                Ram.addr.next = Ram.addr + 1
            else:
                Ram.we.next = 0


        if State == RxS.UDP:
            if RxEnReg == 0:
                State.next = RxS.IDLE
            elif CNT < UDP_Header_Len - 1:
                CNT.next = CNT + 1
            else:
                CNT.next = 0
                State.next = RxS.DATA

            if CNT == 0:  srcPort.next[16:8]    = RxDataReg
            if CNT == 1:  srcPort.next[8:]      = RxDataReg
            if CNT == 2:  desPort.next[16:8]    = RxDataReg
            if CNT == 3:  desPort.next[8:]      = RxDataReg
            if CNT == 4:  UDP_Length.next[16:8] = RxDataReg  #UDP Length
            if CNT == 5:  UDP_Length.next[8:]   = RxDataReg
            if CNT == 6:  pass  #UDP Header Checksum
            if CNT == 7:  pass

        if State == RxS.DATA:
            if RxEnReg == 0:
                State.next = RxS.IDLE
            elif CNT < UDP_Length - UDP_Header_Len + Ether_CRC_LEN - 1:
                CNT.next = CNT + 1
            else:
                CNT.next = 0
                State.next = RxS.GAP

            if CNT < UDP_Length - UDP_Header_Len:
                ReceiveData.next = RxDataReg
                ReceiveEn.next = 1
            else:
                ReceiveEn.next = 0 #CRC
                ReceiveData.next = 0

            if CNT == 0: RxText.next[32:24] = RxDataReg
            if CNT == 1: RxText.next[24:16] = RxDataReg
            if CNT == 2: RxText.next[16: 8] = RxDataReg
            if CNT == 3: RxText.next[8 :  ] = RxDataReg

            if CNT == 0: Ram.din.next = 0
            if CNT == 1: Ram.din.next = ToChar(int(RxText[32:28]))
            if CNT == 2: Ram.din.next = ToChar(int(RxText[28:24]))
            if CNT == 3: Ram.din.next = ToChar(int(RxText[24:20]))
            if CNT == 4: Ram.din.next = ToChar(int(RxText[20:16]))
            if CNT == 5: Ram.din.next = ToChar(int(RxText[16:12]))
            if CNT == 6: Ram.din.next = ToChar(int(RxText[12:8] ))
            if CNT == 7: Ram.din.next = ToChar(int(RxText[8:4]  ))
            if CNT == 8: Ram.din.next = ToChar(int(RxText[4:]   ))

            if CNT >= 0 and CNT <= 8:
                Ram.we.next = 1
                Ram.addr.next = Ram.addr + 1
            else:
                Ram.we.next = 0


        if State == RxS.GAP:
            Ram.we.next = 0
            if CNT < InterframeGap_Len - 7:
                CNT.next = CNT + 1
            else:
                CNT.next = 0
                State.next = RxS.IDLE
                RxEnd.next = 1

        RxEnReg.next   = RxEn
        RxDataReg.next = RxData
        
    return instances()