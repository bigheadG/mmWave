#=============================================
# File Name: pc3d_v12_ex0.py
#
# Requirement:
# Hardware: BM301-ODS
# Firmware: FDS
# lib: pc3d
# show V6,V7,V8
# type: raw
# Application: output RAW data
#
#=============================================
import serial
import struct
import datetime

import numpy as np
from mmWave import pc3d

class globalV:
	count = 0
	def __init__(self, count):
		self.count = count

#pi 3 or pi 4
#port = serial.Serial("/dev/ttyS0",baudrate = 921600, timeout = 0.5)
#for Jetson nano UART port
port = serial.Serial("/dev/ttyTHS1",baudrate = 921600, timeout = 0.5)

#
#initial global value
#
gv = globalV(0)
pm = pc3d.Pc3d(port)
pcNum = 0
def v6Unpack(v6Data):
	print("---v6 unpack---")

def v7UnpackXY(v7Data):
	#print("---v7 unpack---")
	v7xy = []
	for k in v7Data:
		v7xy.append([k[1], k[2]])
	return v7xy
	
def v7UnpackVelocityXY(v7Data): # velocity x,y
	velxy = []
	for k in v7Data:
		velxy.append([k[3], k[4]])
	return velxy

# UART : 50 ms
def uartGetTLVdata(name):
	global pcNum
	port.flushInput()
	#Display 
	#pm.useDebug(True)
	#pm.stateMachine(True)
	while True:
		(dck,v6,v7,v8) = pm.tlvRead(False)
		pcNum = len(v6)
		
		#Show header information
		#pm.headerShow()
		hdr = pm.getHeader()
		if dck:
			print("ID#({:d}) TLVs:{:d} [v6({:d}),v7({:d}),v8({:d})]\n".format(hdr.frameNumber,hdr.numTLVs,len(v6),len(v7),len(v8)))
			print("----X,Y Position:-------")
			xy = v7UnpackXY(v7)
			print("Position[x,y]:",xy)
			
			print("----Velocity:-------")
			vxy = v7UnpackVelocityXY(v7)
			print("Velocity[X,Y]:",vxy)
				
uartGetTLVdata("pc3d")






