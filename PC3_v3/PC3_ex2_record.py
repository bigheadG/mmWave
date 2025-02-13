#=============================================
# File Name: pc3_ex2_record.py
#
# Requirement:
# Hardware: BM201-PC3
# Firmware: 
# lib: pc3
# Get V6,V7 and V8 
# type: raw data (DataFrame)
# Application: Get RAW data from radar sensor
#    Save v6,v7 and v8 data in csv file.
#=============================================
import serial
import struct
import datetime

import numpy as np
from mmWave import  pc3_v2

from datetime import date,datetime,time
import csv
import pandas as pd


#pi 3 or pi 4
#port = serial.Serial("/dev/ttyS0",baudrate = 921600, timeout = 0.5)
#for Jetson nano UART port
#port = serial.Serial("/dev/ttyTHS1",baudrate = 921600, timeout = 0.5)
#port = serial.Serial("/dev/tty.usbmodemGY0052534",baudrate = 921600 , timeout = 0.5)
#port = serial.Serial("/dev/ttyACM1",baudrate = 921600 , timeout = 0.5)
#port = serial.Serial("/dev/tty.SLAB_USBtoUART5",baudrate = 921600, timeout = 0.5)  
port = serial.Serial("/dev/ttyUSB0",baudrate = 921600, timeout = 0.5)

#
#initial global value
#

radar = pc3_v2.Pc3_v2(port)

tt = datetime.now()
dt = tt.strftime("%Y-%m-%d-%H-%M-%S")  # Date Format
fileName = "pc3_{:}.csv".format(dt)

v6_col_names = ['time','fN','type','elv','azimuth','range','doppler','snr','sx', 'sy', 'sz']
v7_col_names = ['time','fN','type','posX','posY','posZ','velX','velY','velZ','accX','accY','accZ','ec0','ec1','ec2','ec3','ec4','ec5','ec6','ec7','ec8','ec9','ec10','ec11','ec12','ec13','ec14','ec15','g','confi','tid']
v8_col_names = ['time','fN','type','targetID']


# UART : 50 ms
def uartGetTLVdata(name):
	port.flushInput()
	#Display 
	#radar.useDebug(True)
	#radar.stateMachine(True)
	with open(fileName, 'w', newline='') as csvfile:
		fieldNames = v7_col_names
		writer = csv.writer(csvfile)
		writer.writerow(fieldNames)
		
		while True:
			(dck,v6,v7,v8) = radar.tlvRead(False,df = 'DataFrame' )
			#(dck,v6,v7,v8) = radar.tlvRead(False)
			#Show header information
			#pm.headerShow()
			hdr = radar.getHeader()
			print(v6) 
			ts = datetime.now()
			 
			if len(v6) != 0:
				print("\n-------------------- V6 -------------------------")
				#[(elv,azimuth,range,doppler,snr,sx,sy,sz).....(...)]
				print("V6: Point Cloud Spherical v6:len({:d})".format(len(v6)))
				print(v6)
				
				for i in range(len(v6)):
					v6i = [ts]
					v6i.extend(v6.iloc[i])
					writer.writerow(v6i)
					
			if len(v7) != 0:
				print("\n-------------------- V7 -------------------------")
				print("V7: Target List :len({:d})".format(len(v7)))
				print(v7)
				
				for i in range(len(v7)):
					v7i = [ts]
					v7i.extend(v7.iloc[i])
					writer.writerow(v7i)

			if len(v8) > 2:
				print("\n-------------------- V8 -------------------------")
				print("V8: TargetID :len({:d})".format(len(v8)-2))
				print(v8)
				writer.writerow([ts,v8[0],'v8',v8[2:]])
			
		port.flushInput()
				
uartGetTLVdata("pc3")






