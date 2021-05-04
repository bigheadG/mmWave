'''
****************************************
version: v1.0 2021/05/04 release
Traffic Monitoring Detection Roadway Sensing 
****************************************
Use: pyqtgraph to plot

Hardware requirements:
 Batman Kit- 201 TRS mmWave Sensor SDK
 Jetson nano or pi 4
 
**************
Install Jetson nano: Please reference

https://makerpro.cc/2019/05/the-installation-and-test-of-nvida-jetson-nano/
it will teach you how to install
 
(1)install Jetson nano GPIO
    $sudo pip3 install Jetson.GPIO
    $sudo groupadd -f -r gpio
    
    #please change pi to your account
    $cd practice sudo usermod -a -G gpio pi
    
    $sudo cp /opt/nvidia/jetson-gpio/etc/99-gpio.rules /etc/udev/rules.d/
    
    reboot system and run
    
    $sudo udevadm control --reload-rules && sudo udevadm trigger
(2)install mmWave lib
$sudo pip3 install mmWave
(3) upgarde mmWave lib
$sudo pip3 install mmWave -U

(4) install pandas
$sudo pip3 install pandas

************************************************
raspberry pi 4 UART setting issues reference:
https://www.raspberrypi.org/documentation/configuration/uart.md

************************************************

Lib: roadwayTMD_kv

'''
#https://github.com/pyqtgraph/pyqtgraph/tree/develop/examples
#https://github.com/pyqtgraph/pyqtgraph/blob/develop/examples/scrollingPlots.py
#import initExample ## Add path to library (just for examples; you do not need this)

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui

import numpy as np
import serial
#import Jetson.GPIO as GPIO

#from mmWave import roadwayTMD_kv
import roadwayTMD_kv as roadwayTMD_kv

import time
import struct
import sys

from threading import Thread
import datetime
from scipy.fftpack import fft
import numpy as np
from scipy import signal

from datetime import date,datetime,time
import pandas as pd


import csv


			
colorSet = [[255,255, 0,255], [0, 255, 0, 255], [0, 100, 255, 255], [248, 89, 253, 255], [89, 253, 242, 255],[89, 253, 253, 255],
		  [253, 89, 226, 255],[253, 229, 204, 255],[51, 255, 255, 255],[229, 204, 255, 255], [89, 253, 100, 255], 
		  [127, 255, 212, 255], [253, 165, 89, 255],[255, 140, 0, 255],[255, 215, 0, 255],[0, 0, 255, 255]]


##################### Parameter ################################### 
QUEUE_LEN = 15
locBuf = []
objBuf = pd.DataFrame([], columns=['fn','x','y'])


win = pg.GraphicsWindow()
win.resize(1200,800)

pg.setConfigOption('foreground', 'y')
 
win.setWindowTitle('Roadway Traffic Monitoring Detection Radar')

#**************************************
brush_list = [pg.mkColor(c) for c in "rgbcmykwrg"]

# 2) for detected object Doppler scatterPlot
w1 = win.addPlot()
w1.setRange(xRange=[-50,50],yRange= [0,100]) 
w1.setLabel('bottom', 'Object Doppler', 'm/s')
w1.setLabel('left', 'Object Range', 'm')
spots1 = []
curveS1 = pg.ScatterPlotItem(size=20, pen=pg.mkPen('g'), pxMode=True)
w1.addItem(curveS1) 

# 1) for detected object scatterPlot
#win.nextRow()
w0 = win.addPlot()
w0.setRange(xRange=[-50,50],yRange= [0,100])
w0.setLabel('bottom', 'Object(x)', 'm')
w0.setLabel('left', 'Object(y)', 'm')
spots0 = []
curveS0 = pg.ScatterPlotItem(size =20, pen=pg.mkPen('w'), pxMode=True) #pg.ScatterPlotItem(pxMode=True)   ## Set pxMode=False to allow spots to transform with the view
w0.addItem(curveS0)

win.nextRow()
# 3) for detected object Doppler scatterPlot
w2 = win.addPlot(colspan=1)
w2.setRange(xRange=[-50,50],yRange= [0,100]) 
w2.setLabel('bottom', 'Object', '')
w2.setLabel('left', '(Target)', '')
spots2 = []
curveS2 = pg.ScatterPlotItem(size=20, pen=pg.mkPen('g'), pxMode=True)
w2.addItem(curveS2) 


def draw_2d_square(x,y,xl,yl):
	rect_item = RectItem(QtCore.QRectF(x,y, xl, yl))
	pg.graphWidget_2D.addItem(rect_item)

# 
# plot data update
#

def update():
	global v21len,spots0,spots1,spots2
		
	if v21len !=0:
		curveS0.setData(spots0)
		curveS1.setData(spots1)
		curveS2.setData(spots2)

def objectRuleBasedReport(distance,doppler,area,nop):
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


#----------timer Update--------------------   
timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(143) #143ms from uart: 
#------------------------------------------


##############################################

#Output:v21:['flow','fn','indexMax','index','x','y','range','doppler','area','ptsNum','cid']")
# ytA: [NotObject,MAN,MotorCycle,car,CAR]
ytA = {'NotObject':[1,0,0,0,0],'MAN':[0,1,0,0,0] ,'MotorCycle':[0,0,1,0,0] ,'car':[0,0,0,1,0],'CAR':[0,0,0,0,1]}

fieldsA = ['fn','indexMax','index','x','y','range','doppler','area','ptsNum','NotObject','MAN','MotorCycle','car','CAR']

