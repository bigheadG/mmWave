#=============================================
# File Name: TMD_ex2_pointCloud.py
#
# Requirement:
# Hardware: BM201-ISK
# Firmware: TMD
# lib: trafficMD
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

from mmWave import trafficMD
import serial
import struct
import datetime

#pi 3 or pi 4
#port = serial.Serial("/dev/ttyS0",baudrate = 921600, timeout = 0.5)
#for Jetson nano UART port
#port = serial.Serial("/dev/ttyTHS1",baudrate = 921600, timeout = 0.5)

port = serial.Serial("/dev/tty.usbmodemGY0052854",baudrate = 921600, timeout = 0.5)


pc3d = trafficMD.TrafficMD(port)

bars = []
pc3 = []
pc3_ti = []
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
	global pc3,dck,dflag,pcNum,pc3_ti
	#print("Thread::" + name)
	while True:
		(dck,v6,v7,v8,v9)  = pc3d.tlvRead(False)
		if dck and (len(v6) != 0) :
			pc3 = v6
			pc3_ti = v8
			#print("v6={:d} v7={:d} v8={:d} v9={:d}".format(len(v6),len(v7),len(v8),len(v9)))
			#pcNum = len(pc3)
			#print("point cloud:{:d}".format(pcNum))
			dflag = True
			
color_values = ['g', 'b', 'r', 'c', 'm', 'o', 'k', 'b']

def color_map(val):
	if val == 253:
		return 'gray'
	elif val == 254:
		return 'gray'
	elif val == 255:
		return 'gray'
	else:
		return 'r'


def animate(i,bars):
	global pc3,pc3_ti,pc3_tg, dflag,color_values,pcNum
	
	if dflag == False:
		return
		
	if len(pc3) != 0 and len(pc3_ti) == len(pc3):
		ax.cla() #clear plot
		ax.set_xlim3d(-50,50) 
		ax.set_xlabel('X',fontsize = 16)
		ax.set_ylim3d(-50,50)
		ax.set_ylabel('Y',fontsize = 16) 
		ax.set_zlim3d(-50,50)
		ax.set_zlabel('Z',fontsize = 16)

		cnt = len(pc3)
		spotsz  = [(pc3[i][0] * np.sin(pc3[i][2])) for i in range(cnt)]
		spotsx  = [(pc3[i][0] * np.cos(pc3[i][2]) * np.sin(pc3[i][1])) for i in range(cnt)]
		spotsy  = [(pc3[i][0] * np.cos(pc3[i][2]) * np.cos(pc3[i][1])) for i in range(cnt)]
		color_s = [color_map(pc3_ti[i]) for i in range(cnt)]
		#print(pc3_ti)
		
		ax.scatter(spotsx, spotsy, spotsz, c = color_s, marker='+')
		plt.draw
	return bars

thread1 = Thread(target = uartThread, args =("UART",))
thread1.setDaemon(True)
thread1.start()
 
ani = animation.FuncAnimation(fig, animate,fargs=[bars], interval=120)
plt.show()
