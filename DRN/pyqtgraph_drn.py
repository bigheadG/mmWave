 # -*- coding: utf-8 -*-
"""
****************************************
version: v1.0 2020/05/13 release
Drone Radar Navigtion API
****************************************
Use: pyqtgraph to plot

Hardware requirements:
 Batman Kit- 201 DRN mmWave Sensor SDK
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
from mmWave import droneRN

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
 
win.setWindowTitle('Drone Object Detect Radar')

#**************************************
detRange = 20
maxlen = 128
len512 = 512
#**************************************

tr2 = np.zeros(len512)
tr21 = np.zeros(len512)
tr4 = np.zeros(len512)


# 1) for detected object scatterPlot
#win.nextRow()
w0 = win.addPlot()
w0.setRange(xRange=[0,detRange],yRange=[-10,10])
w0.setLabel('bottom', 'V1 Doppler/Range(meter)', 'Meter')
w0.setLabel('left', 'Doppler', '')
spots0 = []
curveS0 = pg.ScatterPlotItem(size =20, pen=pg.mkPen('w'), pxMode=True) #pg.ScatterPlotItem(pxMode=True)   ## Set pxMode=False to allow spots to transform with the view
w0.addItem(curveS0)

# 2) for detected object Doppler scatterPlot
w1 = win.addPlot()
w1.setRange(xRange=[0,detRange],yRange= [-10,10]) 
w1.setLabel('bottom', 'V1 Object Position(x,y)', 'meter')
w1.setLabel('left', 'Meter', '')
spots1 = []
curveS1 = pg.ScatterPlotItem(size=20, pen=pg.mkPen('g'), pxMode=True)
w1.addItem(curveS1) 



# 3)plot Range Profile
win.nextRow()
p2 = win.addPlot(colspan=1)
#p2.setRange(xRange=[0,127],yRange= [0,150]) 
#p2.setRange(xRange=[0,127],yRange= [0,150]) 
#p2.setXRange(0,127, padding=None, update=True)
p2.setLabel('bottom', 'V2 Range Profile(W)/V3 Noise Profile(G)', 'Points')
p2.setLabel('left', 'Magnitude', 'A.U.')

curve2 = p2.plot(tr2)
curve21 = p2.plot(tr21,pen=pg.mkPen('g'))

# 4)CPU Loading
p3 = win.addPlot(colspan=1)
p3.setLabel('bottom', 'V6 Stats Information', 'Points')
p3.setLabel('left', 'CPU Load', '%')
p3.setYRange(0,20, padding=None, update=True)

curve3 = p3.plot(tr4)

# 
# plot data update 
#
def updatePlot():
	global v1len,v2len,v3len,spots0,spots1,tr2,tr21,tr4
	
	if v1len !=0:
		curveS0.setData(spots0)
		curveS1.setData(spots1)
		curve2.setData(tr2)
		curve21.setData(tr21)
		curve3.setData(tr4)
		
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
port = serial.Serial("/dev/ttyTHS1",baudrate = 921600*2, timeout = 0.5) 

#for pi 4 UART port
#port = serial.Serial("/dev/ttyS0",baudrate = 921600, timeout = 0.5)
#Drone Object Detect Radar initial 
drn = droneRN.DroneRN(port)

v1len = 0
v2len = 0
v3len = 0
v6len = 0
v7len = 0

svd.sm = False 
 
def drnExec():
	global spots0,spots1,tr2,tr21,v1len,v2len,v3len,v6len,v7len
	
	(dck,v1,v2,v3,v6,v7) = drn.tlvRead(False)
	#hdr = drn.getHeader()
	#drn.headerShow()
	 
	if dck == 1:
		v1len = len(v1)
		v2len = len(v2)
		v3len = len(v3)
		v6len = len(v6)
		v7len = len(v7)
		print("Sensor Data: [v1,v2,v3,v6,v7]:[{:d},{:d},{:d},{:d},{:d}]".format(v1len,v2len,v3len,v6len,v7len))
		#print(v1)	
		if v1len != 0:
			#v1:[(x,y,z,vel))...]
			spots0  = [{'pos': [ np.sqrt(v1[i][0]*v1[i][0] + v1[i][1]*v1[i][1] +  v1[i][2]*v1[i][2]),v1[i][3]], 'data': 1, 'brush':pg.intColor(i, v1len), 'symbol': 'o', 'size': 10 } for i in range(v1len)]
			spots1  = [{'pos': [ v1[i][0] ,v1[i][1] ], 'data': 1, 'brush':pg.intColor(i, v1len), 'symbol': 'o', 'size': 10 } for i in range(v1len)]
			tr2 = v2
			tr21 = v3
	
			#(0)shift left and append
			tr4[:-1] = tr4[1:]
			tr4[-1] = v6[0][5]
		 
	port.flushInput()
		
		 
def uartThread(name):
	port.flushInput()
	while True:
		drnExec()
					
thread1 = Thread(target = uartThread, args =("UART",))
thread1.setDaemon(True)
thread1.start()

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
	import sys
	if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
		QtGui.QApplication.instance().exec_()
