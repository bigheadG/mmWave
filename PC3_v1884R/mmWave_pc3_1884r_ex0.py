############################################################
# mmWave_pc3_1884r_ex0.py 2022.12.23
#
# v1010 (Target List)
# v1011 (Target Index)
# v1012 (Target Height)
# v1020 (V1020 Point Cloud)
# v1021 (Prescence Indication)
#  
#  library install:
#  (1)pySerial Library
#  		$sudo pip3 install pySerial
#  (2)numpy install
#		$sudo pip3 install numpy
# 

import serial
import numpy as np
from mmWave import pc3_v1884R

#UART initial
port = serial.Serial("/dev/tty.usbmodemGY0050694",baudrate = 921600, timeout = 0.5)

radar =  pc3_v1884R.pc3_v1884R(port)

def uartGetdata(name):
	print("mmWave: {:} example:".format(name))
	port.flushInput()
	
	while True:
		(dck,v1010,v1011,v1012,v1020,v1021) = radar.tlvRead(False)
		#hdr = radar.getHeader()
		fn = radar.frameNumber
		
		print(f"\n============= frame Number:{fn} ================")
		if len(v1010) != 0:
			print(f"v1010 (Target List): {v1010}\n")
		if len(v1011) != 0:
			print(f"v1011 (Target Index): {v1011}\n")
		if len(v1012) != 0:
			print(f"v1012 (Target Height): {v1012}\n")
		if len(v1020) != 0:
			print(f"v1020:(Point Cloud) {v1020}\n")
		if len(v1021) != 0:
			print(f"v1021 (Prescence Indication): {v1021}\n")
			
uartGetdata("mmWave-PC3 BM-201 for 1884R")






