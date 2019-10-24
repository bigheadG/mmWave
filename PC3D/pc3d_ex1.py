''' 
ODS People Overhead Counting 3D : 2019/10/15 15:47
ex0:
Hardware: Batman-301 OSD

Scene Parameter: x:[-1.18,2.12] y:[1.00,2.0] z:[-0.05,2.0] 
      Z
      |
     / \
	X   Y

(1)Download lib:
version: over mmWave V.0.1.21
install:
~#sudo pip intall mmWave
update:
~#sudo pip install mmWave -U
'''
import serial
import struct
import datetime

import numpy as np
from mmWave import people3D
import people3D as people3D


#UART initial
'''
try:    #pi 3
	port = serial.Serial("/dev/ttyS0",baudrate = 921600, timeout = 0.5)
except: #pi 2
	port = serial.Serial("/dev/ttyAMA0",baudrate = 921600, timeout = 0.5)
'''
#
#initial global value
#

#for Jetson nano UART port
port = serial.Serial("/dev/ttyTHS1",baudrate = 921600, timeout = 0.5)

pm = people3D.People3D(port)

# UART : 100 ms
def uartGetPC3Ddata(name):
	print("mmWave: {:} example:".format(name))
	pt = datetime.datetime.now()
	ct = datetime.datetime.now()
	port.flushInput()
 
	while True:
		ct = datetime.datetime.now()
		(dck,p3) = pm.pc3dRead(False)
		
		if dck:
			print("{} {}".format(ct-pt,p3))
			#print("flow#({:d}) numObj:{:d} objIdx:{:d} tid:{:d} [{:f}:{:f}:{:f}] {}".format(p3.flow,p3.numObj,p3.oidx,p3.tid,p3.x,p3.y,p3.z,ct-pt))
			 
uartGetPC3Ddata("PC3D: People Overhead Counting (OSD) 3D")






