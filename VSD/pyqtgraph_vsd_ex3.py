# Parameters:
N19 = 23 # range profile points; BM201 := 19; BM501 := 23 

# -*- coding: utf-8 -*-
"""
Various methods of drawing scrolling plots.
"""
# https://github.com/pyqtgraph/pyqtgraph/tree/develop/examples
#https://github.com/pyqtgraph/pyqtgraph/blob/develop/examples/scrollingPlots.py
#import initExample ## Add path to library (just for examples; you do not need this)

import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui

import numpy as np
import numpy.matlib 

import serial
#import Jetson.GPIO as GPIO
from mmWave import vitalsign
import time
import struct
import sys
from collections import deque
from threading import Thread
import datetime
from scipy.fftpack import fft
from scipy import signal

from PyQt5.QtGui import QPalette,QFont
from PyQt5.QtWidgets import QLabel,QMainWindow
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
 
        self.setFixedSize(600,180)
        self.l0 = QLabel(self)
        self.l0.setFixedWidth(300)
        self.l0.setFixedHeight(40)
        self.l0.setAlignment(Qt.AlignCenter)
        self.l0.setText("Breathing(bpm)")
        self.l0.move(0,0)
        
        self.l1 = QLabel(self)
        self.l1.setFixedWidth(300)
        self.l1.setFixedHeight(40)
        self.l1.setAlignment(Qt.AlignCenter)
        self.l1.setText("Heart Rate(bpm)")
        self.l1.move(300,0)
        
        pe = QPalette()
        pe.setColor(QPalette.WindowText,Qt.yellow)        
        pe.setColor(QPalette.Background,Qt.gray)
        self.l0.setAutoFillBackground(True)
        self.l0.setPalette(pe)
        self.l1.setAutoFillBackground(True)
        self.l1.setPalette(pe)
        
        self.l0.setFont(QFont("Roman times",20,QFont.Bold))
        self.l1.setFont(QFont("Roman times",20,QFont.Bold))
        
        self.lbr = QLabel(self)
        self.lbr.setFixedWidth(300)
        self.lbr.setFixedHeight(60)
        self.lbr.setAlignment(Qt.AlignCenter)
        self.lbr.setFont(QFont("Roman times",55,QFont.Bold))
        self.lbr.setText("Breathing")
        self.lbr.move(0,75)
        
        self.lhr = QLabel(self)
        self.lhr.setFixedWidth(300)
        self.lhr.setFixedHeight(60)
        self.lhr.setAlignment(Qt.AlignCenter)
        self.lhr.setFont(QFont("Roman times",55,QFont.Bold))
        self.lhr.setText("Heart Rate")
        
        self.lhr.move(300,75)

class globalV:
	count = 0
	hr = 0.0
	br = 0.0
	zcAveNum = 20
	zcAveStart = 19 #zcAveNum-1
	
	def __init__(self, count):
		self.count = count

win = pg.GraphicsWindow()

pg.setConfigOption('foreground', 'y')
win.setWindowTitle('Vital Sign Demo')

maxlen = 200
ft0  = np.zeros(maxlen)
ft1  = np.zeros(maxlen)
brw0 = np.zeros(maxlen)
hrw1 = np.zeros(maxlen)
br0  = np.zeros(maxlen)
hr1  = np.zeros(maxlen)
cd6  = np.zeros(maxlen)
rp7  = np.zeros(N19) # changed

#**********************************************
# fft0: Breathing    fft1: Heart Rate (200points)
#**********************************************
p0 = win.addPlot()
p0.setRange(xRange=[0,40],yRange=[0,2])
p0.setLabel('bottom', 'Breathing Rate FFT(ft0)', 'bpm')
br2t = np.linspace(0,600,100)
curve_ft0 = p0.plot(ft0)

p1 = win.addPlot()
p1.setRange(xRange=[0,200],yRange=[0,2])
p1.setLabel('bottom', 'Heart Rate FFT(ft1)', 'bpm')
hr2t = np.linspace(0,600,100)
curve_ft1 = p1.plot(ft1)

