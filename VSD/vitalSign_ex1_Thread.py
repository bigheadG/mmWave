''' 
vital: Vital Signs : 2018/3/10 15:47

'''
import serial
import time
import struct
import sys
from collections import deque
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from threading import Thread
import RPi.GPIO as GPIO
from matplotlib.figure import Figure
import numpy as np
from mmWave import vitalsign

import datetime
from tkinter import *

#**************** GUI part ********************
window = Tk()
window.title("Welcome to Vital Sign Demo")
hrString = StringVar()
hrString.set("Heart Rate")
brString = StringVar()
brString.set("Breath Rate")
countString = StringVar()
countString.set("0")

hl = Label(window, textvariable= hrString , font=("Arial Bold", 50) ).grid(column = 0 ,row = 0)
bl = Label(window, textvariable= brString ,font=("Arial Bold", 50)).grid(column=0, row=1)
cl = Label(window, textvariable= countString ,font=("Arial Bold", 25)).grid(column=0, row=2)

#**********************************************

class globalV:
	count = 0
	hr = 0.0
	br = 0.0
	def __init__(self, count):
		self.count = count
		
#UART initial
try:    #pi 3
	port = serial.Serial("/dev/ttyS0",baudrate = 921600, timeout = 0.5)
except: #pi 2
	port = serial.Serial("/dev/ttyAMA0",baudrate = 921600, timeout = 0.5)

#
#Object initail
#
gv = globalV(0)

vts = vitalsign.VitalSign(port)
 
# UART : 50 ms
def uartThread(name):
	pt = datetime.datetime.now()
	ct = datetime.datetime.now()
	port.flushInput()
	while True:
		#mmWave/VitalSign tlvRead & Vital Sign 
		#print(datetime.datetime.now().time())
		pt = datetime.datetime.now()
		(dck , vd, rangeBuf) = vts.tlvRead(False)
		
		vs = vts.getHeader()
		#print("MotionDet:{0:.4f}".format(vs.numDetectedObj))
		if dck:
			ct = datetime.datetime.now()
			brf = vd.outputFilterBreathOut if vd.outputFilterBreathOut < np.pi else np.pi         
			hrf = vd.outputFilterHeartOut if vd.outputFilterHeartOut < np.pi else np.pi
			#add((brf,hrf))
			
			gv.br = vd.breathingRateEst_FFT
			gv.br = gv.br if gv.br < 500 else 500
		
			 
			gv.hr = vd.heartRateEst_FFT
			gv.hr = gv.hr  if gv.hr < 500 else 500
			gv.count = vs.frameNumber
			
			brString.set("Breath:{0:.4f}".format(gv.br))
			hrString.set("Heart:{0:.4f}".format(gv.hr))
			countString.set("#{:d} {}".format(gv.count,ct - pt)) # about: 13 times
			#print("Heart Rate:{:.4f} Breath Rate:{:.4f} #:{:d}  {}".format(gv.hr,gv.br,vs.frameNumber, ct-pt))
			
			port.flushInput()
			#print("Filter OUT:{0:.4f}".format(vd.outputFilterHeartOut))
			'''
			print("EST FFT:{0:.4f}".format(vd.heartRateEst_FFT))
			print("EST FFT 4Hz:{0:.4f}".format(vd.heartRateEst_FFT_4Hz))
			print("EST FFT xCorr:{0:.4f}".format(vd.heartRateEst_FFT_4Hz))
			print("Confi Heart Out:{0:.4f}".format(vd.confidenceMetricHeartOut))
			print("Confi Heart O 4Hz:{0:.4f}".format(vd.confidenceMetricHeartOut_4Hz))
			print("Confi Heart O xCorr:{0:.4f}".format(vd.confidenceMetricHeartOut_xCorr))
			'''
			


thread1 = Thread(target = uartThread, args =("UART",))
thread1.setDaemon(True)
thread1.start()

window.mainloop()








