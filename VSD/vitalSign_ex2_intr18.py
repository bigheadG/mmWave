''' 
vital: Vital Signs : 2018/12/10 15:47


**** if error founded ******
Traceback (most recent call last):
  File "vitalSign_BH_ex2_Thread_intr18.py", line 74, in <module>
    GPIO.add_event_detect(18, GPIO.RISING,my_callback)
RuntimeError: Failed to add edge detection

*** plesae use the following command to clear this error ****

~#gpio unexport 18 

'''
import os
import serial
import time
import struct
from collections import deque
import numpy as np
from threading import Thread
import RPi.GPIO as GPIO
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
lRateString = StringVar()
lRateString.set("0")

hl = Label(window, textvariable= hrString , font=("Arial Bold", 50) ).grid(column = 0 ,row = 0)
bl = Label(window, textvariable= brString ,font=("Arial Bold", 50)).grid(column=0, row=1)
cl = Label(window, textvariable= countString ,font=("Arial Bold", 30)).grid(column=0, row=2)
ll = Label(window, textvariable= lRateString ,font=("Arial Bold", 30)).grid(column=0, row=3)


class globalV:
	count = 0
	lostCount = 0
	startFrame = 0
	inCount = 0
	hr = 0.0
	br = 0.0
	ct = datetime.datetime.now()
	def __init__(self, count):
		self.count = count
		
		
#UART initial
try:    #pi 3
	port = serial.Serial("/dev/ttyS0",baudrate = 921600, timeout = 0.5)
except: #pi 2
	port = serial.Serial("/dev/ttyAMA0",baudrate = 921600, timeout = 0.5)

gv = globalV(0)

#*****************GPIO Setting*****************************
def my_callback(channel):
	#ct = datetime.datetime.now()
	#print("intr:{}".format(ct - gv.ct))
	uartIntr("VitalSign")
	gv.count = gv.count + 1

#****** GPIO 18 for rising edge to catch data from UART ****
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.add_event_detect(18, GPIO.RISING,my_callback)


#
#Object initail
#
vts = vitalsign.VitalSign(port)
 
def uartIntr(name):
	pt = datetime.datetime.now()
	#mmWave/VitalSign tlvRead & Vital Sign 
	#print(datetime.datetime.now().time())
	(dck , vd, rangeBuf) = vts.tlvRead(False)
	vt = vts.getHeader()
	#print("MotionDet:{0:.4f}".format(vts.numDetectedObj))

	if gv.count > 3:
		#print("Delay:{:d}".format(gv.count))
		gv.lostCount = gv.lostCount + 1
		print(gv.lostCount)
		time.sleep(0.097)
		port.flushInput()
		gv.count = 0
	else:
		port.flushInput()
		
		 
	if dck:
		gv.count = 0 
		gv.inCount += 1
		ct = datetime.datetime.now()
		#print("data in:{}".format(ct))
		#print(":")
		brf = vd.outputFilterBreathOut if vd.outputFilterBreathOut < np.pi else np.pi         
		hrf = vd.outputFilterHeartOut if vd.outputFilterHeartOut < np.pi else np.pi
		#add((brf,hrf))
			
		gv.br = vd.breathingRateEst_FFT
		gv.br = gv.br if gv.br < 500 else 500
		
		gv.hr = vd.heartRateEst_FFT
		gv.hr = gv.hr  if gv.hr < 500 else 500
		
		 
		if gv.startFrame == 0:
			gv.startFrame = vt.frameNumber 
		
		brString.set("Breath:{0:.3f}".format(gv.br))
		hrString.set("Heart:{0:.3f}".format(gv.hr))
		countString.set("#{:d} {}".format(vt.frameNumber, ct - pt)) # about: 13 times
		
		d = (vt.frameNumber - gv.startFrame)
		if d != 0:
			s = "Hit rate:{:.4f}".format((float(gv.inCount)/float(d)) * 100.0)
			lRateString.set(s)
		#print("Data P {}".format(gv.hr,gv.br,vt.frameNumber, ct-pt))
		#print("Heart Rate:{:.4f} Breath Rate:{:.4f} #:{:d}  {}".format(gv.hr,gv.br,vt.frameNumber, ct-pt))
		

port.flushInput()
window.mainloop()
GPIO.cleanup()








