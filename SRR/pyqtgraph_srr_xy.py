 # -*- coding: utf-8 -*-
"""
****************************************
version: v1.0 2019/10/29 release
Short Range Radar API
****************************************
Use: pyqtgraph to plot

Hardware requirements:
 Batman Kit- 101 SRR mmWave Sensor SDK
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

************************************************
raspberry pi 4 UART setting issues reference:
https://www.raspberrypi.org/documentation/configuration/uart.md

************************************************

"""
#https://github.com/pyqtgraph/pyqtgraph/tree/develop/examples
#https://github.com/pyqtgraph/pyqtgraph/blob/develop/examples/scrollingPlots.py
#import initExample ## Add path to library (just for examples; you do not need this)

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui

import numpy as np
import serial
#import Jetson.GPIO as GPIO
from mmWave import srradar
import time
import struct
import sys

from threading import Thread
import datetime
from scipy.fftpack import fft
import numpy as np
from scipy import signal

#from PyQt5.QtCore import Qt

class globalV:
	count = 0
	lostCount = 0
	startFrame = 0
	inCount = 0
	frame = 0
	rangeValue = 0.0
	ratioValue = 0.0
	diffValue  = 0.0
	subFrameN = 0
	def __init__(self, count):
		self.count = count		
			
gv = globalV(0)
#pg win
win = pg.GraphicsWindow()
win.resize(1200,1200)
#pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'y')
 
win.setWindowTitle('Short Range Radar')

maxlen = 200
v4 =[]

# 1) for detected object scatterPlot
#win.nextRow()
w0 = win.addPlot()
w0.setRange(xRange=[-10,10],yRange= [0,20])
w0.setLabel('bottom', 'V1 Object Location', '(x,y)')
w0.setLabel('left', 'Distance', 'm')
spots0 = []
curveS0 = pg.ScatterPlotItem(size =20, pen=pg.mkPen('w'), pxMode=True) #pg.ScatterPlotItem(pxMode=True)   ## Set pxMode=False to allow spots to transform with the view
w0.addItem(curveS0)

# 2) for detected object Doppler scatterPlot
w1 = win.addPlot()
w1.setRange(xRange=[0,40],yRange= [-40,40]) 
w1.setLabel('bottom', 'V1 Doppler/Range', '')
w1.setLabel('left', 'V1 Doppler', '')
spots1 = []
curveS1 = pg.ScatterPlotItem(size=20, pen=pg.mkPen('g'), pxMode=True)
w1.addItem(curveS1) 

# 3)plot parking Bins window setting 
win.nextRow()
p2 = win.addPlot(colspan=2)
p2.setRange(xRange=[-20,20],yRange= [0,20]) 
p2.setLabel('bottom', 'Object Distance', 'point')
curve5 = p2.plot()
curve6 = p2.plot()

xa = []
ya = [] 
sx = []
sy = []

# 
# plot data update 
#
def updatePlot():
	global v1len,v2len,v3len,spots0,spots1,sx,sy,xa,ya
	if gv.subFrameN == 1:
		curve5.setData(x=xa,y=ya ,pen= 'g')
		curve6.setData(x=sx,y=sy, pen=None, symbol='o')
		
		
	if v1len !=0:
		if gv.subFrameN == 1:
			curveS0.setData(spots0)
			curveS1.setData(spots1)

# update all plots
def update():
	updatePlot()
	 
#
#----------timer Update--------------------   
timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(143) #150  80: got(20 Times)   *50ms from uart: 
#------------------------------------------

#use USB-UART
#port = serial.Serial("/dev/ttyUSB0",baudrate = 921600, timeout = 0.5)
#
#for Jetson nano UART port
#port = serial.Serial("/dev/ttyTHS1",baudrate = 921600, timeout = 0.5)

#for pi 4 UART port
#port = serial.Serial("/dev/ttyS0",baudrate = 921600, timeout = 0.5)

#Mac OS
port = serial.Serial("/dev/tty.usbmodemGY0050514",baudrate = 921600, timeout = 0.5)

#Short Range Radar initial 
srr = srradar.SRR(port)

v1len = 0
v2len = 0
v3len = 0
v4len = 0
rangeXY = 100.0
keepMin = 100.0   
clearCnt = 0
 
