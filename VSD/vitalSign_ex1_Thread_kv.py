''' 
vital: Vital Signs : 2020/10/20

'''
import serial
import time
import struct
import sys
from collections import deque
import numpy as np
from threading import Thread
import numpy as np
from mmWave import vitalsign_kv
#import vitalsign_kv 

from tkinter import *

#**************** GUI part ********************
window = Tk()
window.title("Welcome to Vital Sign Demo")
hrString = StringVar()
hrString.set("Heart Rate")
brString = StringVar()
brString.set("Breath Rate")
statusString = StringVar()
statusString.set("0")

hl = Label(window, textvariable= hrString , font=("Arial Bold", 50) ).grid(column = 0 ,row = 0)
bl = Label(window, textvariable= brString ,font=("Arial Bold", 50)).grid(column=0, row=1)
cl = Label(window, textvariable= statusString ,font=("Arial Bold", 35)).grid(column=0, row=2)

#**********************************************

		
#UART initial
'''
try:    #pi 3
	port = serial.Serial("/dev/ttyS0",baudrate = 115200, timeout = 0.5)
except: #pi 2
	port = serial.Serial("/dev/ttyAMA0",baudrate = 115200, timeout = 0.5)
'''
#for MAC
#port = serial.Serial("/dev/cu.usbmodemGY0043914",baudrate = 115200, timeout = 0.5)
#

#for Jetson Nano
#port = serial.Serial("/dev/ttyTHS1",baudrate = 115200, timeout = 0.5)

#for NUC
#port = serial.Serial("/dev/ttyACM1",baudrate = 115200, timeout = 0.5)

#for pc
#port = serial.Serial("COM5",baudrate = 115200, timeout = 0.5)

#
#Object initail
#

def labelString(idx):
	if idx == 0:
		return "None"
	elif idx == 1:
		return "Stable"
	elif idx == 2:
		return  "Movement"
	elif idx == 3:
		return "Alert"
	else:
		return "None"


vts = vitalsign_kv.VitalSign_kv(port)
 
# UART : 50 ms
def uartThread(name):
	port.flushInput()
	while True:
		#mmWave/VitalSign tlvRead & Vital Sign 
		
		(dck , vd) = vts.tlvRead(False)
		
		if dck:
			print("Status:{}  {}".format(vd[6],labelString(vd[6])))
			print("Breath Rate:{:}  Heart Rate:{:} Breath Phase:{:} Heart Phase:{:}".format(vd[2],vd[3],vd[4],vd[5]))
			if vd[6] == 0:
				brString.set("Empty")
				hrString.set("")
			elif vd[6] == 3:
				brString.set("Breath:0")
				hrString.set("Heart: 0")
			else:
				brString.set("Breath:{0:.2f}".format(vd[2]))
				hrString.set("Heart:{0:.2f}".format(vd[3]))
				
			statusString.set("{} : {}".format(vd[6],labelString(vd[6])))
			port.flushInput()
 

thread1 = Thread(target = uartThread, args =("UART",))
thread1.setDaemon(True)
thread1.start()

window.mainloop()








