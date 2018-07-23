from myhdl import *

@block
def CRC32(clk, Reset, Data_in, Enable, CrcO,CrcNext):
    Data = Signal(modbv(0)[8:])
    Crc = Signal(modbv(0xffffffff)[32:])

    @always_comb
    def rData():
        Data.next[0] = Data_in[7]
        Data.next[1] = Data_in[6]
        Data.next[2] = Data_in[5]
        Data.next[3] = Data_in[4]
        Data.next[4] = Data_in[3]
        Data.next[5] = Data_in[2]
        Data.next[6] = Data_in[1]
        Data.next[7] = Data_in[0]

    @always_comb
    def Comb1():
        CrcNext.next[0] = Crc[24] ^ Crc[30] ^ Data[0] ^ Data[6]
        CrcNext.next[1] = Crc[24] ^ Crc[25] ^ Crc[30] ^ Crc[31] ^ Data[0] ^ Data[1] ^ Data[6] ^ Data[7]
        CrcNext.next[2] = Crc[24] ^ Crc[25] ^ Crc[26] ^ Crc[30] ^ Crc[31] ^ Data[0] ^ Data[1] ^ Data[2] ^ Data[6] ^ \
                          Data[7]
        CrcNext.next[3] = Crc[25] ^ Crc[26] ^ Crc[27] ^ Crc[31] ^ Data[1] ^ Data[2] ^ Data[3] ^ Data[7]
        CrcNext.next[4] = Crc[24] ^ Crc[26] ^ Crc[27] ^ Crc[28] ^ Crc[30] ^ Data[0] ^ Data[2] ^ Data[3] ^ Data[4] ^ \
                          Data[6]
        CrcNext.next[5] = Crc[24] ^ Crc[25] ^ Crc[27] ^ Crc[28] ^ Crc[29] ^ Crc[30] ^ Crc[31] ^ Data[0] ^ Data[1] ^ \
                          Data[3] ^ Data[4] ^ Data[5] ^ Data[6] ^ Data[7]
        CrcNext.next[6] = Crc[25] ^ Crc[26] ^ Crc[28] ^ Crc[29] ^ Crc[30] ^ Crc[31] ^ Data[1] ^ Data[2] ^ Data[4] ^ \
                          Data[5] ^ Data[6] ^ Data[7]
        CrcNext.next[7] = Crc[24] ^ Crc[26] ^ Crc[27] ^ Crc[29] ^ Crc[31] ^ Data[0] ^ Data[2] ^ Data[3] ^ Data[5] ^ \
                          Data[7]
        CrcNext.next[8] = Crc[0] ^ Crc[24] ^ Crc[25] ^ Crc[27] ^ Crc[28] ^ Data[0] ^ Data[1] ^ Data[3] ^ Data[4]
        CrcNext.next[9] = Crc[1] ^ Crc[25] ^ Crc[26] ^ Crc[28] ^ Crc[29] ^ Data[1] ^ Data[2] ^ Data[4] ^ Data[5]
        CrcNext.next[10] = Crc[2] ^ Crc[24] ^ Crc[26] ^ Crc[27] ^ Crc[29] ^ Data[0] ^ Data[2] ^ Data[3] ^ Data[5]
        CrcNext.next[11] = Crc[3] ^ Crc[24] ^ Crc[25] ^ Crc[27] ^ Crc[28] ^ Data[0] ^ Data[1] ^ Data[3] ^ Data[4]
        CrcNext.next[12] = Crc[4] ^ Crc[24] ^ Crc[25] ^ Crc[26] ^ Crc[28] ^ Crc[29] ^ Crc[30] ^ Data[0] ^ Data[1] ^ \
                           Data[2] ^ Data[4] ^ Data[5] ^ Data[6]
        CrcNext.next[13] = Crc[5] ^ Crc[25] ^ Crc[26] ^ Crc[27] ^ Crc[29] ^ Crc[30] ^ Crc[31] ^ Data[1] ^ Data[2] ^ \
                           Data[3] ^ Data[5] ^ Data[6] ^ Data[7]
        CrcNext.next[14] = Crc[6] ^ Crc[26] ^ Crc[27] ^ Crc[28] ^ Crc[30] ^ Crc[31] ^ Data[2] ^ Data[3] ^ Data[4] ^ \
                           Data[6] ^ Data[7]
        CrcNext.next[15] = Crc[7] ^ Crc[27] ^ Crc[28] ^ Crc[29] ^ Crc[31] ^ Data[3] ^ Data[4] ^ Data[5] ^ Data[7]
        CrcNext.next[16] = Crc[8] ^ Crc[24] ^ Crc[28] ^ Crc[29] ^ Data[0] ^ Data[4] ^ Data[5]
        CrcNext.next[17] = Crc[9] ^ Crc[25] ^ Crc[29] ^ Crc[30] ^ Data[1] ^ Data[5] ^ Data[6]
        CrcNext.next[18] = Crc[10] ^ Crc[26] ^ Crc[30] ^ Crc[31] ^ Data[2] ^ Data[6] ^ Data[7]
        CrcNext.next[19] = Crc[11] ^ Crc[27] ^ Crc[31] ^ Data[3] ^ Data[7]
        CrcNext.next[20] = Crc[12] ^ Crc[28] ^ Data[4]
        CrcNext.next[21] = Crc[13] ^ Crc[29] ^ Data[5]
        CrcNext.next[22] = Crc[14] ^ Crc[24] ^ Data[0]
        CrcNext.next[23] = Crc[15] ^ Crc[24] ^ Crc[25] ^ Crc[30] ^ Data[0] ^ Data[1] ^ Data[6]
        CrcNext.next[24] = Crc[16] ^ Crc[25] ^ Crc[26] ^ Crc[31] ^ Data[1] ^ Data[2] ^ Data[7]
        CrcNext.next[25] = Crc[17] ^ Crc[26] ^ Crc[27] ^ Data[2] ^ Data[3]
        CrcNext.next[26] = Crc[18] ^ Crc[24] ^ Crc[27] ^ Crc[28] ^ Crc[30] ^ Data[0] ^ Data[3] ^ Data[4] ^ Data[6]
        CrcNext.next[27] = Crc[19] ^ Crc[25] ^ Crc[28] ^ Crc[29] ^ Crc[31] ^ Data[1] ^ Data[4] ^ Data[5] ^ Data[7]
        CrcNext.next[28] = Crc[20] ^ Crc[26] ^ Crc[29] ^ Crc[30] ^ Data[2] ^ Data[5] ^ Data[6]
        CrcNext.next[29] = Crc[21] ^ Crc[27] ^ Crc[30] ^ Crc[31] ^ Data[3] ^ Data[6] ^ Data[7]
        CrcNext.next[30] = Crc[22] ^ Crc[28] ^ Crc[31] ^ Data[4] ^ Data[7]
        CrcNext.next[31] = Crc[23] ^ Crc[29] ^ Data[5]

    @always_seq(clk.posedge, reset=None)
    def Seq():
        if Reset:
            Crc.next = 0xffffffff
        elif Enable:
            Crc.next = CrcNext

    @always_comb
    def Comb2():
        CrcO.next[0] =  not Crc[7]
        CrcO.next[1] =  not Crc[6]
        CrcO.next[2] =  not Crc[5]
        CrcO.next[3] =  not Crc[4]
        CrcO.next[4] =  not Crc[3]
        CrcO.next[5] =  not Crc[2]
        CrcO.next[6] =  not Crc[1]
        CrcO.next[7] =  not Crc[0]
        CrcO.next[8] =  not Crc[15]
        CrcO.next[9] =  not Crc[14]
        CrcO.next[10] = not Crc[13]
        CrcO.next[11] = not Crc[12]
        CrcO.next[12] = not Crc[11]
        CrcO.next[13] = not Crc[10]
        CrcO.next[14] = not Crc[9]
        CrcO.next[15] = not Crc[8]
        CrcO.next[16] = not Crc[23]
        CrcO.next[17] = not Crc[22]
        CrcO.next[18] = not Crc[21]
        CrcO.next[19] = not Crc[20]
        CrcO.next[20] = not Crc[19]
        CrcO.next[21] = not Crc[18]
        CrcO.next[22] = not Crc[17]
        CrcO.next[23] = not Crc[16]
        CrcO.next[24] = not Crc[31]
        CrcO.next[25] = not Crc[30]
        CrcO.next[26] = not Crc[29]
        CrcO.next[27] = not Crc[28]
        CrcO.next[28] = not Crc[27]
        CrcO.next[29] = not Crc[26]
        CrcO.next[30] = not Crc[25]
        CrcO.next[31] = not Crc[24]

    return instances()