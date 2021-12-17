''' 
PC3_ex1: People Counting 3d-People Occupancy (ISK) for BM-201" : 2020/07/15
ex1:
Hardware: Batman-201 ISK

V6: Point Cloud Spherical
	v6 structure: [(range,azimuth,elevation,doppler),......]
	
V7: Target Object List
	V7 structure: [(tid,posX,posY,velX,velY,accX,accY,posZ,velZ,accZ),....]
	
V8: Target Index
	V8 structure: [id1,id2....]
	
V9:Point Cloud Side Info
	v9 structure: [(snr,noise'),....]

(1)Download lib:
install:
~#sudo pip intall mmWave
update:
~#sudo pip install mmWave -U
'''

import serial
import numpy as np
#from mmWave import pc3
import pc3
import serial
from sklearn.cluster import DBSCAN
import pandas as pd
#UART initial

#############################       UART     ##################################
#
#use USB-UART
#port = serial.Serial("/dev/ttyUSB0",baudrate = 921600, timeout = 0.5)
#
#for Jetson nano UART port
#port = serial.Serial("/dev/ttyTHS1",baudrate = 921600, timeout = 0.5) 
#
#for pi 4 UART port
#port = serial.Serial("/dev/ttyS0",baudrate = 921600, timeout = 0.5)
#
#Drone Object Detect Radar initial 
#port = serial.Serial("/dev/tty.usbmodemGY0052854",baudrate = 921600, timeout = 0.5)
port = serial.Serial("/dev/tty.usbmodemGY0043914",baudrate = 921600, timeout = 0.5)
#for NUC ubuntu 
#port = serial.Serial("/dev/ttyACM1",baudrate = 921600, timeout = 0.5)
#
############################################################################


radar = pc3.Pc3(port)

def radarExec(name):
	global v6len,v7len,v8len,pos1,gcolorA,zOffSet,sensorA,mapA,mapSum
	print("mmWave: {:} example:".format(name))
	port.flushInput()
	while(True):
		flag = True
		(dck,v6,v7,v8) = radar.tlvRead(False,df = 'DataFrame')  #radar.tlvRead(False)
		
		#(0) show v6, v7 data as dataframe type
		
		if len(v6) != 0:
			print("-------------- v6 ---------------")
			print(v6)
		if len(v7) != 0:
			print("-------------- v7 ---------------")
			print(v7)
		
		#(1) show sensor information
		#hdr = radar.getHeader()
		#radar.headerShow() # check sensor information
		
		v6op = v6
		if len(v6op) !=0: 
			d = v6op.loc[:,['sx','sy','sz']]
			dd = v6op.loc[:,['sx','sy','sz','doppler']]
			print(dd)
		
		port.flushInput()

radarExec("PC3 DataFrame Example")





