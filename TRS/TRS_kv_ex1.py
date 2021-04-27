''' 
Traffic Monitoring Detection Roadway Sensing (ISK) for BM-201" : 2021/04/17
ex1:
Hardware: BM201-TRS kit


(1)Download lib:
install:
~#sudo pip3 intall mmWave
update:
~#sudo pip3 install mmWave -U

install numpy
~#sudo pip3 install numpy

'''

import serial
import numpy as np
from mmWave import roadwayTMD_kv

def objectReport(distance,doppler,area,nop):
	obj = "CAR"
	speed = -doppler*3600.0/1000.0
	#############################
	# JUDGE OBJECT BY RULE BASED
	#############################
					
	#from last test
	if speed > 82.8: # frameOffset 349..367
		obj = "NotObject"
	elif distance < 40 and distance >= 10 and nop <= 15 and nop >= 1: # and -doppler <= 3.0: #doppler
		obj = "MAN"
	elif distance < 40 and distance >= 10 and nop <= 2: 
		obj = "NotObject"
	elif distance < 60 and distance >= 50 and nop <= 2: 
		obj = "NotObject"
	elif distance < 20 and distance >= 10  and nop <= 3 and area >= 10: 
		obj = "NotObject"
	#elif area > 7.0:
	#	obj = "TRUCK"
	elif distance < 60 and distance >= 50 and nop >= 2: # added for TRUCK
		obj = "CAR"
	elif distance < 50 and distance >= 40 and nop >= 3: # added for TRUCK
		obj = "CAR"
	elif distance < 40 and distance >= 30 and nop >= 10: # added for TRUCK
		obj = "CAR"
	elif distance < 30 and distance >= 20 and nop >= 20: # added for TRUCK
		obj = "CAR"
	elif distance < 20 and distance >= 10 and nop >= 22: # added for TRUCK
		obj = "CAR"
	elif distance < 40 and distance >= 10 and nop >= 2 and area < 4.00 and speed >= 70:
		obj = "NotObject"
	elif distance < 40 and distance >= 30 and nop >= 2 and area < 1.50: 
		obj = "MotorCycle"
	elif distance < 30 and distance >= 20 and nop >= 3 and area < 2.00: 
		obj = "MotorCycle"
	elif distance < 20 and distance >= 10 and nop >= 3 and area < 4.00: 
		obj = "MotorCycle"
	
	return (obj,distance,speed)

#port = serial.Serial("COM189",baudrate = 921600, timeout = 0.5)
port = serial.Serial("/dev/tty.usbmodemGY0052534",baudrate = 921600 , timeout = 0.5) 

tmd = roadwayTMD_kv.roadwayTmdISK_kv(port)

def uartGetdata(name):
	print("mmWave: {:} example:".format(name))
	port.flushInput()
	while True:
		(dck,v21)=tmd.trsRead(False) 
		if dck and len(v21) > 0:
			print(v21)
			if v21.indexMax[0] != 0:
				opA = v21.loc[:,['range','doppler','area','ptsNum']]
				#(1.2) Show Text
				objA = []
				opAn = opA.to_numpy()
				
				for i in range(len(opAn)):
					(obj,rng,speed)  = objectReport(opAn[i][0],opAn[i][1],opAn[i][2],opAn[i][3]) 
					print("================= result ===========================")
					print("object({:})  speed:{:}  range:{:}".format(obj,rng,speed))
					print("====================================================")
					
						
			
uartGetdata("Traffic Monitoring Detection Roadway Sensing (TRS) for BM-201")
