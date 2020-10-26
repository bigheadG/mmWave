''' 
Vital Signs : 2020/10/20 15:47
ex0:
Display heart rate & breathing rate data

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
#import vitalsign_kv
from mmWave import vitalsign_kv

#UART initial
'''
try:    #pi 3
	port = serial.Serial("/dev/ttyS0",baudrate = 115200, timeout = 0.5)
except: #pi 2
	port = serial.Serial("/dev/ttyAMA0",baudrate = 115200, timeout = 0.5)
'''
#for Mac
#port = serial.Serial("/dev/cu.usbmodemGY0043914",baudrate = 115200, timeout = 0.5)

#for Jetson Nano
#port = serial.Serial("/dev/ttyTHS1",baudrate = 115200, timeout = 0.5)

#for Ubuntu
#port = serial.Serial("/dev/ttyACM1",baudrate = 115200, timeout = 0.5)

#for Windows10
#port = serial.Serial("COM5",baudrate = 115200, timeout = 0.5)

vts = vitalsign_kv.VitalSign_kv(port)

def labelString(idx):
	if idx == 0:
		return "TargetNone"
	elif idx == 1:
		return "TargetStable"
	elif idx == 2:
		return  "TargetMovement"
	elif idx == 3:
		return "TargetAlert"
	else:
		return "TargetNone"


def uartGetTLVdata(name):
	print("mmWave: {:} example:".format(name))
	port.flushInput()
	while True:
		#mmWave/VitalSign tlvRead & Vital Sign 
		(dck , vd) = vts.tlvRead(False)
		if dck:
			#idx =  vd[6] #int(vd[6])
			print("Status:{}  {}".format(vd[6],labelString(vd[6])))
			print("Breath Rate:{:}  Heart Rate:{:} Breath Phase:{:} Heart Phase:{:}".format(vd[2],vd[3],vd[4],vd[5]))

uartGetTLVdata("VitalSign")






