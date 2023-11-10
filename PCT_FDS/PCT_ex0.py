#=============================================
# File Name: PCT_ex0.py
#
# Requirement:
# Hardware: AOP
# Firmware: 
# lib: pct : People Counting with Tilt
# show V6,V7,V8
# type: raw
# Application: output RAW data
#
#=============================================
import serial
import struct
import datetime

import numpy as np
from mmWave import pct



#pi 3 or pi 4
#port = serial.Serial("/dev/ttyS0",baudrate = 921600, timeout = 0.5)
#for Jetson nano UART port
#port = serial.Serial("/dev/ttyTHS1",baudrate = 921600, timeout = 0.5)
#port = serial.Serial("/dev/tty.usbmodemGY0052534",baudrate = 921600 , timeout = 0.5)
#port = serial.Serial("/dev/ttyACM1",baudrate = 921600 , timeout = 0.5)
port = serial.Serial("/dev/tty.SLAB_USBtoUART5",baudrate = 921600, timeout = 0.5)  


#
# dataType : false is list output more fast  
#          : true is Easy to observe but low performance
#
dataType = False 

if dataType:
	radar = pct.Pct(port,tiltAngle=45,height = 2.41,df = "DataFrame")
else:
	radar = pct.Pct(port,tiltAngle=45,height = 2.41)


fn = 0
prev_fn = 0
def uartGetTLVdata(name):
	global fn,prev_fn
	port.flushInput()
	while True:	
		 
		(dck,v6,v7,v8) = radar.tlvRead(False )
		#Show header information
		#pm.headerShow()
		hdr = radar.getHeader()
		fn = radar.frameNumber
		if dck and fn != prev_fn:
			prev_fn = fn
			print(f"\n\n\n====================== {fn} ===============================")
			print(f"fn={fn} lenth of:[v6:{len(v6)} :v7:{len(v7)}:v8:{len(v8)}]")
			
			if len(v6) != 0:
				
				print("\n-------------------- V6 -------------------------")
				#[(sx,sy,sz,range,elv,azimuth,doppler,snr).....(...)]
				print("V6: Point Cloud Spherical v6:len({:d})".format(len(v6)))
				print(v6)
						 
			if len(v7) != 0:
				print("\n-------------------- V7 -------------------------")
				print("V7: Target List :len({:d})".format(len(v7)))
				print(v7)
							
			if len(v8) != 0:
				print("\n-------------------- V8 -------------------------")
				print("V8: TargetID :len({:d})".format(len(v8)))
				print(v8)
			
		port.flushInput()
				
uartGetTLVdata("po3VOH-POS")
 