toolkitBaudRate = 115200

##############################################

#use USB-UART
#port = serial.Serial("/dev/ttyUSB0",baudrate = 921600, timeout = 0.5)
#
#for Jetson nano UART port
#port = serial.Serial("/dev/ttyTHS1",baudrate = 921600, timeout = 0.5) 
#port = serial.Serial("/dev/ttyACM1",baudrate = 115200 , timeout = 0.5) # set 115200 for Algorithm develelop 
#port = serial.Serial("/dev/ttyACM3",baudrate = 921600 , timeout = 0.5) # set 921600 for REAL case


port = serial.Serial("/dev/tty.usbmodem14103",baudrate = toolkitBaudRate , timeout = 0.5)

#for pi 4 UART port
#port = serial.Serial("/dev/ttyS0",baudrate = 921600, timeout = 0.5)

trs = roadwayTMD_kv.roadwayTmdISK_kv(port)

v21len = 0

tt = datetime.now()
dt = tt.strftime("%Y-%m-%d-%H-%M-%S")  # 格式化日期
fileName = "tmd{:}.csv".format(dt)

v21Read = trs.readFile("RoadwayTMD_2021-05-04-09-50-43.csv")
print("--------------v21Read----------------")
print(v21Read)


fn = 0
prev_fn = 0
flag = True


def trsExec():
	global spots0,spots1,spots2,v21len,prev_fn,fn,objBuf,flag
	
	(dck,_) = trs.trsRead(False) # for generate frameNumber
	fn = trs.frameNumber
	(dck,v21) = trs.getRecordData(fn)
	v21len = len(v21)
	
	if  fn != prev_fn:
		print("frameNum: sim_stopFN:{:}  workFrameNumber(sim_startFN:fn)=({:}+{:}) = {:}".format(trs.sim_stopFN,trs.sim_startFN,fn,fn+trs.sim_startFN ))
		prev_fn = fn
		if v21len != 0 and flag == True  and v21['indexMax'].values[0] >= 1:
			flag = False
			  
			#(1.0) Extract data for plot
			xy21A = v21.loc[:,['x','y']] 
			drA   = v21.loc[:,['doppler','range']]
			opA   = v21.loc[:,['fn','indexMax','index','x','y','range','doppler','area','ptsNum']]
			fxyA  = v21.loc[:,['fn','x','y','doppler','ptsNum']]
			
			#(1.1) prepare Plot Object data
			rdn = drA.to_numpy()
			spots1  = [{'pos': [rdn[i][0],rdn[i][1]], 'data': 1, 'brush':'r', 'symbol': 'o', 'size': 10 } for i in range(len(rdn))]
				
			v21n = xy21A.to_numpy()
			spots0  = [{'pos': [v21n[i][0],v21n[i][1]], 'data': 1, 'brush':'r', 'symbol': 'o', 'size': 10 } for i in range(len(v21n))]
			
			#(1.2) rule base judge
			objA = []
			opAn = opA.to_numpy()
			for i in range(len(opAn)):
				
				fnum = 		opAn[i][0]
				indexMax =	opAn[i][1]
				idx = 		opAn[i][2]
				x =  		opAn[i][3]
				y =  		opAn[i][4]
				ran = 		opAn[i][5]
				dop = 		opAn[i][6]
				area = 		opAn[i][7]
				ptsNum = 	opAn[i][8]
				
				#distance,doppler,area,nop)
				(obj,rng,speed)  = objectRuleBasedReport(ran,dop,area,ptsNum) 
				if obj == 'TRUCK' or obj == 'CAR' or obj == 'MotorCycle':
					print('############################## FrameNum: {:} ##########################'.format(fnum))
					print('# WARNING: VEHICLE FROM LEFT SIDE, obj={:10s}, r={:3.0f} m, v={:5.0f} Km/Hr'.format(obj, rng, speed))
					print('##########################################################################')
					
			#(1.3) prepare target trace data
			#(1.3.1)Target trace(push)
			objBuf = objBuf.append(fxyA, ignore_index=True)
			locBuf.insert(0,fn)
			
			#(1.3.2) remove data from objBuf(pop)
			if len(objBuf) > QUEUE_LEN:
				objBuf = objBuf.loc[objBuf.fn != locBuf.pop()]
			xBuf = objBuf.loc[:,['x','y']]
			v21np = xBuf.to_numpy()
			spots2  = [{'pos': [v21np[i][0],v21np[i][1]], 'data': 1, 'brush':'r', 'symbol': 'o', 'size': 10 } for i in range(len(v21np))]
			
			flag = True
		
		#clear or pop data when no object data input
		if v21len == 1:
			if v21['indexMax'].values[0] == 0:
				spots1 = []
				spots0 = []
				if len(locBuf) > 0:
					print("len:({:})".format(len(locBuf)))
					objBuf = objBuf.loc[objBuf.fn != locBuf.pop()]
					xBuf = objBuf.loc[:,['x','y']]
					v21np = xBuf.to_numpy()
					spots2  = [{'pos': [v21np[i][0],v21np[i][1]], 'data': 1, 'brush':'r', 'symbol': 'o', 'size': 10 } for i in range(len(v21np))]
				else:
					spots2 = []
				
		
	port.flushInput()

def uartThread(name):
	port.flushInput()
	while True:
		trsExec()


thread1 = Thread(target = uartThread, args =("UART",))
thread1.setDaemon(True)
thread1.start()

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
	import sys
	#window.mainloop()
	if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
		QtGui.QApplication.instance().exec_()
		
