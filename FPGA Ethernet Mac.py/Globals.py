from myhdl import *
import numpy as np
import pickle

#arp -s 192.168.0.7 aa-bb-cc-dd-ee-ff
#0x55 0xd5

Preamble_Len, DestinationMAC_Len, SourceMac_Len, EtherType_Len = 8, 6 ,6, 2
Ether_Header_Len = 22
ARP_Len = 28
IP_Header_Len = 20
UDP_Header_Len = 8
Ether_CRC_LEN = 4

InterframeGap_Len = 24 #12

EtherType_IPv4 = 0x800
EtherType_ARP = 0x0806

IP_Version_HeaderLen = 0x45
TypeofService = 0x00

IP_Protocal_TCP = 6
IP_Protocal_UDP = 17

SourceMac = Signal(modbv(0xaabbccddeeff)[48:])
DestinationMAC = Signal(modbv(0xf07959e0857b)[48:])

SourceIP = Signal(modbv(0xc0a80007)[32:]) #[0xc0,0xa8,0x00,0x7]  #192.168.0.7
DestinationIP = Signal(modbv(0xc0a8005b)[32:]) #[0xc0,0xa8,0x00,0x5b]  #192.168.0.91

WHb = 12
TestWidth, TestHeight = 1200, 700


def Text(String):
    code = [Signal(modbv(ord(s) - 31)[8:0]) for s in String]
    return code

def Char2code(char):
    return ord(char) - 31

def Txt(String):
    code = [(ord(s) - 31) for s in String]
    return code

class COLOR:
    def __init__(self, r = 0, g = 0, b = 0):
        self.R = Signal(modbv(r)[8:])
        self.G = Signal(modbv(g)[8:])
        self.B = Signal(modbv(b)[8:])

class SIZE:
    def __init__(self, w = 0, h = 0):
        self.W = Signal(modbv(w)[WHb:])
        self.H = Signal(modbv(h)[WHb:])

class LOC:
    def __init__(self, X = 0, Y = 0):
        self.x = Signal(modbv(X)[WHb:])
        self.y = Signal(modbv(Y)[WHb:])

class RAM:
    def __init__(self,addrWidth, dataWidth):
        self.we = Signal(bool(0))
        self.addr = Signal(modbv(0)[addrWidth:])
        self.din = Signal(modbv(0)[dataWidth:])
        self.dout = Signal(modbv(0)[dataWidth:])



BLACK = COLOR(0, 0, 0)
RED = COLOR(255, 0, 0)
GREEN = COLOR(0, 255, 0)
BLUE = COLOR(0, 0, 255)
YELLOW = COLOR(255, 255, 0)
WHITE = COLOR(255, 255, 255)







