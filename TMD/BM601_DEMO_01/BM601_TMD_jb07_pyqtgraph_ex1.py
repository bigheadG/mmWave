###########################################################################
# jb07_pyqtgraphy_ex1.py    2023.02.13
# Hardware: IWR1843 ISK ES2
# Firmware: V20.12A, V80.36 and V8062R testing
# Software: BM601_TMD_jb07_pyqtgraphy_ex1.py
# Python: V3.9.5
########################################################################
# Revision History:
# jb00 2021.09.11 1. original
# jb01 2021.09.12 1. added jb_v7Text() and called in update() thread 
# jb02 2021.09.13 1. draw grid on window 
# jb03 2021.09.15 1. for 2D70M50ms based on V80.31_TMD
#                 2. library 'trafficTMD' should be updated to fit new data structure
# jb04 2021.09.15 1. for real field testing 
# jb05 2021.09.22 1. adde fN for frame number
# jb06 2021.10.20 1. for REAL field test on V20.12, V80.36 and V80.37  
# jb07 2021.10.20 1. for REAL field test on V80.36 (passed) but V80.37 (failed) 
# jb07 2022.03.08 1. for REAL field test on V80.38
#                 2. for x axis post_processing, jb_newX()   
###########################################################################
'''
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
'''
###########################################################################
# Parameters:
JB_UART_PORT 		= 'COM30' 	# sel COM12 (TI EVM owner JB), COM5 (TI EVM owner Lilin) or COM9 (JB EVM)' # depends
JB_RANGE_NEAR		= -2 		# default 0 Meter
JB_RANGE_FAR  		= 140		# default 100 Meter
JB_LEFT 		= -15 		#-10	# default -1 Meter
JB_RIGHT 		= +15 		#+20	# default 6 Meter
JB_POINT_CLOUD_SIZE	= 5			# default 5
JB_TARGET_SIZE		= 20		# default 20
JB_SNR_TH 		= 0 		# for example: set snr threshold as 150, this value is recommended observing from REAL case
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
np.set_printoptions(precision=2,suppress=True)

import serial
#import Jetson.GPIO as GPIO

# test, 
from mmWave import trafficMD_I480
#import trafficMD_I480

#import trafficMD # local

import time
import struct
import sys

from threading import Thread
import datetime
from scipy.fftpack import fft
import numpy as np
from scipy import signal

import pandas as pd
pd.options.display.float_format = '{:,.2f}'.format

# run pyqtgraph example
#import pyqtgraph.examples
#pyqtgraph.examples.run()
#exit()

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
fN = 0 # frame number

########################################################################
# open a WINDOW
win = pg.GraphicsWindow()

pg.setConfigOption('foreground', 'y') # show grid in YELLOW
 

win.resize(1200, 800)
win.setWindowTitle('Traffic Monitor Detect Radar (V80.38_TMD)')
# 1) for TARGET location scatterPlot
# for V7 TARGET
w3 = win.addPlot()


