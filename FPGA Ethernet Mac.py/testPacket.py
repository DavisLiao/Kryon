from scapy.sendrecv import sniff

#dpkt = sniff(count=2)
#sniff(iface='Realtek PCIe GBE Family Controller', count= 2, prn=lambda x:x.show())

pkts = sniff(count = 1)
pkt = pkts[0]
pkt