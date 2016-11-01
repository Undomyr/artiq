from migen import *
from misoc.interconnect import wishbone


class Mailbox(Module):
    def __init__(self, size=1):
        self.i1 = wishbone.Interface()
        self.i2 = wishbone.Interface()

        # # #

        values = Array([Signal(32) for _ in range(size)])
        for i in self.i1, self.i2:
            self.sync += [
                i.dat_r.eq(values[i.adr & 0xff]),
                i.ack.eq(0),
                If(i.cyc & i.stb & ~i.ack,
                    i.ack.eq(1),
                    If(i.we, values[i.adr & 0xff].eq(i.dat_w))
                )
            ]