def srrExec():
	global spots0,spots1,spots2,spots3,v1len,v2len,v3len,v4len,v4,xa,ya,sx,sy,keepMin,clearCnt
	
	#pt = datetime.datetime.now()
	#print(pt)
	
	(dck , v1,v2,v3,v4) = srr.tlvRead(False)
	v1len = len(v1)
	
	hdr = srr.getHeader()
	gv.subFrameN = hdr.subFrameNumber
	
	if dck == 1:
		
		v2len = len(v2)
		v3len = len(v3)
		v4len = len(v4)
		pt = datetime.datetime.now()
		print("SubFrame:{:d} [v1,v2,v3,v4]:[{:d},{:d},{:d},{:d}]".format(hdr.subFrameNumber,v1len,v2len,v3len,v4len))
		if v1len != 0:
			#spots = [{'pos': pos[:,i], 'data': 1, 'brush':pg.intColor(i, n), 'symbol': i%5, 'size': 50} for i in range(n)]
			#v1:[(tlvNDOCnt,jb_x,jb_y,jb_doppler_v1,jb_range_v1,jb_peakValue))...]
			#        0        1    2      3             4           5
			spots0  = [{'pos': [v1[i][1],v1[i][2]], 'data': 1, 'brush':pg.intColor(i, v1len), 'symbol': 'o', 'size': 10 } for i in range(v1len)]
			spots1  = [{'pos': [v1[i][4],v1[i][3]], 'data': 1, 'brush':pg.intColor(i, v1len), 'symbol': 'o', 'size': 10 } for i in range(v1len)]
			
			sx = [] 
			sy = []
			for i in range(v1len):
				sx.append(v1[i][1])
				sy.append(v1[i][2])
				rangeXY = np.sqrt(v1[i][1] * v1[i][1] + v1[i][2] * v1[i][2])
				keepMin = np.min([keepMin,rangeXY])
				print("Range:{:f}".format(keepMin))
			
			if clearCnt % 100 == 0:
				keepMin = 100.0
			
		#if v2len != 0:
			#v2:[(tlvNDOCnt,float(jb_xc),float(jb_yc),float(jb_xcSize),float(jb_ycSize))...]
            #        0           1            2               3              4
			#spots2  = [{'pos': [v2[i][1],v2[i][2]], 'data': 1, 'brush':pg.intColor(i, v2len), 'symbol': 's', 'size':np.sqrt(v2[i][3]*v2[i][3] + v2[i][4]*v2[i][4]) * 10 } for i in range(v2len)]
		
		#if v3len !=0:
			#print(v3)
			#v3:[(tlvNDOCnt,jb_xt,jb_yt,jb_xtSize,jb_ytSize,jb_vxt,jb_vyt,jb_tRange,jb_tDoppler)...]
			#     0        1     2       3        4        5      6       7          8
			#spots3  = [{'pos': [v3[i][1],v3[i][2]], 'data': 1, 'brush':pg.intColor(i, v3len), 'symbol': 's', 'size': np.sqrt(v3[i][3]*v3[i][3] + v3[i][4]*v3[i][4]) * 10 } for i in range(v3len)]
		
		if v4len != 0:	# parkingBins
			v4 = np.fft.fftshift(v4)
			v4 = np.append(v4,v4[0])
			#print(v4)
			x1 = np.linspace(-1,1,v4len+2)
			y1 = np.sqrt(1 - x1 * x1)
			
			x_1 = v4 * x1[0:-1]
			x_2 = v4 * x1[1:]
			y_1 = v4 * y1[0:-1]
			y_2 = v4 * y1[1:]
			xa = []
			ya = []
			for i in range(len(x_1)):
				xa.append(x_1[i])
				xa.append(x_2[i])
				ya.append(y_1[i])
				ya.append(y_2[i])
			xa = xa[1:-1]
			ya = ya[1:-1]
			
		
	port.flushInput()
		
		 
def uartThread(name):
	pt = datetime.datetime.now()
	ct = datetime.datetime.now()
	port.flushInput()
	while True:
		srrExec()
					
thread1 = Thread(target = uartThread, args =("UART",))
thread1.setDaemon(True)
thread1.start()

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
	import sys
	if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
		QtGui.QApplication.instance().exec_()
