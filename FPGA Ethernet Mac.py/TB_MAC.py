from Mac_Ctrl import *

@block
def test_mac(Convert = False):
    clk,TxEn,SendEn, Dkey2, RxEn, TxErr, ReceiveEn, Clear = (Signal(bool(0)) for i in range(8))
    TxData, RxData = (Signal(modbv(0)[8:]) for i in range(2))
    Ram_MacText = RAM(11, 9)
    DataLength = Signal(modbv(7)[16:])
    GapLength = Signal(modbv(0)[16:])
    TxCNT, RxCNT, TxLimit = (Signal(modbv(1)[24:]) for i in range(3))
    FrameRate = Signal(modbv(0)[8:])

    iMac_Ctrl = Mac_Ctrl(clk, TxEn, TxErr, TxData, TxEn, TxData, SendEn, Dkey2, Clear, Ram_MacText, DataLength, GapLength,TxCNT, RxCNT, TxLimit, FrameRate)

    @instance
    def clkgen():
        while True:
            clk.next = not clk
            yield  delay(5)

    @instance
    def stimulus_mac():
        for i in range(4000):
            if i == 10:
                SendEn.next = 1
            else:
                SendEn.next = 0
            yield clk.negedge
        raise StopSimulation()


    return instances()

tbmac = test_mac()
tbmac.config_sim(trace = True)
#tbmac.convert(hdl="Verilog", initial_values=True)
tbmac.run_sim()