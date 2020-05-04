 # -*- coding: utf-8 -*-
"""
****************************************
version: v1.0 2020/04/30 release
Traffice Monitor Dector Radar API
****************************************
Use: pyqtgraph to plot

Hardware requirements:
 Batman Kit- 201 TMD mmWave Sensor SDK
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
from mmWave import trafficMD

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

win = pg.GraphicsWindow()
win.resize(1200,800)

pg.setConfigOption('foreground', 'y')
win.setWindowTitle('Traffic Monitor Detect Radar')

#**************************************
detRange = 50
maxlen = 128
#**************************************

# 2) for detected object(point cloud) Doppler scatterPlot
w1 = win.addPlot()
w1.setRange(xRange=[0,detRange],yRange= [-5,5]) 
w1.setLabel('bottom', 'V6.Doppler', 'meter')
w1.setLabel('left', 'V6.Doppler', '')
spots1 = []
curveS1 = pg.ScatterPlotItem(size=20, pen=pg.mkPen('g'), pxMode=True)
w1.addItem(curveS1) 

# 1) for detected point cloud location scatterPlot
#win.nextRow()
w0 = win.addPlot()
w0.setRange(xRange=[-5,50],yRange= [-30,30])
w0.setLabel('bottom', 'V6 Point Cloud Location', 'meter')
w0.setLabel('left', 'V6', 'm')
spots0 = []
curveS0 = pg.ScatterPlotItem(size =20, pen=pg.mkPen('w'), pxMode=True) #pg.ScatterPlotItem(pxMode=True)   ## Set pxMode=False to allow spots to transform with the view
w0.addItem(curveS0)

#********** next window ********
win.nextRow()
# 2) for detected object(point cloud) Doppler scatterPlot
w2 = win.addPlot()
w2.setRange(xRange=[0,detRange],yRange= [-5,5]) 
w2.setLabel('bottom', 'V7.Doppler', 'meter')
w2.setLabel('left', 'V7.Doppler', '')
spots2 = []
curveS2 = pg.ScatterPlotItem(size=20, pen=pg.mkPen('g'), pxMode=True)
w2.addItem(curveS2) 

# 1) for detected point cloud location scatterPlot
#win.nextRow()
w3 = win.addPlot()
w3.setRange(xRange=[-5,50],yRange= [-30,30])
w3.setLabel('bottom', 'V7 Object Location', 'meter')
w3.setLabel('left', 'V7', 'm')
spots3 = []
curveS3 = pg.ScatterPlotItem(size =20, pen=pg.mkPen('w'), pxMode=True) #pg.ScatterPlotItem(pxMode=True)   ## Set pxMode=False to allow spots to transform with the view
w3.addItem(curveS3)



# 
# plot data update 
#
def updatePlot():
	global v6len,v7len,spots0,spots1,spots2,spots3
	if v6len !=0:
		curveS0.setData(spots0)
		curveS1.setData(spots1)
	if v7len != 0:
		curveS2.setData(spots2)
		curveS3.setData(spots3)
		
# update all plots
def update():
	updatePlot()
	 
#
#----------timer Update--------------------   
timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
# based on your computing power you can change this parameter
timer.start(150) #150  80: got(20 Times)  #mmWave Sensor:50ms from uart: 
#------------------------------------------

#use USB-UART
#port = serial.Serial("/dev/ttyUSB0",baudrate = 921600, timeout = 0.5)
#
#for Jetson nano UART port
#port = serial.Serial("/dev/ttyTHS1",baudrate = 921600, timeout = 0.5) 
port = serial.Serial("/dev/tty.usbmodemGY0052854",baudrate = 921600, timeout = 0.5)
#for pi 4 UART port
#port = serial.Serial("/dev/ttyS0",baudrate = 921600, timeout = 0.5)

#Traffice Monitor Radar initial 
tmd = trafficMD.TrafficMD(port)

v6len = 0
v7len = 0
v8len = 0
v9len = 0

tmd.sm = False 
 

def tmdExec():
	global spots0,spots1,spots2,spots3,v6len,v7len,v8len,v9len
	
	(dck,v6,v7,v8,v9) = tmd.tlvRead(False)
	
	if dck == 1:
		v6len = len(v6)
		v7len = len(v7)
		v8len = len(v8)
		v9len = len(v9)
		
		print("Sensor Data: [v6,v7,v8,v9]:[{:d},{:d},{:d},{:d}]".format(v6len,v7len,v8len,v9len))
		if v6len != 0:
			#v6[(range,azmuth,elevate,velociy)...]
			
			spots1  = [{'pos': [v6[i][0],v6[i][3]], 'data': 1, 'brush':pg.intColor(i, v6len), 'symbol': 'o', 'size': 10 } for i in range(v6len)]
			spots0  = [{'pos': [ v6[i][0]*np.cos(v6[i][1]),v6[i][0]*np.sin(v6[i][1])], 'data': 1, 'brush':pg.intColor(i, v6len), 'symbol': 'o', 'size': 10 } for i in range(v6len)]
			spots2  = [{'pos': [ np.sqrt(v7[i][0]*v7[i][0] + v7[i][1] *  v7[i][1] ), v7[i][8]], 'data': 1, 'brush':pg.intColor(i, v7len), 'symbol': 'o', 'size': 10 } for i in range(v7len)]
			spots3  = [{'pos': [ v7[i][1], v7[i][0]], 'data': 1, 'brush':pg.intColor(i, v7len), 'symbol': 'o', 'size': 10 } for i in range(v7len)]
			
		 
	port.flushInput()
		
		 
def uartThread(name):
	port.flushInput()
	while True:
		tmdExec()
					
thread1 = Thread(target = uartThread, args =("UART",))
thread1.setDaemon(True)
thread1.start()

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
	import sys
	if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
		QtGui.QApplication.instance().exec_()
