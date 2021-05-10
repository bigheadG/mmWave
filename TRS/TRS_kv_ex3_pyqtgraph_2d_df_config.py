'''
****************************************
version: v1.0 2021/04/17 release
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

from mmWave import roadwayTMD_kv

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
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler

import tkinter as tk
import csv

########################## GUI Method ##################################
def sendConfigData():
	strB = "jb_zoneCfg 1.0 -0.5 3.0 10.0 70.0 -150.0 -0.01"
	tail : bytes = b'\x0d\x0a'
	d = str.encode(strB) + tail
	portCFG.write(d)
	resultString.set(outString)

def callbackFunc():
	#resultString.set("{} - {}".format(landString.get(),cityString.get()))
	outString = "jb_zoneCfg 1.0 {} {} {} {} {} {}".format(
								minXString.get(),maxXString.get(),
								minYString.get(),maxYString.get(),
								minSString.get(),maxSString.get())
	tail : bytes = b'\x0d\x0a'
	d = str.encode(outString) + tail
	portCFG.write(d)
	print(outString)
	resultString.set(outString)
	
rec_Flag = False
def callbackFunc_record():
	global rec_Flag
	if recordButton['fg'] == 'black': # record
		recordButton['fg'] = 'red'
		print("Record Start")
		rec_Flag = True
	else:
		recordButton['fg'] = 'black'
		print("Record Stop")
		rec_Flag = False 

########################## GUI Window ##################################
window = tk.Tk()

# Title setting
window.title('Roadway Traffic Monitoring Detection App')
#window.geometry('700x300')
window.columnconfigure(0, pad=10)
window.columnconfigure(1, pad=10)
window.columnconfigure(2, pad=10)
window.columnconfigure(3, pad=10)

#window.configure(background='gray')
#Row 0
labelMinX = tk.Label(window, text = "min X(m)")
labelMaxX = tk.Label(window, text = "max X(m)")
#labelMinX.grid(column=0, row=0, sticky=tk.W)
#labelMaxX.grid(column=2, row=0, sticky=tk.W)
labelMinX.grid(column=0, row=0)
labelMaxX.grid(column=2, row=0)

minXString = tk.StringVar()
entryMinX = tk.Entry(window, width=10, textvariable=minXString)
entryMinX.grid(column=1, row=0, padx=10)
minXString.set(-0.3)

maxXString = tk.StringVar()
entryMaxX = tk.Entry(window, width=10, textvariable=maxXString)
entryMaxX.grid(column=3, row=0, padx=10)
maxXString.set(3.0)

#Row 1
labelMinY = tk.Label(window, text = "min Y(m)")
labelMaxY = tk.Label(window, text = "max Y(m)")
labelMinY.grid(column=0, row=1)
labelMaxY.grid(column=2, row=1)

minYString = tk.StringVar()
entryMinY = tk.Entry(window, width=10, textvariable=minYString)
entryMinY.grid(column=1, row=1, padx=10)
minYString.set(3.0)

maxYString = tk.StringVar()
entryMaxY = tk.Entry(window, width=10, textvariable=maxYString)
entryMaxY.grid(column=3, row=1, padx=10)
maxYString.set(70.0)

#Row 2
labelMinS = tk.Label(window, text = "min Speed(Km/hr)")
labelMaxS = tk.Label(window, text = "max Speed(km/hr)")
labelMinS.grid(column=0, row=2)
labelMaxS.grid(column=2, row=2)

minSString = tk.StringVar()
entryMinS = tk.Entry(window, width=10, textvariable=minSString)
entryMinS.grid(column=1, row=2, padx=10)
minSString.set(-150.0)

maxSString = tk.StringVar()
entryMaxS = tk.Entry(window, width=10, textvariable=maxSString)
entryMaxS.grid(column=3, row=2, padx=10)
maxSString.set(-0.15)

#Row 3
resultString=tk.StringVar()
resultLabel = tk.Label(window, textvariable=resultString)
resultLabel.grid(column=0, columnspan=3, row=3, padx=10)

#Row 4
resultButton = tk.Button(window, text = 'Send Config Data', command=callbackFunc)
resultButton.grid(column=1, row=4, pady=10)

recordButton = tk.Button(window, text = 'Record', command=callbackFunc_record)
recordButton.grid(column=3, row=4, pady=10)

#Row 5
objString=tk.StringVar()
objLabel = tk.Label(window, textvariable=objString)
objLabel.config(font=("Courier", 44))
objLabel.grid(column=0, columnspan=3, row=5, padx=10, sticky=tk.W )

#Row 6
dataString=tk.StringVar()
dataLabel = tk.Label(window,textvariable=dataString)
dataLabel.config(font=("Courier", 30))
dataLabel.grid(column=0, columnspan=3, row=6, padx=10, sticky=tk.W)


################################################

			
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
w2.setLabel('bottom', 'V7 Object', '')
w2.setLabel('left', 'V7(Target)', '')
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


#----------timer Update--------------------   
timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(143) #150  80: got(20 Times)   *50ms from uart: 
#------------------------------------------

#Output:v21:['flow','fn','indexMax','index','x','y','range','doppler','area','ptsNum','cid']")
# ytA: [NotObject,MAN,MotorCycle,car,CAR]
ytA = {'NotObject':[1,0,0,0,0],'MAN':[0,1,0,0,0] ,'MotorCycle':[0,0,1,0,0] ,'car':[0,0,0,1,0],'CAR':[0,0,0,0,1]}

#fieldsA = ['fn','x','y','range','doppler','area','ptsNum','NotObject','MAN','MotorCycle','car','CAR']
fieldsA = ['fn','indexMax','index','x','y','range','doppler','area','ptsNum','NotObject','MAN','MotorCycle','car','CAR']
################### Real Time or read from file switch ************
#rtSwitch = True # real time mode
rtSwitch = True  # read data from file


dataBaudRate = 921600 if rtSwitch == True else 115200
configBaudRate = 115200

##############################################

#use USB-UART
#port = serial.Serial("/dev/ttyUSB0",baudrate = 921600, timeout = 0.5)
#
#for Jetson nano UART port
#port = serial.Serial("/dev/ttyTHS1",baudrate = 921600, timeout = 0.5) 
'''
if rtSwitch == True:
	#(real time)
	port = serial.Serial("/dev/tty.usbmodemGY0052534",baudrate = 921600 , timeout = 0.5) 
