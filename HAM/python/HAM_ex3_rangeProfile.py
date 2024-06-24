##################################################################
# please find 'try' for adjust parameters    2021.09.08
##################################################################


# -*- coding: utf-8 -*-
'''
Various methods of drawing scrolling plots.
'''
#https://github.com/pyqtgraph/pyqtgraph/tree/develop/examples
#https://github.com/pyqtgraph/pyqtgraph/blob/develop/examples/scrollingPlots.py
#import initExample ## Add path to library (just for examples; you do not need this)

import pyqtgraph as pg
#from pyqtgraph.Qt import QtCore, QtGui
from PyQt5 import QtGui, QtWidgets, QtCore   
from pyqtgraph.Qt import mkQApp, QtGui

import numpy as np
import numpy.matlib 

import serial
#import Jetson.GPIO as GPIO
import time
import struct
import sys

from threading import Thread
import datetime
from scipy.fftpack import fft
from scipy import signal
from mmWave import highAccuracy

# new
from PyQt5.QtGui import QPalette,QFont
from PyQt5.QtWidgets import QLabel,QMainWindow
from PyQt5.QtCore import Qt


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
 
        self.setFixedSize(300,180)
        self.l0 = QLabel(self)
        self.l0.setFixedWidth(300)
        self.l0.setFixedHeight(40)
        self.l0.setAlignment(Qt.AlignCenter)
        self.l0.setText("HAM(meter)")
        self.l0.move(0,0)
  
        pe = QPalette()
        pe.setColor(QPalette.WindowText,Qt.yellow)        
        pe.setColor(QPalette.Background,Qt.gray)
        self.l0.setAutoFillBackground(True)
        self.l0.setPalette(pe)
        
        self.l0.setFont(QFont("Roman times",20,QFont.Bold))

        self.lbr = QLabel(self)
        self.lbr.setFixedWidth(300)
        self.lbr.setFixedHeight(60)
        self.lbr.setAlignment(Qt.AlignCenter)
        self.lbr.setFont(QFont("Roman times",55,QFont.Bold))
        self.lbr.setText("HAM")
        self.lbr.move(0,75)
     

class globalV:
	count = 0
	br = 0.0
	objDistance = 0.0
	
	def __init__(self, count):
		self.count = count

#win = pg.GraphicsWindow()
win = pg.GraphicsLayoutWidget(show=True) 

pg.setConfigOption('foreground', 'y')
win.setWindowTitle('High Accuracy Measurement')

rp7 = np.zeros(256)

#######################################
# range profile: Points= 64 points
#######################################
p7 = win.addPlot(colspan=3)
p7.setLabel('bottom', 'Range Profile(rp7)', 'y:A.U. x:m')

##############################################################################
# try01, adjust parameters 
p7t = np.linspace(0.0, 10.0, 256) # 0 m to 10 m per 256  
p7.setRange(xRange=[0.0, 3.0]) # show range from 0 m to 1 m
##################################################################

curve_rp = p7.plot(rp7)

def update_indata():
	global rp7 ,p7t
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
    mainwindow.lbr.setText("{:.3f}".format(gv.distance))


timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(250) # 80: got(20 Times)   *50ms from uart: 

#use USB-UART
#for rpi
#port = serial.Serial("/dev/ttyUSB0",baudrate = 921600, timeout = 0.5)
#for jetson nano
#port = serial.Serial("/dev/ttyTHS1",baudrate = 921600, timeout = 0.5)
#for MAC os
port = serial.Serial("COM14",baudrate = 921600, timeout = 0.5)
#for windows
#port = serial.Serial("COM20", baudrate = 921600, timeout = 0.5)


#ham setup
gv = globalV(0)
ham = highAccuracy.HighAccuracy(port)

def hamExec():
	global rp7,tukwd
	(dck , hd, rangeBuf) = ham.tlvRead(False)
	vs = ham.getHeader()
	
	if dck:
		#print(len(rangeBuf))
		
		##############################################################################################
		# try02, run fft
		w_1024 = signal.tukey(1024, alpha=0.5)
		rp7_1024 = rangeBuf * w_1024  # windowing
		rp7_512_fft = np.abs(np.fft.fft(rp7_1024))[0:512] # fft
		rp7 = rp7_512_fft[0:256] # half
		##############################################################################################

		gv.distance = hd.rangeValue 
		print("distance:{:.3f}m".format(gv.distance))

		 
def uartThread(name):
	pt = datetime.datetime.now()
	ct = datetime.datetime.now()
	port.flushInput()
	while True:
		hamExec()
					
thread1 = Thread(target = uartThread, args =("UART",))
thread1.setDaemon(True)
thread1.start()


## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
	import sys
	if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
		mainwindow=MainWindow()
		mainwindow.show()
		#QtGui.QApplication.instance().exec_()
		QtWidgets.QApplication.instance().exec_()  # for Pyqtgraph_V0.13
