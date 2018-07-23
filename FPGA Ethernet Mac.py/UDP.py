from socket import *
from numba import jit
import threading
import numpy as np
from PIL import Image

PicWidth = 1024
PicHeight = 512

HOST = '192.168.0.91'
PORT = 57788
DESIP_Port = ('192.168.0.7',57766)

s = socket(AF_INET, SOCK_DGRAM)
s.bind((HOST, PORT))
s.setsockopt(SOL_SOCKET, SO_RCVBUF, 2048000000)
bsize = s.getsockopt(SOL_SOCKET, SO_RCVBUF)
print(bsize)
n = 0
RxPic = True


def receive():
    while RxPic:
        global n
        index = 0
        data,address = s.recvfrom(57788)    
        #print(data,address)
        #print(type(data))
        n += 1
        print(n)
        #s.sendto((str(n)).encode('ascii'),address)


th1 = threading.Thread(target=receive)

th1.start()
s.sendto(bytearray([1,2,3,4,5,6,7]),DESIP_Port)   