else:
	#(playback)
	port = serial.Serial("/dev/tty.usbmodem14103",baudrate = 115200 , timeout = 0.5)  
'''
#port = serial.Serial("/dev/ttyACM1",baudrate = 115200 , timeout = 0.5) # set 115200 for Algorithm develelop 
#port = serial.Serial("/dev/ttyACM3",baudrate = 921600 , timeout = 0.5) # set 921600 for REAL case


port = serial.Serial("/dev/tty.usbmodemGY0052534",baudrate = dataBaudRate , timeout = 0.5)   # Data port
portCFG = serial.Serial("/dev/tty.usbmodemGY0052531",baudrate = configBaudRate , timeout = 0.5) # config port


#for pi 4 UART port
#port = serial.Serial("/dev/ttyS0",baudrate = 921600, timeout = 0.5)

trs = roadwayTMD_kv.roadwayTmdISK_kv(port)

v21len = 0

tt = datetime.now()
dt = tt.strftime("%Y-%m-%d-%H-%M-%S")  # 格式化日期
fileName = "tmd{:}.csv".format(dt)



if rtSwitch == False:
	(v6smu,v7smu,v8smu,v9smu) = tmd.readFile("tmd2021-04-05-10-27-43.csv")
	print("------------------ v6smu --------start:{:}  stop:{:}--------------".format(tmd.sim_startFN,tmd.sim_stopFN))


fn = 0
prev_fn = 0
flag = True


def getFileName():
	tt = datetime.now()
	dt = tt.strftime("%Y-%m-%d-%H-%M-%S") 
	return  "Roadwaytmd_{:}.csv".format(dt)


def trsExec(writer):
	global spots0,spots1,spots2,v21len,prev_fn,fn,objBuf,flag
	
	(dck,v21) = trs.trsRead(False)
	
	hdr = trs.getHeader()
	fn = hdr.frameNumber
	
	#if rtSwitch == False:
	#	(dck,v6,v7,v8,v9) = trs.getRecordData(fn)
	
	print(v21)
	
	v21len = len(v21)
	if v21len != 0:
		fn = v21.fn[0]
		
	if  fn != prev_fn:
		print("-----------{:}--------input Data Length:{:}".format(fn,len(v21)))
		prev_fn = fn
		if v21len != 0 and flag == True and v21.indexMax[0] >= 1:
			flag = False
			 
			#(1.0) Extract data for plot
			xy21A = v21.loc[:,['x','y']] 
			drA   = v21.loc[:,['doppler','range']]
			#opA   = v21.loc[:,['fn','x','y','range','doppler','area','ptsNum']]
			opA   = v21.loc[:,['fn','indexMax','index','x','y','range','doppler','area','ptsNum']]
			fxyA  = v21.loc[:,['fn','x','y','cid','doppler','ptsNum']]
			
			#(1.1) Plot Object
			rdn = drA.to_numpy()
			spots1  = [{'pos': [rdn[i][0],rdn[i][1]], 'data': 1, 'brush':'r', 'symbol': 'o', 'size': 10 } for i in range(len(rdn))]
				
			v7n = xy21A.to_numpy()
			spots0  = [{'pos': [v7n[i][0],v7n[i][1]], 'data': 1, 'brush':'r', 'symbol': 'o', 'size': 10 } for i in range(len(v7n))]
			
			#(1.2) Show Text
			objA = []
			opAn = opA.to_numpy()
			for i in range(len(opAn)):
				fn = 		opAn[i][0]
				indexMax =	opAn[i][1]
				idx = 		opAn[i][2]
				x =  		opAn[i][3]
				y =  		opAn[i][4]
				ran = 		opAn[i][5]
				dop = 		opAn[i][6]
				area = 		opAn[i][7]
				ptsNum = 	opAn[i][8]
				
				#distance,doppler,area,nop)
				(obj,rng,speed)  = objectReport(ran,dop,area,ptsNum) 
				if obj == 'TRUCK' or obj == 'CAR' or obj == 'MotorCycle':
					print('############################## {:} #######################################'.format(fn))
					print('# WARNING: VEHICLE FROM LEFT SIDE, obj={:10s}, r={:3.0f} m, v={:5.0f} Km/Hr'.format(obj, rng, speed))
					print('##########################################################################')
					
					#wString = '# WARNING:{:10s}, r={:3.0f} m, v={:5.0f} Km/Hr'.format(obj, rng, speed)
					objString.set('# {:10s}'.format(obj))
					dataString.set('r={:3.0f}m,v={:5.0f}Km/Hr'.format(rng, speed))
					
					if rec_Flag == True:
						#csvData = [fn,x,y,distance,dop,area,ptsNum] + ytA[obj] 
						csvData =  [fn,indexMax,idx,x,y,ran,dop,area,ptsNum]  + ytA[obj] 
						writer.writerow(csvData)
						print(csvData)
					
			#(1.3)Target trace(push)
			objBuf = objBuf.append(fxyA, ignore_index=True)
			locBuf.insert(0,fn)
			
			#(1.4) remove data from objBuf(pop)
			if len(objBuf) > QUEUE_LEN:
				objBuf = objBuf.loc[objBuf.fn != locBuf.pop()]
			xBuf = objBuf.loc[:,['x','y']]
			v21t = xBuf.to_numpy()
			spots2  = [{'pos': [v21t[i][0],v21t[i][1]], 'data': 1, 'brush':'r', 'symbol': 'o', 'size': 10 } for i in range(len(v21t))]
			
			flag = True
		
		#clear or pop data when no object data input
		if v21.indexMax[0] == 0:
			spots1 = []
			spots0 = []
			if len(locBuf) > 0:
				print("len:({:})".format(len(locBuf)))
				objBuf = objBuf.loc[objBuf.fn != locBuf.pop()]
				xBuf = objBuf.loc[:,['x','y']]
				v21t = xBuf.to_numpy()
				spots2  = [{'pos': [v21t[i][0],v21t[i][1]], 'data': 1, 'brush':'r', 'symbol': 'o', 'size': 10 } for i in range(len(v21t))]
			else:
				spots2 = []
			
			objString.set('# None')
			dataString.set('r=     m,v=    Km/Hr')
			
	port.flushInput()


def uartThread(name):
	port.flushInput()
	with open(getFileName(), 'w', newline='') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(fieldsA)
		while True:
			trsExec(writer)
			csvfile.flush()


thread1 = Thread(target = uartThread, args =("UART",))
thread1.setDaemon(True)
thread1.start()

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
	import sys
	window.mainloop()
	if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
		QtGui.QApplication.instance().exec_()
		
