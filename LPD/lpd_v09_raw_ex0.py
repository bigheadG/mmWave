''' 
Long range People Detect (ISK) for BM-201" : 2019/12/04 
ex0:
Hardware: Batman-201 ISK

V6: Point Cloud Spherical
	v6 structure: [(range,azimuth,elevation,doppler),......]
	
V7: Target Object List
	V7 structure: [(tid,posX,posY,velX,velY,accX,accY,posZ,velZ,accZ),....]
	
V8: Target Index
	V8 structure: [id1,id2....]
	
V9:Point Cloud Side Info
	v9 structure: [(snr,noise'),....]

(1)Download lib:
install:
~#sudo pip intall mmWave
update:
~#sudo pip install mmWave -U
'''

import serial
import numpy as np
from mmWave import lpdISK

#UART initial

try:    #pi 3
	port = serial.Serial("/dev/ttyS0",baudrate = 921600, timeout = 0.5)
except:  #for Jetson nano UART port
	port = serial.Serial("/dev/ttyTHS1",baudrate = 921600, timeout = 0.5)

pm = lpdISK.LpdISK(port)

def uartGetdata(name):
	print("mmWave: {:} example:".format(name))
	port.flushInput()
	while True:
		hdr = pm.getHeader()
		(dck,v6,v7,v8,v9)=pm.tlvRead(False) 
		if dck:
			print("V6:V7:V8:V9 = length([{:d},{:d},{:d},{:d}])".format(len(v6),len(v7),len(v8),len(v9)))
			if len(v6) != 0:
				print("V6: Point Cloud Spherical v6:len({:d})-----------------".format(len(v6)))
				#[(range,azimuth,elevation,doppler),......]
				print(v6)
			if len(v7) != 0:
				print("V7: Target Object List----v7:len({:d})-----------------".format(len(v7)))
				#[(tid,posX,posY,velX,velY,accX,accY,posZ,velZ,accZ),....]
				print(v7)
			if len(v8) != 0:
				print("V8: Target Index----------v8:len({:d})-----------------".format(len(v8)))
				#[id1,id2....]
				print(v8)
			if len(v9) != 0:
				print("V9:Point Cloud Side Info--v9:len({:d})-----------------".format(len(v9)))
				#[(snr,noise'),....]
				print(v9)
			
uartGetdata("Long range People Detect (LPD) for BM-201")






