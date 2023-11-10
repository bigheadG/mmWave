#=============================================
# File Name: PCT_ex2_record.py
#
# Requirement:
# Hardware: BM201-PCT
# Firmware: 
# lib: pct
# Get V6,V7 and V8 
# type: raw data (DataFrame)
# Application: Record RAW data
#    Save v6,v7 and v8 data in csv file.
#=============================================
import serial
import struct
import datetime

import numpy as np
from mmWave import pct
from datetime import date,datetime,time
import csv
import pandas as pd


###################################################################################
# Parameters:
PORT = '/dev/tty.SLAB_USBtoUART5'
JB_TILT_DEGREE = 45  
JB_RADAR_INSTALL_HEIGHT = 2.41  

#pi 3 or pi 4
#port = serial.Serial("/dev/ttyS0",baudrate = 921600, timeout = 0.5)
#for Jetson nano UART port
#port = serial.Serial("/dev/ttyTHS1",baudrate = 921600, timeout = 0.5)
#port = serial.Serial("/dev/tty.usbmodemGY0052534",baudrate = 921600 , timeout = 0.5)
#port = serial.Serial("/dev/ttyACM1",baudrate = 921600 , timeout = 0.5)


port = serial.Serial(PORT,baudrate = 921600, timeout = 0.5)  
radar = pct.Pct(port,tiltAngle=JB_TILT_DEGREE,height = JB_RADAR_INSTALL_HEIGHT,df = "DataFrame")

tt = datetime.now()
dt = tt.strftime("%Y-%m-%d-%H-%M-%S")  # Date Format
fileName = "pct_{:}.csv".format(dt)



v6_col_names = ['time','fN','type','sx', 'sy', 'sz','range','elv','azimuth','doppler','snr']
v7_col_names = ['time','fN','type','tid','posX','posY','posZ','velX','velY','velZ','accX','accY','accZ','ec0','ec1','ec2','ec3','ec4','ec5','ec6','ec7','ec8','ec9','ec10','ec11','ec12','ec13','ec14','ec15','g','confi'] #v0.1.2
v8_col_names = ['time','fN','type','targetID']


# UART : 50 ms
fn = 0
prev_fn = 0

def uartGetTLVdata(name):
	global fn, prev_fn
	port.flushInput()
	#Display 
	#pm.useDebug(True)
	#pm.stateMachine(True)
	with open(fileName, 'w', newline='') as csvfile:
		fieldNames = v7_col_names
		writer = csv.writer(csvfile)
		writer.writerow(fieldNames)
		
		while True:
			(dck,v6,v7,v8) = radar.tlvRead(False)
			#Show header information
			#pm.headerShow()
			hdr = radar.getHeader()
			fn = radar.frameNumber
			
			if dck == True and fn != prev_fn:
				prev_fn = fn 
				ts = datetime.now()
				if len(v6) != 0:
					print("\n-------------------- V6 -------------------------")
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
					print("V8: TargetID :len({:d})".format(len(v8)))
					print(v8)
					writer.writerow([ts,v8[0],'v8',v8[2:]])
				
				
uartGetTLVdata("pct")






