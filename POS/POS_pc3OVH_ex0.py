#=============================================
# File Name: POS_pc3OVH_ex0.py
#
# Requirement:
# Hardware: AOP
# Firmware: 
# lib: pc3OVH
# show V6,V7,V8
# type: raw
# Application: output RAW data
#
#=============================================
import serial
import struct
import datetime

import numpy as np
from mmWave import pc3OVH
from datetime import date,datetime,time
import pandas as pd


#pi 3 or pi 4
#port = serial.Serial("/dev/ttyS0",baudrate = 921600, timeout = 0.5)
#for Jetson nano UART port
#port = serial.Serial("/dev/ttyTHS1",baudrate = 921600, timeout = 0.5)
#port = serial.Serial("/dev/tty.usbmodemGY0052534",baudrate = 921600 , timeout = 0.5)
#port = serial.Serial("/dev/ttyACM1",baudrate = 921600 , timeout = 0.5)
port = serial.Serial("/dev/tty.SLAB_USBtoUART5",baudrate = 921600, timeout = 0.5)  

#
#initial global value
#

radar = pc3OVH.Pc3OVH(port)

tt = datetime.now()
dt = tt.strftime("%Y-%m-%d-%H-%M-%S")  # Date Format

v6_col_names = ['time','fN','type','elv','azimuth','range','doppler','snr','sx', 'sy', 'sz']
v7_col_names = ['time','fN','type','posX','posY','posZ','velX','velY','velZ','accX','accY','accZ','ec0','ec1','ec2','ec3','ec4','ec5','ec6','ec7','ec8','ec9','ec10','ec11','ec12','ec13','ec14','ec15','g','confi','tid']
v8_col_names = ['time','fN','type','targetID']


def uartGetTLVdata(name):
	port.flushInput()
	while True:	
		(dck,v6,v7,v8) = radar.tlvRead(False,df = 'DataFrame' )
		#Show header information
		#pm.headerShow()
		hdr = radar.getHeader()
				 
		if dck:
			ts = datetime.now()
			if len(v6) != 0:
				print("\n-------------------- V6 -------------------------")
				#[(elv,azimuth,range,doppler,snr,sx,sy,sz).....(...)]
				print("V6: Point Cloud Spherical v6:len({:d})".format(len(v6)))
				print(v6)
						 
			if len(v7) != 0:
				print("\n-------------------- V7 -------------------------")
				print("V7: Target List :len({:d})".format(len(v7)))
				print(v7)
							
			if len(v8) > 2:
				print("\n-------------------- V8 -------------------------")
				print("V8: TargetID :len({:d})".format(len(v8)-2))
				print(v8)
					
				
				
uartGetTLVdata("po3VOH-POS")






