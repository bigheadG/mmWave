''' 
People Movement Behavior : 2019/2/21 15:47
ex0:
Display Object TLV data

(1)Download lib:

install:
~#sudo pip intall mmWave
update:
~#sudo pip install mmWave -U
'''
import serial
import struct
import datetime

import numpy as np
from mmWave import peopleMB

class globalV:
	count = 0
	def __init__(self, count):
		self.count = count


#UART initial
try:    #pi 3
	port = serial.Serial("/dev/ttyS0",baudrate = 921600, timeout = 0.5)
except: #pi 2
	port = serial.Serial("/dev/ttyAMA0",baudrate = 921600, timeout = 0.5)
#
#initial global value
#
gv = globalV(0)
pm = peopleMB.PeopleMB(port)

def v6Unpack(v6Data):
	print("---v6 unpack---")

def v7UnpackXY(v7Data):
	print("---v7 unpack---")
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
	print("mmWave:People Movement Behavior {:} example:".format(name))
	pt = datetime.datetime.now()
	ct = datetime.datetime.now()
	port.flushInput()
	pm.useDebug(True)
	#pm.stateMachine(True)
	while True:
		#mmWave/PMB tlvRead
		ct = datetime.datetime.now()
		(dck,v6,v7,v8) = pm.tlvRead(False)
		#pm.headerShow()
		hdr = pm.getHeader()
		if dck:
			print("ID#({:d}) TLVs:{:d} [v6({:d}),v7({:d}),v8({:d})] {}\n".format(hdr.frameNumber,hdr.numTLVs,len(v6),len(v7),len(v8),ct-pt))
			pt = ct
			xy = v7UnpackXY(v7)
			print("Position[x,y]:",xy)
			vxy = v7UnpackVelocityXY(v7)
			print("Velocity[X,Y]:",vxy)
			
uartGetTLVdata("PMB")






