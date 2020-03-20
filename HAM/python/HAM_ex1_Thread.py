''' 
High Accuracy Measurement(HAM) : 2018/12/10 15:47


System requirement:
(1)Hardware BM101 kit mmWave Sensor
(2)Firmware: High Accuracy Measurement

'''
import serial
import time
import struct
import sys
from collections import deque
#import matplotlib.pyplot as plt
#import matplotlib.animation as animation
import numpy as np
from threading import Thread
import RPi.GPIO as GPIO
#from matplotlib.figure import Figure
import numpy as np
from mmWave import highAccuracy

import datetime
from tkinter import *

#**************** GUI part ********************
window = Tk()
window.title("Welcome to High Accuracy Measurement Demo")
hrString = StringVar()
hrString.set("Range")
brString = StringVar()
brString.set("")
countString = StringVar()
countString.set("0")

hl = Label(window, textvariable= hrString , font=("Arial Bold", 50) ).grid(column = 0 ,row = 0)
bl = Label(window, textvariable= brString ,font=("Arial Bold", 50)).grid(column=0, row=1)
cl = Label(window, textvariable= countString ,font=("Arial Bold", 50)).grid(column=0, row=2)

lRateString = StringVar()
lRateString.set("0")
ll = Label(window, textvariable= lRateString ,font=("Arial Bold", 30)).grid(column=0, row=3)

#**********************************************

class globalV:
	count = 0
	lostCount = 0
	startFrame = 0
	inCount = 0
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
	
#
#Object initail
#
gv = globalV(0)


ham = highAccuracy.HighAccuracy(port)

# UART : 50 ms
def uartThread(name):
	pt = datetime.datetime.now()
	ct = datetime.datetime.now()
	port.flushInput()
	while True:
		pt = datetime.datetime.now()
		#mmWave/High Accuracy Measurement tlvRead  
		#print(datetime.datetime.now().time())
		(dck , hd, rangeBuf) = ham.tlvRead(False)
	
		if gv.count > 3: #do the usrt flush
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
			gv.rangeValue = hd.rangeValue 
			hdr = ham.getHeader()
			print("Range:{:.4f}m #:{:d}  {}".format(gv.rangeValue,hdr.frameNumber, ct-pt))
		
			gv.frame = hdr.frameNumber
		
			if gv.startFrame == 0:
				gv.startFrame = gv.frame
		
			hrString.set("Range:{0:.3f} m".format(gv.rangeValue))
			countString.set("#{:d}".format(gv.frame)) # about: 13 times
		
			
			d = (gv.frame - gv.startFrame)
			#print("frame:{:d} startFrame:{:d}  diff:{:d} inCount:{:d}".format(gv.frame,gv.startFrame,d,gv.inCount))
			if d != 0:
				s = "Hit rate:{:.4f}".format((float(gv.inCount)/float(d)) * 100.0)
				lRateString.set(s)
			
			pt = ct 


thread1 = Thread(target = uartThread, args =("UART",))
thread1.setDaemon(True)
thread1.start()
window.mainloop()








