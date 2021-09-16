###########################################################################
# jb_pyqtgraphy_TMD_ex1.py    2021.09.11
# Hardware: IWR1843 ISK ES2
# Firmware: V80.31 TMD 2D70M50ms
# Software: jb04_pyqtgraphy_TMD_ex1.py
# Python: V3.9.5
# Revision History:
# jb00 2021.09.11 1. original
# jb01 2021.09.12 1. added jb_v7Text() and called in update() thread 
# jb02 2021.09.13 1. draw grid on window 
# jb03 2021.09.15 1. for 2D70M50ms based on V80.31_TMD
#                 2. library 'trafficTMD' should be updated to fit new data structure
# jb04 2021.09.15 1. for real field testing 
###########################################################################
# Parameters:
JB_UART_PORT 		= 'COM12'
JB_RANGE_NEAR		= 0 	# default 0 Meter
JB_RANGE_FAR  		= 120	# default 100 Meter
JB_LEFT 			= -4	# default -1 Meter
JB_RIGHT 			= +16	# default 6 Meter
JB_POINT_CLOUD_SIZE = 5		# default 5
JB_TARGET_SIZE		= 50	# default 20
###########################################################################

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

from mmWave import trafficMD_I480

#import trafficMD # local

import time
import struct
import sys

from threading import Thread
import datetime
from scipy.fftpack import fft
import numpy as np
from scipy import signal

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

########################################################################
# open a WINDOW
win = pg.GraphicsWindow()
win.resize(1200, 800)
win.setWindowTitle('Traffic Monitor Detect Radar (V80.31_TMD)')
# 1) for TARGET location scatterPlot
# for V7 TARGET
w3 = win.addPlot()
w3.setRange(xRange= [JB_LEFT, JB_RIGHT], yRange=[JB_RANGE_NEAR, JB_RANGE_FAR]) # see top parameters setting 
w3.setLabel('left',   'V7 Target Location Y Axis', 'meter')
w3.setLabel('bottom', 'V7 Target Location X Axis', 'meter')
w3.showGrid(x=True, y=True)  # now we can turn on the grid
spots3 = [] # for TARGET
curveS3 = pg.ScatterPlotItem(size= 20, pen= pg.mkPen('w'), pxMode= True) #pg.ScatterPlotItem(pxMode=True)   ## Set pxMode=False to allow spots to transform with the view
w3.addItem(curveS3)
spots0 = [] # for POINT CLOUD
########################################################################

########################################################################
# for V7 TARGET TAG
# ALERT: should be called in update() thread otherwise WARNING on thread issue
textA_old = [pg.TextItem()]
JB_skipFirst = 0
JB_textCount = 0
def jb_v7Text(w3, v7):
	global textA_old, JB_skipFirst, JB_textCount
	 
	# (1) clean old target text
	# due to TARGET is NO needed to be removed at first time
	if JB_skipFirst == 0:
		JB_skipFirst = 1  
	else:
		for i in range(len(textA_old)):
			w3.removeItem(textA_old[i])
			
	# (2) insert new target text
	textA_old = [] # all cleared before running
	for i in range(len(v7)):
		#refer: v7     =: [(tid,posX,posY,posZ,velX,velY,velZ,accX,accY,accZ),....]
		#       v7 index:     0    1    2    3    4    5    6    7    8    9
		textA = pg.TextItem()		
		textA.setPos(v7[i][1], v7[i][2])
		jb_posStr = '     (x={:.1f},y={:.1f},vy={:.1f},c={}, l={})'.format(v7[i][1], v7[i][2], v7[i][5], JB_textCount, len(v7))
		textA.setColor(pg.intColor(i, len(v7))) # set the same color with TARGET dot		
		textA.setPlainText(jb_posStr)
		w3.addItem(textA)
		textA_old.append(textA) # saved into old array
########################################################################	

########################################################################	
# 
# plot data update 
#
# update all plots
def update():
	global spots0, spots3,v7
		
	if v7len > 0:
		print(v7)
		curveS3.setData(spots3) # for RangeX  vs RangeY
		jb_v7Text(w3, v7) # ALERT: should be put here otherwise WARNING on thread issue
########################################################################	
	 
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
#port = serial.Serial("/dev/tty.usbmodemGY0052854",baudrate = 921600, timeout = 0.5)
#for pi 4 UART port
#port = serial.Serial("/dev/ttyS0",baudrate = 921600, timeout = 0.5)
port = serial.Serial(JB_UART_PORT, baudrate = 921600, timeout = 0.5)

############################################################################################################
#Traffice Monitor Radar initial 
tmd = trafficMD_I480.TrafficMD_I480(port)
v6len = 0
v7len = 0
v8len = 0
v9len = 0
tmd.sm = False 
tmd.debug = True
spots3= []
def tmdExec():
	global spots0,spots1,spots2,spots3,v6len,v7len,v8len,v9len
	global testA
	global JB_textCount, v7, JB_POINT_CLOUD_SIZE, JB_TARGET_SIZE
	
	(dck,v6,v7,v8,v9) = tmd.tlvRead(False)	
	#dck = 1
	if dck == 1:
		v6len = len(v6)
		v7len = len(v7)
		v8len = len(v8)
		v9len = len(v9)
		fN = tmd.hdr.frameNumber
		print('\n\n')
		print('###########################')
		print('# fN={:10d}'.format(fN))
		print('###########################')
		print("JB> Sensor Data: [fN,v6,v7,v8,v9]:[{:10d},{:3d},{:3d},{:3d},{:3d}]".format(fN,v6len,v7len,v8len,v9len))
		# for POINT CLOUD
		if v6len > 0:
			#v6[(range,azmuth,elevate,velociy)...] := {r, a, e, d}
			for i in range(len(v6)):
				x = v6[i][0]*np.sin(v6[i][1])
				y = v6[i][0]*np.cos(v6[i][1])
				#print('JB> (fN, i, x, y) = ({}, {}, {:.1f}, {:.1f})'.format(fN, i, x, y))
			spots0  = [{'pos': [v6[i][0]*np.sin(v6[i][1]),v6[i][0]*np.cos(v6[i][1])], 'data': 1, 'brush':pg.intColor(i, v6len), 'symbol': 'o', 'size': JB_POINT_CLOUD_SIZE } for i in range(v6len)]
		# for TARGET
		if v7len > 0:
			#refer: v7     =: [(tid,posX,posY,posZ,velX,velY,velZ,accX,accY,accZ),....]
			#       v7 index:     0    1    2    3    4    5    6    7    8    9
			spots3  = [{'pos': [ v7[i][1], v7[i][2]], 'data': 1, 'brush':pg.intColor(i, v7len), 'symbol': 'o', 'size': JB_TARGET_SIZE } for i in range(v7len)]			
			JB_textCount += 1
			print('JB> v7 [x, y, vy], count, v7_len = \n{}, {}, {}'.format(np.array(v7)[:, (1,2,4)], JB_textCount, len(v7)))
		# merge POINT CLOUD and TARGET
		spots3 += spots0	
	port.flushInput()
############################################################################################################
				 
############################################################################################################
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
############################################################################################################
