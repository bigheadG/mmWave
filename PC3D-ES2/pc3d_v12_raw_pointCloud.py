#=============================================
# File Name: pc3d_v12_pointCloud.py
#
# Requirement:
# Hardware: BM301-
# Firmware: FDS
# lib: pc3d
# Plot point cloud(V6) in 3D figure 
# type: Raw data
#
# 				*****Notes*****
# This program is use matplotlib animation to develop
# the frame update is slow. program waiting for
# improvement
#=============================================
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import mpl_toolkits.mplot3d.axes3d as p3
import matplotlib.animation as animation
from numpy.random import random
import sys
from threading import Thread
from mmWave import pc3d
import serial
import struct
import datetime

#pi 3 or pi 4
#port = serial.Serial("/dev/ttyS0",baudrate = 921600, timeout = 0.5)
#for Jetson nano UART port
port = serial.Serial("/dev/ttyTHS1",baudrate = 921600, timeout = 0.5)


pc3d = pc3d.Pc3d(port)
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
 
v6 = []
dflag = False
pcNum = 0

def uartThread(name):
	global pc3, dck , dflag,pcNum
	#print("Thread::" + name)
	while True:
		(dck,v6,v7,v8)  = pc3d.tlvRead(False)
		if dck and (len(v6) != 0) :
			pc3 = v6 
			#print(v6)
			pcNum = len(pc3)
			#print("point cloud:{:d}".format(pcNum))
			dflag = True
			
color_values = ['b', 'g', 'y', 'c', 'm', 'r', 'k', 'w']

def animate(i,bars):
	global pc3,dflag,color_values,pcNum
	
	if dflag == False:
		return
		
	if len(pc3) != 0:
		
		ax.cla() #clear plot
		ax.set_xlim3d(-4,4) 
		ax.set_xlabel('X',fontsize = 16)
		ax.set_ylim3d(-4,4)
		ax.set_ylabel('Y',fontsize = 16) 
		ax.set_zlim3d(-4,4)
		ax.set_zlabel('Z',fontsize = 16)
		
		cnt = len(pc3)
		
		spotsz  = [(pc3[i][3] * np.sin(pc3[i][0])) for i in range(cnt)]
		spotsx  = [(pc3[i][3] * np.cos(pc3[i][0]) * np.sin(pc3[i][1])) for i in range(cnt)]
		spotsy  = [(pc3[i][3] * np.cos(pc3[i][0]) * np.cos(pc3[i][1])) for i in range(cnt)]
		
		ax.scatter(spotsx, spotsy, spotsz, c='b', marker='o')		
		plt.draw
	return bars

thread1 = Thread(target = uartThread, args =("UART",))
thread1.setDaemon(True)
thread1.start()
 
ani = animation.FuncAnimation(fig, animate,fargs=[bars], interval=120)
plt.show()
