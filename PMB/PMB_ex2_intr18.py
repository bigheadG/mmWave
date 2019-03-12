''' 
People Movement Behavior(PMB) : 2019/3/3 13:47


**** if error founded ******
Traceback (most recent call last):
  File "PMB_ex2_intr18.py", line 74, in <module>
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
#import matplotlib.pyplot as plt
#import matplotlib.animation as animation
import numpy as np
from threading import Thread
import RPi.GPIO as GPIO
#from matplotlib.figure import Figure
import numpy as np

import datetime
from mmWave import peopleMB

from tkinter import *

#**************** GUI part ********************
window = Tk()
window.title("Welcome to People Movement Behavior Demo")
v6String = StringVar()
v6String.set("v6:")
v7String = StringVar()
v7String.set("v7:")
v8String = StringVar()
v8String.set("v8:")
countString = StringVar()
countString.set("0")

hl = Label(window, textvariable= v6String , font=("Arial Bold", 50) ).grid(sticky="W",column = 0 ,row = 0)
bl = Label(window, textvariable= v7String ,font=("Arial Bold", 50)).grid(sticky="W",column=0, row=1)
cl = Label(window, textvariable= v8String ,font=("Arial Bold", 50)).grid(sticky="W",column=0, row=2)
ll = Label(window, textvariable= countString ,font=("Arial Bold", 20)).grid(sticky="W",column=0, row=3)

class globalV:
	count = 0
	lostCount = 0
	startFrame = 0
	frame = 0
	rangeValue = 0.0
	ct = datetime.datetime.now()
	gt = datetime.datetime.now()
	def __init__(self, count):
		self.count = count
		
class v7S:
	tid = 0
	posX = 0.0
	posY = 0.0
	velX = 0.0
	velY = 0.0
	accX = 0.0
	accY = 0.0
	EC = [0.0,0.0,0.0,0.0]
	G = 0.0
		
v7A = [v7S]
		
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
	uartIntr("TEST")
	gv.count = gv.count + 1

#****** GPIO 18 for rising edge to catch data from UART ****
GPIO.setmode(GPIO.BCM)
GPIO.setup(18, GPIO.IN)
GPIO.add_event_detect(18, GPIO.RISING,my_callback)


#
#Object initail
#

pm = peopleMB.PeopleMB(port)

def v7UnpackXY(v7Data):
	print("---v7 unpack---")
	v7xy = []
	for k in v7Data:
		v7xy.append([k[1], k[2]])
	return v7xy

def v7UnpackVelocityXY(v7Data): # velocity x,y
	velxy = []
	for k in v7Data:
		velxy.append([k[3], k[4]])
	return velxy


def uartIntr(name):
	pt = datetime.datetime.now()
	#mmWave/People Movement Behavior tlvRead  
	#print(datetime.datetime.now().time())
	(dck , v6,v7,v8) = pm.tlvRead(False)
	hdr = pm.getHeader()
	gv.gt = pt
	ct = datetime.datetime.now()
		
	if dck:
		gv.count = 0 
		diff = ct-pt
		print("ID#({:d}) TLVs:{:d} [v6({:d}),v7({:d}),v8({:d})] {}".format(hdr.frameNumber,hdr.numTLVs,len(v6),len(v7),len(v8),diff))
		xy = v7UnpackXY(v7)
		#print("Position[x,y]:",xy)
		vxy = v7UnpackVelocityXY(v7)
		#print("Velocity[X,Y]:",vxy)
			
		v6String.set("V6 points:{:d}".format(len(v6)))
		v7String.set("V7 Objects:{:d}".format(len(v7)))
		v8String.set("V8 Indexs:{:d}".format(len(v8)))
		countString.set("#{:d} ex:{}".format(hdr.frameNumber, diff))
		pt = ct 


port.flushInput()
window.mainloop()
GPIO.cleanup()








