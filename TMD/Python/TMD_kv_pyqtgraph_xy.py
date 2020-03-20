 # -*- coding: utf-8 -*-
"""
****************************************
version: v1.0 2020/3/19 release
Traffic Monitor Detect API
****************************************
Use: pyqtgraph to plot

Hardware requirements:
 Batman Kit- 201 TMD mmWave Sensor SDK-ISK
 Jetson nano , pi 4  
 
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

$pip3 install pyqtgraph

$pip3 install pyqt5

$because pyqtgraph not support python 3.8
needs modifed ptime.py

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

#import trafficMD as TrafficMD
from mmWave import trafficMD

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
 
win.setWindowTitle('Traffic Monitor Detect')

maxlen = 200
v4 =[]

# 1) for detected object scatterPlot
#win.nextRow()
w0 = win.addPlot()
w0.setRange(xRange=[-10,10],yRange= [0,20])
w0.setLabel('bottom', 'V1 Object Location', '(x,y)')
w0.setLabel('left', 'Distance', 'm')
spots0 = []
curveS0 = pg.ScatterPlotItem(size = 30, pen=pg.mkPen('w'), pxMode=True) #pg.ScatterPlotItem(pxMode=True)   ## Set pxMode=False to allow spots to transform with the view
w0.addItem(curveS0)

# 2) for detected object Doppler scatterPlot
w1 = win.addPlot()
w1.setRange(xRange=[0,40],yRange= [-40,40]) 
w1.setLabel('bottom', 'V1 Doppler/Range', '')
w1.setLabel('left', 'V1 Doppler', '')
spots1 = []
curveS1 = pg.ScatterPlotItem(size=30, pen=pg.mkPen('g'), pxMode=True)
w1.addItem(curveS1) 

# 3)plot parking Bins window setting 

xa = []
ya = [] 
sx = []
sy = []

# 
# plot data update 
#
def updatePlot():
	global v1len,spots0,spots1
		
	if v1len !=0:
		#if gv.subFrameN == 1:
			curveS0.setData(spots0)
			curveS1.setData(spots1)

# update all plots
def update():
	updatePlot()
	 
#
#----------timer Update--------------------   
timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(50) #150  80: got(20 Times)   *50ms from uart: 
#------------------------------------------

#use USB-UART
#port = serial.Serial("/dev/ttyUSB0",baudrate = 921600, timeout = 0.5)
#
#for Jetson nano UART port
#port = serial.Serial("/dev/ttyTHS1",baudrate = 921600, timeout = 0.5)
#
#for Mac example: please check: $ls /dev/tty* to get uart name
#port = serial.Serial(""/dev/tty.usbmodemGY0052534"",baudrate = 921600, timeout = 0.5)
#
#for windows UART port
#please check windows UART port 
port = serial.Serial("COM189",baudrate = 921600, timeout = 0.5)

pm =trafficMD.tmdISK_kv(port)

v1len = 0
v2len = 0
rangeXY = 100.0
keepMin = 100.0   
clearCnt = 0

def sizeTrans(iten):
	x = iten * 6
	return  10 if x < 10 else x
 
def tmdExec():
	global spots0,spots1,v1len,v4,xa,ya,sx,sy,keepMin,clearCnt
	
	(dck,v0,v1)=pm.tmdRead(False) 
	v1len = len(v1)
	if dck == True:
		print("framre= {:d} target={:d} pointCloud#:{:d}".format(v0.frame,v0.target,v0.pcNum))
		
		if v1len != 0:
			spots1  = [{'pos': [v1[i].vx,v1[i].vy], 'data': 1, 'brush':pg.intColor(i, v1len), 'symbol': 'o', 'size': sizeTrans(v1[i].iten) } for i in range(v1len)]
			spots0  = [{'pos': [v1[i].x,v1[i].y], 'data': 1, 'brush':pg.intColor(i, v1len), 'symbol': 'o', 'size':  sizeTrans(v1[i].iten) } for i in range(v1len)]
		
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
