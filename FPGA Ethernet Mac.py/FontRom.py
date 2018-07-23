from Globals import *

rfile = open('Font.dat', 'rb')
RomData = pickle.load(rfile)
rfile.close()

@block
def FontRom(clk, Rom):

    @always_seq(clk.posedge, reset=None)
    def rom_read():
        Rom.dout.next = RomData[int(Rom.addr)]

    return instances()