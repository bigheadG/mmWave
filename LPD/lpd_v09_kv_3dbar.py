#=======================================================================
# File Name: lpd_v09_kv_3dbar.py
#
# Requirement:
# Hardware: BM201-ISK
# Firmware: V0905_LPD
# Lib: lpdISK 
# Type: Key data 
# Baud Rate: 921600 /8 /n /1
# ALERT: Dedicated for V0905_LPD Firmware Only 
#        Not supported for V0910_LPD Firmware
#=======================================================================

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
from numpy.random import random

import sys
from threading import Thread
from mmWave import lpdISK_kv
import serial
import struct
import datetime

#for Jetson nano UART port
port = serial.Serial("/dev/ttyTHS1",baudrate = 921600, timeout = 0.5)
# for pi 3/ pi 4
#port = serial.Serial("/dev/ttyS0",baudrate =  921600, timeout = 0.5)

pc3d = lpdISK_kv.LpdISK_kv(port)

bars = []
pc3 = []

# Attaching 3D axis to the figure
fig = plt.figure()
ax = p3.Axes3D(fig)

# Setting the axes properties
border = 1

#set axes limit
ax.set_xlim3d(left=-1, right=1 ,auto = False) 
ax.set_xlabel('Z',fontsize = 16)
ax.set_ylim3d(top =-2, bottom= 2,auto = False)
ax.set_ylabel('X',fontsize = 16) 
ax.set_zlim3d(bottom=0, top=50 ,auto = False)
ax.set_zlabel('Y',fontsize = 16)
  
dflag = False
def uartThread(name):
	global pc3, dck , dflag
	#print("Thread::" + name)
	while True:
		(dck,pc3x) = pc3d.lpdRead(False)
		
		if dck:
			pc3 = pc3x
			#print(pc3)
			dflag = True
			#for i in range(pc3.numObjs):
			#	print("frame:{:d} id:{:d} state:{:d} ({:.4f}:{:.4f}:{:.4f}) dx:{:.4f} dy:{:.4f} dz:{:.4f}".format(pc3.frameNum,pc3.op[i].tid,pc3.op[i].state,pc3.op[i].x,pc3.op[i].y,pc3.op[i].z,pc3.op[i].dimX,pc3.op[i].dimY,pc3.op[i].dimZ))
			
color_values = ['b', 'g', 'y', 'c', 'm', 'r', 'k', 'w']
def animate(i,bars):
	global pc3,dflag,color_values
	'''
	if dflag == False:
		return
	'''
	if pc3.numObjs != 0:
		bars = []
		ax.cla() #clear plot
		
		ax.set_xlim3d(-10, 10) 
		ax.set_xlabel('X',fontsize = 16)
		ax.set_ylim3d(0, 50)
		ax.set_ylabel('Y',fontsize = 16) 
		ax.set_zlim3d(-5, 5)
		ax.set_zlabel('Z',fontsize = 16)
		'''
		ax.set_xlim3d(left=-20, right=20,auto = False) 
		ax.set_xlabel('Z',fontsize = 16)
		ax.set_ylim3d(top =-2, bottom= 2,auto = False)
		ax.set_ylabel('X',fontsize = 16) 
		ax.set_zlim3d(bottom=0, top= 50 ,auto = False)
		ax.set_zlabel('Y',fontsize = 16)
		'''
		spotsx  = [pc3.op[i].x for i in range(pc3.numObjs)]
		spotsy  = [pc3.op[i].y for i in range(pc3.numObjs)]
		spotsz  = [pc3.op[i].z for i in range(pc3.numObjs)]
		
		dx = [ 0.3  for i in range(pc3.numObjs)]
		dy = [ 0.6 for i in range(pc3.numObjs)]
		dz = [ 0.3  for i in range(pc3.numObjs)]
		stateA = [pc3.op[i].state for i in range(pc3.numObjs)]
		
		for i in range(pc3.numObjs):
			bars.append(ax.bar3d( spotsz[i],spotsx[i],spotsy[i], dz[i], dx[i],dy[i], color = color_values[stateA[i]]))
			
		plt.draw
	return bars

thread1 = Thread(target = uartThread, args =("UART",))
thread1.setDaemon(True)
thread1.start()
 
ani = animation.FuncAnimation(fig, animate,fargs=[bars], interval=120)
plt.show()

