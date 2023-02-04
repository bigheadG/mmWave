 # -*- coding: utf-8 -*-
"""
#=======================================================================
# File Name: lpd_v24_2d_pyqtgraph_xy_50m.py
#
# Requirement:
# Hardware: BM201-ISK (AWR6843)
# Firmware: LPD
# config file:(V24_JB)people_detection_and_tracking_50m_2D_advanced.cfg
# lib: lpdISK 
# plot tools: pyqtgraph 2D
# Plot point cloud(V6) and Target(V7) in 2D figure
# type: Raw data
# Baud Rate:
#=======================================================================
 
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
import sys
from threading import Thread
from mmWave import lpdISK

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
 
win.setWindowTitle('Long Range People Detect 100m')

#**************************************

# 1) for detected object scatterPlot
#win.nextRow()
w0 = win.addPlot()
w0.setRange(xRange=[-100,100],yRange=[0,150])
w0.setLabel('bottom', 'V6 Poin Cloud', 'Meter')
w0.setLabel('left', 'range', 'meter')
spots0 = []
curveS0 = pg.ScatterPlotItem(size =20, pen=pg.mkPen('w'), pxMode=True) #pg.ScatterPlotItem(pxMode=True)   ## Set pxMode=False to allow spots to transform with the view
curveS1 = pg.ScatterPlotItem(size =20, pen=pg.mkPen('w'), pxMode=True)
w0.addItem(curveS0)
w0.addItem(curveS1)

# 
# plot data update 
#
def updatePlot():
	global v6len,spots0,spots1,v7len
	 
	curveS0.setData(spots0 if v6len != 0 else [])
	curveS1.setData(spots1 if v7len != 0 else [])
		
		
# update all plots
def update():
	updatePlot()
	 
#
#----------timer Update--------------------   
timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(143) #150  80: got(20 Times)   *50ms from uart: 
#------------------------------------------

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

port = serial.Serial("/dev/tty.usbmodemGY0043864",baudrate = 921600, timeout = 0.5)
#for NUC ubuntu 
#port = serial.Serial("/dev/ttyACM1",baudrate = 921600, timeout = 0.5)

radar = lpdISK.LpdISK(port) 
 
v6len = 0
v7len = 0
v8len = 0
v9len = 0

radar.sm = False 
'''
	for i in range(len(pct)):
		zt = pct[i][0] * np.sin(pct[i][2]) 
		xt = pct[i][0] * np.cos(pct[i][2]) * np.sin(pct[i][1])
		yt = pct[i][0] * np.cos(pct[i][2]) * np.cos(pct[i][1])
'''

fn = 0
prev_fn = 0
def radarExec():
	global spots0,spots1,v8len,v9len,v6len,v7len,prev_fn, fn
	
	(dck,v6,v7,v8,v9) = radar.tlvRead(False)
	hdr = radar.getHeader()
	#radar.headerShow()
	hdr = radar.getHeader()
	fn = hdr.frameNumber
	
	if prev_fn != fn:
		v6len = len(v6)
		v7len = len(v7)
		v8len = len(v8)
		v9len = len(v9)
		 
		print("Sensor Data: [v6,v7,v8,v9]:[{:d},{:d},{:d},{:d}]".format(v6len,v7len,v8len,v9len))
		
		#v6 struct = [(r,a,e,d),(r,a,e,d),(r,a,e,d)..]
		if v6len != 0:
			pc = v6
			spots0  = [{'pos': [pc[i][0] * np.cos(pc[i][2]) * np.sin(pc[i][1]),pc[i][0] * np.cos(pc[i][2]) * np.cos(pc[i][1])],'data': 1, 'brush':pg.intColor(i, v6len), 'symbol': 'o', 'size': 3 } for i in range(v6len)]
		 
		if v7len != 0:
			pct = v7
			spots1  = [{'pos': [pct[i][1],pct[i][2]],'data': 1, 'brush':pg.intColor(i, v7len), 'symbol': 's', 'size': 10 } for i in range(v7len)]
		 
			
		flag = True
			
	port.flushInput()
		
def uartThread(name):
	port.flushInput()
	while True:
		radarExec()
					
thread1 = Thread(target = uartThread, args =("UART",))
thread1.setDaemon(True)
thread1.start()

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
	import sys
	if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
		QtGui.QApplication.instance().exec_()
