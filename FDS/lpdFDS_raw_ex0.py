''' 
Falling Detection Sensing  (ISK) for BM-201" : 2021/05/26 
ex0:
Hardware: Batman-201 ISK

V6: Point Cloud Spherical
	v6 structure: #[(fN,type,range,azimuth,elv,doppler,sx,sy,sz),......]
	
V7: Target Object List
	V7 structure: #[( fN,typ,posX,posY  ...ec15,g,confi,tid),....]
	
V8: Target Index
	V8 structure: #[id1,id2....]
	
V9:Point Cloud Side Info
	v9 structure: #[(snr,noise'),....]

(1)Download lib:
install:
~#sudo pip intall mmWave
update:
~#sudo pip install mmWave -U
'''

import serial
import numpy as np
from mmWave import lpdFDS


#UART initial
###################################################################
#
#use USB-UART
#port = serial.Serial("/dev/ttyUSB0",baudrate = 921600, timeout = 0.5)
#
#for Jetson nano UART port
#port = serial.Serial("/dev/ttyTHS1",baudrate = 921600, timeout = 0.5) 
#
#for pi 4 UART port
#port = serial.Serial("/dev/ttyS0",baudrate = 921600, timeout = 0.5)
#
#Drone Object Detect Radar initial 
#port = serial.Serial("/dev/tty.usbmodemGY0052534",baudrate = 921600, timeout = 0.5)
#port = serial.Serial("/dev/tty.usbmodem14103",baudrate = 115200 , timeout = 0.5)  
port = serial.Serial("/dev/tty.usbmodemGY0043864",baudrate = 921600, timeout = 0.5) 
#port = serial.Serial("/dev/tty.SLAB_USBtoUART3",baudrate = 921600, timeout = 0.5)   

#for NUC ubuntu 
#port = serial.Serial("/dev/ttyACM1",baudrate = 921600, timeout = 0.5

radar = lpdFDS.LpdFDS(port)

def uartGetdata(name):
	print("mmWave: {:} example:".format(name))
	port.flushInput()
	while True:
		hdr = radar.getHeader()
		(dck,v6,v7,v8,v9)  = radar.tlvRead(False,df = 'DataFrame')
	
		hdr = radar.getHeader()
		fn = hdr.frameNumber
	
		if dck:
			print("V6:V7:V8:V9 = length([{:d},{:d},{:d},{:d}])".format(len(v6),len(v7),len(v8),len(v9)))
			if len(v6) != 0:
				print("V6: Point Cloud Spherical v6:len({:d})-----------------".format(len(v6)))
				#[(fN,type,range,azimuth,elv,doppler,sx,sy,sz),......]
				print(v6)
			if len(v7) != 0:
				print("V7: Target Object List----v7:len({:d})-----------------".format(len(v7)))
				#[( fN,typ,posX,posY  ...ec15,g,confi,tid),....]
				print(v7)
			if len(v8) != 0:
				print("V8: Target Index----------v8:len({:d})-----------------".format(len(v8)))
				#[id1,id2....]
				print(v8)
			if len(v9) != 0:
				print("V9:Point Cloud Side Info--v9:len({:d})-----------------".format(len(v9)))
				#[(snr,noise'),....]
				print(v9)
			
uartGetdata("Falling Detect Sensing (FDS) for BM-201")






