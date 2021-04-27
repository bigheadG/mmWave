''' 
Traffic Monitoring Detection Roadway Sensing (ISK) for BM-201" : 2021/04/17
ex0:
Hardware: BM201-TRS kit


(1)Download lib:
install:
~#sudo pip3 intall mmWave
update:
~#sudo pip3 install mmWave -U

install numpy
~#sudo pip3 install numpy

'''

import serial
import numpy as np
from mmWave import roadwayTMD_kv

#port = serial.Serial("COM189",baudrate = 921600, timeout = 0.5)
port = serial.Serial("/dev/tty.usbmodemGY0052534",baudrate = 921600 , timeout = 0.5) 

trs = roadwayTMD_kv.roadwayTmdISK_kv(port)

def uartGetdata(name):
	print("mmWave: {:} example:".format(name))
	port.flushInput()
	while True:
		(dck,v21)=trs.tmdRead(False)
		if dck:
			print(v21)
			 
uartGetdata("Traffic Monitoring Detection Roadway Sensing (TRS) for BM-201")