## Set up an animated arrow and text that track the curve
# Breathing rate
curvePoint_br_rt = pg.CurvePoint(curve_ft0) 
p0.addItem(curvePoint_br_rt)
text_br_rt = pg.TextItem("", anchor=(0.5, 1.7),color = 'y')
text_br_rt.setParentItem(curvePoint_br_rt)
arrow0 = pg.ArrowItem(angle=270)
arrow0.setParentItem(curvePoint_br_rt)
# Heart rate
curvePoint_hr_rt = pg.CurvePoint(curve_ft1)
p1.addItem(curvePoint_hr_rt)
text_hr_rt = pg.TextItem("", anchor=(0.5, 1.7),color = 'y')
text_hr_rt.setParentItem(curvePoint_hr_rt)
arrow1 = pg.ArrowItem(angle=270)
arrow1.setParentItem(curvePoint_hr_rt)
#*******************************


#************* 
hrLow =  0.0
hrHigh = 200.0
brLow =  0.0
brHigh = 40.0
def jb_br_loc2Val(inp):
	return inp * (brHigh - brLow)/40 * 600/100  + brLow
	
def jb_hr_loc2Val(inp):
	return inp * (hrHigh - hrLow)/200 * 600/100 + hrLow

def update_fft():
	global ft0,ft1,hr2t,br2t,ft0A,ft1A
	curve_ft0.setData(br2t,ft0)
	curve_ft1.setData(hr2t,ft1)
	
	#Set cursor location(breathing rate)
	br_idx = np.argmax(ft0)
	curvePoint_br_rt.setPos(br_idx/(len(ft0)-1))
	text_br_rt.setText("{:}".format(jb_br_loc2Val(br_idx)))
	
	#Set cursor location(heart rate)
	hr_idx = np.argmax(ft1)
	curvePoint_hr_rt.setPos(hr_idx/(len(ft1)-1))
	text_hr_rt.setText("{:}".format(jb_hr_loc2Val(hr_idx)))

#**************************************
#(windowing) Breathing rate waveform & heart rate waveform after windowing
#************************************** 
win.nextRow()
p2 = win.addPlot()
p2.setLabel('bottom', 'Breathing Rate(windowing[brw0])', 'unit:sec')
curve_brw = p2.plot(brw0)

p3 = win.addPlot()
p3.setLabel('bottom', 'Heart Rate(windowing[hrw1])', 'unit:sec')
curve_hrw = p3.plot(hrw1)
p23t = np.linspace(0,10,200)

def update_windowing():
	global p23t,brw0,hrw1
	curve_brw.setData(p23t,brw0)
	curve_hrw.setData(p23t,hrw1)
 
#**************************************
#(filtering) Breathing rate waveform & heart rate waveform
#**************************************
win.nextRow()
p4 = win.addPlot()
p4.setLabel('bottom', 'Breathing Rate(br0)', 'unit:point')
curve_br = p4.plot(br0) 

p5 = win.addPlot()
p5.setLabel('bottom', 'Heart Rate(hr1)', 'unit:point')
curve_hr = p5.plot(hr1) 
#curve_hr = p5.plot(hr1,pen = pg.mkPen('y')) 

#***************************************
#(original) Chest Displacement: Points= 200 points
#***************************************
win.nextRow()
p6 = win.addPlot(colspan=1)
p6.setLabel('bottom', 'Chest Displacement(cd6)', 'unit:sec')
p6.setRange(xRange=(0,10))
p6t= np.linspace(0,10,200)
curve_cd = p6.plot(cd6)

#######################################
# range profile: Points= 64 points
#######################################
p7 = win.addPlot(colspan=1)
p7.setLabel('bottom', 'Range Profile(rp7)', 'y:RCS x:cm')
p7t = np.linspace(0.3,0.9, N19)
p7.setRange(xRange=[0.3,0.9])
curve_rp = p7.plot(rp7)

def update_indata():
	global p6t,br0,hr1,maxlen,cd6,rp7
	curve_cd.setData(p6t,cd6)
	curve_br.setData(br0)  
	curve_hr.setData(hr1) 
	curve_rp.setData(p7t,rp7)

#####################################
# windowing function
#####################################
tukwd = signal.tukey(200,alpha=0.5)

#####################################
# update all plots
#####################################
def update():
    update_indata()
    update_windowing()
    update_fft()
    mainwindow.lbr.setText("{:.2f}".format(gv.br))
    mainwindow.lhr.setText("{:.2f}".format(gv.hr))

timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(250) # 80: got(20 Times)   *50ms from uart: 

#use USB-UART
#for rpi
#port = serial.Serial("/dev/ttyUSB0",baudrate = 921600, timeout = 0.5)
#for jetson nano
#port = serial.Serial("/dev/ttyTHS1",baudrate = 921600, timeout = 0.5)
#for MAC os
port = serial.Serial("/dev/tty.usbmodemGY0052524",baudrate = 921600, timeout = 0.5)
#UART initial

