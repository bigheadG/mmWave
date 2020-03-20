''' 
High Accuracy Measurement(HAM) : 2018/12/10 15:47

Use gpio 18 edge detection to get sensor data


**** if error founded ******
Traceback (most recent call last):
  File "HAM_ex2_intr18.py", line xx, in <module>
    GPIO.add_event_detect(18, GPIO.RISING,my_callback)
RuntimeError: Failed to add edge detection

*** plesae use the following command to clear this error ****

~#gpio unexport 18 

System requirement:
(1)Hardware BM101 kit mmWave Sensor
(2)Firmware: High Accuracy Measurement


'''
#import os
import serial
import time
import struct
from collections import deque
#import matplotlib.pyplot as plt
#import matplotlib.animation as animation
import numpy as np
#from threading import Thread
import RPi.GPIO as GPIO
#from matplotlib.figure import Figure

import datetime
#import highAccuracy as ham
from mmWave import highAccuracy

from tkinter import *

#**************** GUI part ********************
window = Tk()
window.title("Welcome to High Accuracy Measurement Demo")
hrString = StringVar()
hrString.set("Range:")
brString = StringVar()
brString.set("")
countString = StringVar()
countString.set("0")
lRateString = StringVar()
lRateString.set("0")

hl = Label(window, textvariable= hrString ,   font=("Arial Bold", 50) ).grid(column = 0 ,row = 0)
bl = Label(window, textvariable= brString ,   font=("Arial Bold", 50)).grid(column=0, row=1)
cl = Label(window, textvariable= countString ,font=("Arial Bold", 50)).grid(column=0, row=2)
ll = Label(window, textvariable= lRateString ,font=("Arial Bold", 30)).grid(column=0, row=3)

class globalV:
	count = 0
	lostCount = 0
	inCount = 0
	startFrame = 0
	frame = 0
	rangeValue = 0.0
	ct = datetime.datetime.now()
	def __init__(self, count):
		self.count = count
		
# UART initial
try:    #pi 3
	port = serial.Serial("/dev/ttyS0",baudrate = 921600, timeout = 0.5)
except: #pi 2
	port = serial.Serial("/dev/ttyAMA0",baudrate = 921600, timeout = 0.5)

gv = globalV(0)

#*****************GPIO Setting*****************************
def my_callback(channel):
	#ct = datetime.datetime.now()
	#print("intr:{}".format(ct - gv.ct))
	uartIntr("TEST")
	gv.count = gv.count + 1

#****** GPIO 18 for rising edge to catch data from UART ****
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN)
GPIO.add_event_detect(18, GPIO.RISING,my_callback)

#
#Object initail
#

ham = highAccuracy.HighAccuracy(port)
hd  = highAccuracy.dos
 
def uartIntr(name):
	pt = datetime.datetime.now()
	#mmWave/High Accuracy Measurement tlvRead  
	#print(datetime.datetime.now().time())
	(dck , hd, rangeBuf) = ham.tlvRead(False)
	
	if gv.count > 3:
		#print("Delay:{:d}".format(gv.count))
		gv.lostCount = gv.lostCount + 1
		print("lostCount {:d}".format(gv.lostCount))
		time.sleep(0.097)
		port.flushInput()
		gv.count = 0
	#else:
		#port.flushInput()
		
		
	if dck:
		gv.count = 0 
		gv.inCount += 1
		ct = datetime.datetime.now()
		#print("data in:{}".format(ct))
		#print(":")
		gv.rangeValue = hd.rangeValue
		hdr = ham.getHeader()
		print("Range(m):{:.4f} #:{:d}  {}".format(gv.rangeValue,hdr.frameNumber, ct-pt))
		
		gv.frame = hdr.frameNumber
		
		if gv.startFrame == 0:
			gv.startFrame = gv.frame
		
		
		hrString.set("Range:{0:.3f} m".format(gv.rangeValue))
		countString.set("#{:d}".format(gv.frame)) # about: 13 times
		
		d = (gv.frame - gv.startFrame)
		if d != 0:
			s = "Hit rate:{:.4f}".format( (float(gv.inCount)/float(d)) * 100.0)
			lRateString.set(s)
		#print("Data P {}".format(gv.hr,gv.br,vts.frameNumber, ct-pt))
		pt = ct 
		
		

port.flushInput()
window.mainloop()
GPIO.cleanup()








