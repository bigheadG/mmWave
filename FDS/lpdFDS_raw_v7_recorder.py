''' 
Falling Detection Sensing  (ISK) for BM-201" : 2021/06/01

Hardware: Batman-201 ISK

V6: Point Cloud Spherical
	v6 structure: #[(fN,type,range,azimuth,elv,doppler,sx,sy,sz),......]
	
V7: Target Object List
	V7 structure: #[( fN,typ,posX,posY  ...ec15,g,confi,tid),....]
	
V8: Target Index
	V8 structure: #[id1,id2....]
	
V9:Point Cloud Side Info
	v9 structure: #[(snr,noise'),....]

(1)Download lib:
install:
~#sudo pip intall mmWave
update:
~#sudo pip install mmWave -U
'''

import serial
import numpy as np
from mmWave import lpdFDS
import csv
from datetime import date,datetime,time

v6_col_names_rt = ['fN','type','range','azimuth','elv','doppler','sx', 'sy', 'sz']
v7_col_names_rt = ['fN','type','posX','posY','posZ','velX','velY','velZ','accX','accY','accZ','ec0','ec1','ec2','ec3','ec4','ec5','ec6','ec7','ec8','ec9','ec10','ec11','ec12','ec13','ec14','ec15','g','confi','tid']
v8_col_names_rt = ['fN','type','targetID']
v9_col_names_rt = ['fN','type','snr','noise']


def getFileName():
	tt = datetime.now()
	dt = tt.strftime("%Y-%m-%d-%H-%M-%S") 
	return  "lpdFDS_{:}.csv".format(dt)


#UART initial
###################################################################
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
#port = serial.Serial("/dev/tty.usbmodemGY0052534",baudrate = 921600, timeout = 0.5)
#port = serial.Serial("/dev/tty.usbmodem14103",baudrate = 115200 , timeout = 0.5)  
port = serial.Serial("/dev/tty.usbmodemGY0043914",baudrate = 921600, timeout = 0.5) 
#port = serial.Serial("/dev/tty.SLAB_USBtoUART3",baudrate = 921600, timeout = 0.5)   

#for NUC ubuntu 
#port = serial.Serial("/dev/ttyACM1",baudrate = 921600, timeout = 0.5

radar = lpdFDS.LpdFDS(port)

def uartGetdata(name):
	print("mmWave: {:} example:".format(name))
	port.flushInput()
	with open(getFileName(), 'w', newline='') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(v7_col_names_rt)
		
		while True:
			hdr = radar.getHeader()
			(dck,v6,v7,v8,v9)  = radar.tlvRead(False,df = 'DataFrame')
		
			hdr = radar.getHeader()
			fn = hdr.frameNumber
		
			if dck:
				print("V6:V7:V8:V9 = length([{:d},{:d},{:d},{:d}])".format(len(v6),len(v7),len(v8),len(v9)))
				'''
				if len(v6) != 0:
					print("V6: Point Cloud Spherical v6:len({:d})-----------------".format(len(v6)))
					#[(fN,type,range,azimuth,elv,doppler,sx,sy,sz),......]
					print(v6)
				'''
				if len(v7) != 0:
					print("V7: Target Object List----v7:len({:d})-----------------".format(len(v7)))
					#[( fN,typ,posX,posY  ...ec15,g,confi,tid),....]
					opA = v7.loc[:,v7_col_names_rt]
					print("-----v7 count:{:}".format(len(opA)))
					objA = []
					opAn = opA.to_numpy()
					#v7_col_names_rt = ['fN','type','posX','posY','posZ','velX','velY','velZ','accX','accY','accZ','ec0'
					#,'ec1','ec2','ec3','ec4','ec5','ec6','ec7','ec8','ec9','ec10','ec11','ec12','ec13','ec14','ec15','g','confi','tid']
					for i in range(len(opAn)):
						fn   = opAn[i][0]
						ty   = opAn[i][1]
						posX = opAn[i][2]
						posY = opAn[i][3]
						posZ = opAn[i][4]
						velX = opAn[i][5]
						velY = opAn[i][6]
						velZ = opAn[i][7]
						accX = opAn[i][8]
						accY = opAn[i][9]
						accZ = opAn[i][10]
						ec0  = opAn[i][11]
						ec1  = opAn[i][12]
						ec2  = opAn[i][13]
						ec3  = opAn[i][14]
						ec4  = opAn[i][15]
						ec5  = opAn[i][16]
						ec6  = opAn[i][17]
						ec7  = opAn[i][18]
						ec8  = opAn[i][19]
						ec9  = opAn[i][20]
						ec10 = opAn[i][21]
						ec11 = opAn[i][22]
						ec12 = opAn[i][23]
						ec13 = opAn[i][24]
						ec14 = opAn[i][25]
						ec15 = opAn[i][26]
						g    = opAn[i][27]
						confi = opAn[i][28]
						tid   = opAn[i][29]
						writer.writerow([fn,ty,posX,posY,posZ,velX,velY,velZ,accX,accY,accZ,ec0,ec1,ec2,ec3,ec4,ec5,ec6,ec7,ec8,ec9,ec10,ec11,ec12,ec13,ec14,ec15,g,confi,tid])
						csvfile.flush()
						
					
					#print(v7)
				'''
				if len(v8) != 0:
					print("V8: Target Index----------v8:len({:d})-----------------".format(len(v8)))
					#[id1,id2....]
					print(v8)
				if len(v9) != 0:
					print("V9:Point Cloud Side Info--v9:len({:d})-----------------".format(len(v9)))
					#[(snr,noise'),....]
					print(v9)
				'''
uartGetdata("Falling Detect Sensing (FDS) for BM-201")