#vital sign setup
gv = globalV(0)
vts = vitalsign.VitalSign(port)

fs = 1/0.05 # 50ms
nqy = 0.5 * fs * 60 # 600

b1,a1   = signal.butter(6,[40.0/nqy , 200.0/nqy], 'band') #heart rate parameter for fft
b, a    = signal.butter(6, [6.0/nqy , 30.0/nqy],'band') #breath rate parameter for fft 

def vtsExec():
	global ft0,ft1,ft0A,ft1A,cd6,rp7,b,a,b1,a1,tukwd,br0,brw0,hr1,hrw1
	
	(dck , vd, rangeBuf) = vts.tlvRead(False)
	
	#print(dck)
	vs = vts.getHeader()
	#print("MotionDet:{0:.4f}".format(vs.numDetectedObj))
	if dck:
 
		#print(len(rangeBuf))
		rp7 = [np.sqrt(rangeBuf[i*2]*rangeBuf[i*2] + rangeBuf[i*2+1]*rangeBuf[i*2+1]) for i in range(N19)]		
		brf = vd.outputFilterBreathOut if vd.outputFilterBreathOut < np.pi else np.pi         
		hrf = vd.outputFilterHeartOut if vd.outputFilterHeartOut   < np.pi else np.pi
		
		gv.br = vd.breathingRateEst_FFT
		gv.br = gv.br if gv.br < 500 else 500
			 
		gv.hr = vd.heartRateEst_FFT
		gv.hr = gv.hr if gv.hr < 500 else 500
		gv.count = vs.frameNumber
		
		#
		#(0)insert chest Displacement 
		#
		#shift left and insert
		cd6[:-1] = cd6[1:]
		cd6[-1]  = vd.unwrapPhasePeak_mm
		
		if True:
			pt = datetime.datetime.now()
			
			#-----------breathing rate--------------------
			#(3.0)breathing rate bandpass filter
			br0 = signal.filtfilt(b, a, cd6)
			#(3.0.1) remove DC level
			br0d = np.diff(br0)
			br0d = np.append(br0d,0.0)
			#(3.0.2) windowing
			brw0 = br0d * tukwd
	
			#-----------heart rate ---------
			#(3.1)heart rate bandpass filter
			hr1 = signal.filtfilt(b1, a1, cd6)
			#(3.1.1) windowing
			hrw1 = hr1 * tukwd
			#print("vd.conf  br:{:f}   hr:{:f}".format(vd.outputFilterBreathOut ,vd.outputFilterHeartOut ) )
			
			#---- fft ---------------
			# you can select better FFT function to get better result
			# 
			#(3.0.3)breathing fft
			yf0 = fft(brw0)
			ft0 = np.abs(yf0[0:200//2])
			ft0 = ft0/np.amax(ft0)
			
			#(3.0.4)heart rate fft
			yf1 = fft(hrw1)
			ft1 = np.abs(yf1[0:200//2]) 
			ft1 = ft1/np.amax(ft1)
			
			ct = datetime.datetime.now()
			#print("Heart Rate:{:.4f} Breath Rate:{:.4f} #:{:d} execTime:{}".format(gv.hr,gv.br,vs.frameNumber, ct-pt))

			#mainwindow.lbr.setText("{:.2f}".format(gv.br_zc))
			#mainwindow.lbr.setText("{:.2f}".format(fmax))
			#mainwindow.lhr.setText("{:.2f}".format(gv.hr_zc))
			#mainwindow.lfm.setText("{:d}".format(vs.frameNumber))
			#mainwindow.lex.setText("execTime:{}".format( ct-pt))	
			#mainwindow.l1.setText("Heart Rate:{:.4f} Breath Rate:{:.4f} #:{:d} execTime:{}".format(gv.hr,gv.br,vs.frameNumber, ct-pt))
			print("HR:{:.4f} BR:{:.4f} flag:{}".format(gv.hr,gv.br,vd.motionDetectedFlag ))

		 
def uartThread(name):
	pt = datetime.datetime.now()
	ct = datetime.datetime.now()
	port.flushInput()
	while True:
		vtsExec()
					
thread1 = Thread(target = uartThread, args =("UART",))
thread1.setDaemon(True)
thread1.start()


## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
	import sys
	if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
		mainwindow=MainWindow()
		mainwindow.show()
		QtGui.QApplication.instance().exec_()