w3.setRange(xRange= [JB_LEFT, JB_RIGHT], yRange=[JB_RANGE_NEAR, JB_RANGE_FAR]) # see top parameters setting 
w3.setLabel('left',   'V7 Target Location Y Axis', 'meter')
w3.setLabel('bottom', 'V7 Target Location X Axis', 'meter')
w3.showGrid(x=True, y=True, alpha=1.0)  # now we can turn on the grid
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
	global fN
	 
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
		#old: refer: v7     =: [(tid,posX,posY,posZ,velX,velY,velZ,accX,accY,accZ),....]
		#            v7 index:     0    1    2    3    4    5    6    7    8    9
		#new; refer: v7     =: [(posX,posY,posZ,velX,velY,velZ,accX,accY,accZ, tid),....]
		#             v7 index:     0    1    2    3    4    5    6    7    8    9
		textA = pg.TextItem()
		textA.setFont(QtGui.QFont("consolas", 16))
		textA.setPos(v7[i][0], v7[i][1])
		jb_posStr = '   (fN={},tid={:2d},x={:.1f},y={:.1f},vy={:.1f}Km/H)'.format(fN, int(v7[i][9]), v7[i][0], v7[i][1], v7[i][4] * 3.6)
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
		#print(v7)
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
# test, 
tmd = trafficMD_I480.TrafficMD_I480(port)
tmd.X_CALI_DEGREE = 0.0 #2.134 # set 0.0 for logging data then changed it 

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
	global fN, JB_SNR_TH
	
	(dck,v6,v7,v8,v9) = tmd.tlvRead(False)	
	#dck = 1
	if dck == 1:
		v6len = len(v6)
		v7len = len(v7)
		v8len = len(v8)
		v9len = len(v9)
		fN = tmd.hdr.frameNumber
		print('\n')
		print('###########################')
		print('# fN={:10d}'.format(fN))
		print('###########################')
		print("JB> Sensor Data: [fN, v6, v7, v8, v9] := [{:10d},{:3d},{:3d},{:3d},{:3d}]".format(fN,v6len,v7len,v8len,v9len))
		#print("JB> Sensor Data: [fN, v6, v7]:[{:10d}, {:3d}, {:3d}]".format(fN, v6len, v7len))
		
		
		print(v6)
		for i in range(v6len):
			print(v6[i])
		
		
		
		#(1) for POINT CLOUD
		if 0 and v6len > 0:
						
			# changed from df to array
			####################################################################################
			# deNoise Algorithm: 
			# v6 => v6A => v6A_sorted => v6A_filtered => v6
			# PseudoCode: if tid < 253 then removing noise point cloud 
			# PseudoCode: if snr >= SNR_TH then removing noise point cloud 
			# Alert: please using numpy array for speed up if had timing demands, here using df for easy reading only 			
			# V6 structure: [(range,azimuth,elevation,doppler,sx,sy,sz),......]
			# refer01: ['r', 'a', 'e', 'd', 'sx', 'sy', 'sz']
			# refer02: ['r', 'a', 'e', 'd', 'sx', 'sy', 'sz', 'tid', 'snr', 'noise'] # expanded 3 fields
			#          0    1    2    3      4      5     6      7      8        9
			v6_len = np.array(v6).shape[0] 
			v6_width = np.array(v6).shape[1] + 3 # 3 means field number ['tid', 'snr', 'noise'] 
			v6A = np.zeros( (v6_len, v6_width) ) # final columns = ['r', 'a', 'e', 'd', 'tid', 'snr', 'noise']
			v6A[:, 0:7] = v6 # copy 
			if len(v8) > 0:
				v6A[:, 7] = v8 # insert field, 'tid' 
			if len(v9) > 0:
				v6A[:, 8:] = v9 # insert field, 'snr' 'noise'			
			
			# sorted by 8, 'snr' 
			v6A_sorted_indices = np.lexsort((v6A[:, 7], v6A[:, 6], v6A[:, 5], v6A[:, 4], v6A[:, 3], v6A[:, 2], v6A[:, 1], v6A[:, 0], v6A[:, 8]))[::-1] # sort filed by 8 ('snr') then reverse
			v6A_sorted = v6A[v6A_sorted_indices]
			# filter out invalid tid, if tid < 253 
			jb_tid_logic = v6A_sorted[:, 7] < 253 
			v6A_sorted = v6A_sorted[jb_tid_logic]  
			#print("# refer02: ['r', 'a', 'e', 'd', 'sx', 'sy', 'sz', 'tid', 'snr', 'noise']")
			#print('v6A_sorted shape={}\nv6A_sorted=\n{}\n'.format(v6A_sorted.shape, v6A_sorted)) # example (13,10)				
			jb_snr_logic = v6A_sorted[:, 8] >= JB_SNR_TH # filter logic by if snr > JB_SNT_TH
			#print('v6A_sorted shape={}\nv6A_sorted=\n{}\n'.format(v6A_sorted.shape, v6A_sorted)) # example (13,10)				
			#print(jb_snr_logic)
			v6A_filtered = v6A_sorted[jb_snr_logic] # filter out noise and keep wanted point cloud
			#print('run deNoise Algorithm, if snr >= JB_SNR_TH {}'.format(JB_SNR_TH)) 
			#print('v6A_filtered shape={}\nv6A_filtered=\n{}\n'.format(v6A_filtered.shape, v6A_filtered)) 			
			print("JB> refer v6: ['r', 'a', 'e', 'd', 'sx', 'sy', 'sz', 'tid', 'snr', 'noise']")
			print('JB> v6A_filtered=\n{}\n'.format(v6A_filtered)) 				
			v6 = v6A_filtered[:, 0:7] # extract the first 7 fields, ['r', 'a', 'e', 'd', 'sx', 'sy', 'sz']				
			v6len = len(v6) # update new v6 len
 			####################################################################################

			''' keep df syntax
			####################################################################################
			# deNoise Algorithm: 
			# PseudoCode: if snr >= SNR_TH then removing noise point cloud 
			# Alert: please using numpy array for speed up if had timing demands, here using df for easy reading only 
			# final columns = ['r', 'a', 'e', 'd', 'tid', 'snr', 'noise'] then sort() by 'snr' in descending order
			
			# V6 structure: [(range,azimuth,elevation,doppler,sx,sy,sz),......]
			JB_SNR_TH = 150 # for example: set snr threshold as 200, this value is recommended observing from REAL case
			# if v6 is list 		
			v6_df = pd.DataFrame(np.array(v6), columns=['r', 'a', 'e', 'd', 'sx', 'sy', 'sz'])
			v8_df = pd.DataFrame(v8)				
			v6_df['tid'] = v8_df # added new field of 'tid'
			v9_df = pd.DataFrame(v9, columns=['snr','noise'])
			v6_df['snr'] = v9_df['snr'] # added new field of 'snr'
			v6_df['noise'] = v9_df['noise'] # added new field of 'noise'
			v6_df = v6_df.sort_values(by=['snr'], ascending=False) # sorted by 'snr' in descending order
			v6_df_logic = v6_df['snr'] >= JB_SNR_TH # filter logic
			v6_df = v6_df[v6_df_logic] # filter out noise and keep wanted point cloud
			print('run deNoise Algorithm, if snr >= JB_SNR_TH {}'.format(JB_SNR_TH)) 
			print('v6_df shape={}\nv6_df=\n{}\n'.format(v6_df.shape, v6_df)) # (23, 2)				
			v6A = v6_df.to_numpy() # array
			v6 = v6A[:, 0:7] # extract the first 7 fields, ['r', 'a', 'e', 'd', 'sx', 'sy', 'sz']				
			v6len = len(v6) # update new v6 len
			####################################################################################
			'''
			
			#v6[(range,azmuth,elevate,velociy)...] := {r, a, e, d}
			for i in range(len(v6)):
				x = v6[i][0]*np.sin(v6[i][1])
				y = v6[i][0]*np.cos(v6[i][1])
				#print('JB> (fN, i, x, y) = ({}, {}, {:.1f}, {:.1f})'.format(fN, i, x, y))
				
			spots0  = [{'pos': [v6[i][0]*np.sin(v6[i][1]),v6[i][0]*np.cos(v6[i][1])], 'data': 1, 'brush':pg.intColor(i, v6len), 'symbol': 'o', 'size': JB_POINT_CLOUD_SIZE } for i in range(v6len)]

		#(2) for TARGET
		
				# for TARGET
		if v7len > 0:
			v7_df = pd.DataFrame(np.array(v7))
			v7_df[0] = v7_df[0].astype(int) # id type is int
			
			print('JB> refer: v7     =: [(posX,posY,posZ,velX,velY,velZ,accX,accY,accZ,tid)]')
			print('JB> v7_df= \n{}'.format(v7_df))

		''' old
		if 0 and v7len > 0:
			#refer: v7     =: [(tid,posX,posY,posZ,velX,velY,velZ,accX,accY,accZ),....]
			#       v7 index:     0    1    2    3    4    5    6    7    8    9
			
			spots3  = [{'pos':  [ v7[i][1] , v7[i][2]]  , 'data': 1, 'brush':pg.intColor(i, v7len), 'symbol': 'o', 'size': JB_TARGET_SIZE } for i in range(v7len)]			
			
			
			JB_textCount += 1			
			pd.options.display.float_format = "   {:.1f}".format

			v7A = np.array(v7)
			v7A[:, 5] *= 3.6 # convert vy unit as Km/H
			#a = v7A[:, (0, 1, 2, 5)]
			a = v7A[:, (0, 1, 2, 5)]
			df = pd.DataFrame(a, columns=['id', 'x', 'y', 'vy(Km/H)'])
			df['id'] = df['id'].astype(int) # id type is int
			print('JB> V7=\n{}'.format(df))
		'''
			
		# Alert: tid at the end of structure	
		if 1 and v7len > 0:
			#refer: v7     =: [(posX,posY,posZ,velX,velY,velZ,accX,accY,accZ,tid),....]
			#       v7 index:      0    1    2    3    4    5    6    7    8   9	
			JB_TID_INDEX = 9
			JB_X_INDEX = 0
			JB_Y_INDEX = 1
			JB_VY_INDEX = 4

			spots3  = [{'pos': [ v7[i][JB_X_INDEX], v7[i][JB_Y_INDEX]], 'data': 1, 'brush':pg.intColor(i, v7len), 'symbol': 'o', 'size': JB_TARGET_SIZE } for i in range(v7len)]			

			JB_textCount += 1			
			pd.options.display.float_format = "   {:.1f}".format

			v7A = np.array(v7)
			v7A[:, 5] *= 3.6 # convert vy unit as Km/H
 
			a = v7A[:, (JB_TID_INDEX, JB_X_INDEX, JB_Y_INDEX, JB_VY_INDEX)] # 9 means tid
			df = pd.DataFrame(a, columns=['id', 'x', 'y', 'vy(Km/H)'])
			df['id'] = df['id'].astype(int) # id type is int
			print('JB> V7=\n{}'.format(df))
			
		#(3) merge POINT CLOUD and TARGET
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
