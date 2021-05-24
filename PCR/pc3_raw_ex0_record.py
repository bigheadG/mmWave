#=============================================
# File Name: pc3_raw_ex0_record.py
#
# Requirement:
# Hardware: BM501-AOP
# Firmware: pc3
# lib: pc3
# show V6,V7,V8
# type: raw
# Application: output RAW data
#
#=============================================
import serial
import struct
import datetime

import numpy as np
from mmWave import pc3
#import pc3 as pc3

from datetime import date,datetime,time
import csv
import pandas as pd

class globalV:
	count = 0
	def __init__(self, count):
		self.count = count

#pi 3 or pi 4
#port = serial.Serial("/dev/ttyS0",baudrate = 921600, timeout = 0.5)
#for Jetson nano UART port
#port = serial.Serial("/dev/ttyTHS1",baudrate = 921600, timeout = 0.5)
#port = serial.Serial("/dev/tty.usbmodemGY0052534",baudrate = 921600 , timeout = 0.5)
   
#port = serial.Serial("/dev/ttyACM1",baudrate = 921600 , timeout = 0.5)
port = serial.Serial("/dev/tty.SLAB_USBtoUART3",baudrate = 921600 , timeout = 0.5)

#
#initial global value
#
gv = globalV(0)
radar = pc3.Pc3(port)
pcNum = 0


record_time_mins = 10 * 60


tt = datetime.now()
dt = tt.strftime("%Y-%m-%d-%H-%M-%S")  # 格式化日期
fileName = "pc3az{:}.csv".format(dt)


# UART : 50 ms
def uartGetTLVdata(name):
	global pcNum
	port.flushInput()
	#Display 
	#pm.useDebug(True)
	#pm.stateMachine(True)
	with open(fileName, 'w', newline='') as csvfile:
		fieldNames = ['time','frameNum','type','elv/px','azimuth/py','doppler/pz','range/vx','snr/vy','sx/vz','sy/ax','sz/ay','na/az','na/ID']
		writer = csv.writer(csvfile)
		writer.writerow(fieldNames)
		
		while True:
			(dck,v6,v7,v8) = radar.tlvRead(False)
			pcNum = len(v6)
			
			#Show header information
			#pm.headerShow()
			hdr = radar.getHeader()
			 
			if dck:
				print("----v6:--------------")
				print(v6)
				ts = datetime.now() #-st
				if len(v6) != 0:
					posTemp = v6
					#[(elv,azimuth,doppler,range,snr).....(...)]
					for i in range(len(posTemp)):
						sz  = posTemp[i][3] * np.sin(posTemp[i][0])
						sx  = posTemp[i][3] * np.cos(posTemp[i][0]) * np.sin(posTemp[i][1])
						sy  = posTemp[i][3] * np.cos(posTemp[i][0]) * np.cos(posTemp[i][1])
						elvation = posTemp[i][0]
						azimuth  = posTemp[i][1]
						doppler  = posTemp[i][2]
						r        = posTemp[i][3]
						snr      = posTemp[i][4]
						
						writer.writerow([ts,hdr.frameNumber,'v6',elvation,azimuth,doppler,r,snr,sx,sy,sz])
						
					print("V6: Point Cloud Spherical v6:len({:d})-----------------".format(len(v6)))
				
				
				print("ID#({:d}) TLVs:{:d} [v6({:d}),v7({:d}),v8({:d})]\n".format(hdr.frameNumber,hdr.numTLVs,len(v6),len(v7),len(v8)))
				print("----X,Y Position:-------")
				
				if len(v7) != 0:
					v7t = v7
					print("----v7 data:-------")
					for i in range(len(v7t)):
						writer.writerow([ts,hdr.frameNumber,'v7',v7t[i][1],v7t[i][2],v7t[i][7],v7t[i][3],v7t[i][4],v7t[i][8],v7t[i][5],v7t[i][6],v7t[i][9],v7t[i][0]])
				
				
				if len(v8) != 0:
					v8t = v8
					writer.writerow([ts,hdr.frameNumber,'v8',v8])
				
				
				
uartGetTLVdata("pc3")






