#================================================
# File Name: pc3d_v12_kv_FDS.py  v0.0.2
#
# Requirement:
# Hardware: BM301-ODS
# Firmware: FDS
# lib: pc3d_kv
# Plot point cloud(V6) in 3D figure
# type: key/value
# Application: Use in Fall Detect Sensing(FDS)
#
# input data: 50ms per Frame
#
# 				*****Notes*****
# This program is use matplotlib animation to develop
# the frame update is too slow. program waiting for
# improvement
#==================================================
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
from numpy.random import random

import sys
from threading import Thread
from mmWave import pc3d_kv
import serial
import struct
import datetime

#for Jetson nano UART port
port = serial.Serial("/dev/ttyTHS1",baudrate = 921600, timeout = 0.5)

pc3d = pc3d_kv.Pc3d_kv(port)

bars = []
pc3 = []

# Attaching 3D axis to the figure
fig = plt.figure()
ax = p3.Axes3D(fig)

# Setting the axes properties
border = 1

#set axes limit
ax.set_xlim3d(left=-1, right=2 ,auto = False) 
ax.set_xlabel('Z',fontsize = 16)
ax.set_ylim3d(top =-1, bottom= 2,auto = False)
ax.set_ylabel('X',fontsize = 16) 
ax.set_zlim3d(bottom=0, top=2.4 ,auto = False)
ax.set_zlabel('Y',fontsize = 16)
  
dflag = False
def uartThread(name):
	global pc3, dck , dflag
	#print("Thread::" + name)
	while True:
		(dck,pc3x) = pc3d.pc3dRead(False)
		#print(pc3x)
		if dck:
			pc3 = pc3x
			dflag = True
			'''
			for i in range(pc3.numObjs):
				print("frame:{:d} id:{:d} state:{:d} ({:.4f}:{:.4f}:{:.4f}) dx:{:.4f} dy:{:.4f} dz:{:.4f}".format(pc3.frameNum,pc3.op[i].tid,pc3.op[i].state,pc3.op[i].x,pc3.op[i].y,pc3.op[i].z,pc3.op[i].aX,pc3.op[i].aY,pc3.op[i].aZ))
			'''
			
color_values = ['b', 'g', 'y', 'c', 'm', 'r', 'k', 'w']
def animate(i,bars):
	global pc3,dflag,color_values
	
	if dflag == False:
		return
		
	if pc3.numObjs >= 0:
		
		pc3b = pc3 # to avoid pc3 data unsync with display
		bars = []
		ax.cla() #clear plot
		
		ax.set_xlim3d(2,-2) 
		ax.set_xlabel('X',fontsize = 16)
		ax.set_ylim3d(2.4,0)
		ax.set_ylabel('Y',fontsize = 16) 
		ax.set_zlim3d(-2,2)
		ax.set_zlabel('Z',fontsize = 16)
		
		try:
			spotsx  = [pc3b.op[i].x for i in range(pc3b.numObjs)]
			spotsy  = [pc3b.op[i].y for i in range(pc3b.numObjs)]
			spotsz  = [pc3b.op[i].z for i in range(pc3b.numObjs)]
		
			dx = [ 0.3  for i in range(pc3b.numObjs)]
			dy = [ 0.3  for i in range(pc3b.numObjs)]
			dz = [ 0.3  for i in range(pc3b.numObjs)]
			stateA = [pc3b.op[i].state for i in range(pc3b.numObjs)]
		
			for i in range(pc3b.numObjs):
				bars.append(ax.bar3d( spotsx[i],spotsy[i],spotsz[i], dx[i], dy[i],dz[i], color = color_values[stateA[i]]))
			
			plt.draw
		except:
			print("Except: animation")
			
	return bars

thread1 = Thread(target = uartThread, args =("UART",))
thread1.setDaemon(True)
thread1.start()
 
ani = animation.FuncAnimation(fig, animate,fargs=[bars], interval= 200)
plt.show()

