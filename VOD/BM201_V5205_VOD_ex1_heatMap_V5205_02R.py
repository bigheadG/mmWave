########################################################################
# File: BM201_V5205_VOD_ex1_heatMap_V5205_02R.py
# Hardware BM201, FW V5205_VOD, SW V5205.02
########################################################################
# VOD: Vehicle Occupant Detection
# VOD: Y: Range 0~3m [0..64]
#      X: Range: (-60deg ~ +60deg) [0..48]
# UART Baud Rate: 921600
########################################################################
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time
import serial
from mmWave import vehicleODR
import sys
from threading import Thread
import math # for pi

#UART initial
#Jetson nano
#port = serial.Serial("/dev/ttyTHS1",baudrate = 921600, timeout = 0.5)
#raspberry pi 4
#port = serial.Serial("/dev/ttyS0",baudrate = 921600, timeout = 0.5)

# for INTEL NUC, 
# in case USB port had been changed,  
# please try to change the setting by selecting one of '/dev/ttyACM1' and '/dev/ttyACM2' 
# and set enable permission by command of 'sudo chmod 777 /dev/ttyACM*' 
port = serial.Serial("/dev/ttyACM1",baudrate = 921600, timeout = 0.5)

##########################################################
# global definition section
JB_VERSION_TITLE = '\nJB> VOD H/W: V52.05; S/W: V5205.02; DATE: 2021.01.05'
# here zone area deinfed as [r, dr, a, da] to 
# form a rectangular by points pair of (r,a) and (r + dr, a + da) in diagonal manner
JB_ZONE_A = [[9, 10, 8, 14],[9, 10, 26, 14],
			[24, 10, 8, 14],[24, 10, 26, 14],
			[9, 10, 8, 32],[24, 10, 8, 32]]  
# above: the last two zones be reserved did NOT be used here
JB_ZONE_NUM_4 = 4
# (5204.04) flip zone index
JB_PLOT_FLIP_ZONE_INDEX = [1, 0, 3, 2, 4, 5] # for plot flip, means swap zone index (0, 1) and (2, 3)  
JB_COLOR_YELLOW = 1.00
JB_COLOR_DARKBLUE = 0.10
JB_PTH_600 = 600 # you may set this power threshold, set lower value more sensitivity
JB_RANGE_GRID_64 = 64
JB_AZIMUTH_GRID_48 = 48
JB_V8_MAX_VALUE_32000 = 32000 # this value is observed in real case
##########################################################

##########################################################################################
# callng: jb_plotLine(jb_heatA, [[9, 8], [17, 8], jb_color) 
def jb_plotLine(jb_heatA, pointA, pointB, jb_color):
	# callng: jb_plotLine(jb_heatA, [9, 8], [17, 8], jb_color) 
	if pointA[1] == pointB[1]:
		for i in range(pointB[0] - pointA[0] + 1):
			jb_heatA[pointA[0] + i][pointB[1]] = jb_color
	# callng: jb_plotLine(jb_heatA, [17, 8], [17, 24], jb_color) 
	if pointA[0] == pointB[0]:
		for i in range(pointB[1] - pointA[1] + 1):
			jb_heatA[pointA[0]][pointA[1] + i] = jb_color
	return jb_heatA
##########################################################################################

##########################################################################################
# syntax: jb_plotZone(heatA, [r, dr, a, da], jb_color) 
# callng: jb_plotZone(heatA, [9, 10, 8, 14], 0.25) 
def jb_plotZoneAtom(jb_heatA, jb_zone, jb_color):
	r  = jb_zone[0]
	dr = jb_zone[1]
	a  = jb_zone[2]
	da = jb_zone[3]
	# plot line segments to form as rectangular zone
	for i in range(len(jb_zone)):
		# plot line segment 1: (r, a) to (r + dr, a)  
		jb_heatA = jb_plotLine(jb_heatA, [r, a], [r + dr, a], jb_color) 
		# plot line segment 2: (r + dr, a) to (r + dr, a + da)  
		jb_heatA = jb_plotLine(jb_heatA, [r + dr, a], [r + dr, a + da], jb_color) 
		# plot line segment 3: (r + dr, a) to (r + dr, a + da)  
		jb_heatA = jb_plotLine(jb_heatA, [r, a], [r, a + da], jb_color) 
		# plot line segment 4: (r, a + da) to (r + dr, a + da)  
		jb_heatA = jb_plotLine(jb_heatA, [r, a + da], [r + dr, a + da], jb_color) 		
	return jb_heatA
##########################################################################################

##########################################################################################
# put define zones here
def jb_plotZoneDefault(jb_heatA):
	for jb_zoneIndex in range(JB_ZONE_NUM_4):
		jb_heatA = jb_plotZoneAtom(jb_heatA, JB_ZONE_A[jb_zoneIndex], JB_COLOR_DARKBLUE)
	return jb_heatA
##########################################################################################

##########################################################################################
# topics: on {target in selected zone} return true
# syntax: jb_isTargetInZone(jb_v10, jb_zoneA, jb_zoneIndex)
# calling: jb_isTargetInZone(v10, JBG_zoneA, 0)
def jb_isTargetInZone(jb_v10, jb_zoneA, jb_zoneIndex):
	# set power threthold value as 5000
	percent = jb_v10[jb_zoneIndex][0]
	P = jb_v10[jb_zoneIndex][1]
	R = jb_v10[jb_zoneIndex][2]
	A = jb_v10[jb_zoneIndex][3]
	r  = jb_zoneA[jb_zoneIndex][0]
	dr = jb_zoneA[jb_zoneIndex][1]
	a  = jb_zoneA[jb_zoneIndex][2]
	da = jb_zoneA[jb_zoneIndex][3]
	# [R, A] in jb_zone
	print('JB> show: (zoneIndex, R, A; r, dr, a, da, power)='
			'({:02d},{:02d},{:02d};{:02d},{:02d},{:02d},{:02d}, {:5.1f}K)'
			.format(jb_zoneIndex, R,A, r, dr, a, da, P/1000))	
	if P >= JB_PTH_600: 
		if (R >= r) and (R <= (r + dr)) and (A >= a) and (A <= (a + da)):
			return True
	else:
		return False
##########################################################################################

##########################################################################################
# topics: on {target in zone and power over threshold} high light zone boder in yellow color
# syntax:  jb_plotZoneHighLight(jb_heatA, jb_v10):
# calling: heatA= jb_plotZoneHighLight(heatA, v10):
def jb_plotZoneHighLight(jb_heatA, jb_v10):
	#print('JB> calling jb_plotZoneHighLight()')
	for jb_zoneIndex in range(JB_ZONE_NUM_4):
		# (5204.04) consider plot with zone flip
		jb_zone = JB_ZONE_A[JB_PLOT_FLIP_ZONE_INDEX[jb_zoneIndex]]
		if jb_isTargetInZone(jb_v10, JB_ZONE_A, jb_zoneIndex):
			# (5204.05) set zone boder color is function of target power rate in related zone
			P = jb_v10[jb_zoneIndex][1]
			if P <= JB_PTH_600: 
				jb_color = jb_mapF32(P, 0, JB_PTH_600, JB_COLOR_DARKBLUE, 0.25)
			else:
				jb_color = jb_mapF32(P, JB_PTH_600, JB_PTH_600 * 10, 0.25, JB_COLOR_YELLOW) 
			jb_heatA = jb_plotZoneAtom(jb_heatA, jb_zone, jb_color)
		else:
			jb_heatA = jb_plotZoneAtom(jb_heatA, jb_zone, JB_COLOR_DARKBLUE)
	return jb_heatA
##########################################################################################

##########################################################################################
# topics: on {target in zone and power over threshold} high light target dot location in yellow color
# syntax:  jb_plotTagetHighLight(jb_heatA, jb_v10):
# calling: heatA= jb_plotTargetHighLight(heatA, v10):
def jb_plotTargetHighLight(jb_heatA, jb_v10):
	for jb_zoneIndex in range(JB_ZONE_NUM_4):
		P = jb_v10[jb_zoneIndex][1]
		R = jb_v10[jb_zoneIndex][2]
		# (5204.05) consider the location flip
		A = (JB_AZIMUTH_GRID_48 - 1) - jb_v10[jb_zoneIndex][3] # 0..47
		if P >= JB_PTH_600:
			# set high light value to location of jb_heatA
			jb_heatA[R][A] = JB_COLOR_YELLOW
	return jb_heatA
##########################################################################################

##########################################################################################
# syntax:  jb_yOutF32= jb_mapF32(jb_xInF32, jb_xMinF32, jb_xMaxF32, jb_yMinF32, jb_yMaxF32)
# calling: 50= jb_mapF32(5, 0, 10, 0, 100)
def jb_mapF32(jb_xInF32, jb_xMinF32, jb_xMaxF32, jb_yMinF32, jb_yMaxF32):
	slopeF32 = float((jb_yMaxF32 - jb_yMinF32)) / float((jb_xMaxF32 - jb_xMinF32)) 
	jb_yOutF32 = (jb_xInF32 - jb_xMinF32) * slopeF32 + jb_yMinF32 
	return jb_yOutF32
##########################################################################################

##########################################################################################
# topics:  trasfer input value to output value within 0.0 to 1.0, martrix in 64 x 48 
# syntax:  jb_heatA= jb_standardV8ToHeatMap(jb_v8)
# calling: heatA= jb_standardV8ToHeatMap(v8)
def jb_standardV8ToHeatMap(jb_v8): 
	for i in range(len(jb_v8)):
		jb_v8[i] = jb_mapF32(jb_v8[i], 0, JB_V8_MAX_VALUE_32000, 0.0, 1.0)
	jb_heatA = np.array(jb_v8).reshape((JB_RANGE_GRID_64, JB_AZIMUTH_GRID_48))
	return jb_heatA
##########################################################################################
  
##########################################################################################
# topics: show v10 in format of (zoneIndex, percent, Range, Azimuth, Power)
def jb_showV10(jb_v10):
	for jb_zoneIndex in range(JB_ZONE_NUM_4):
		percent = jb_v10[jb_zoneIndex][0] * 100 # %0 .. 100%
		P = jb_v10[jb_zoneIndex][1] / 1000 # show power in K uint
		R = jb_v10[jb_zoneIndex][2] # 0..63
		A = (JB_AZIMUTH_GRID_48 - 1) - jb_v10[jb_zoneIndex][3] # 0..47
		# for easy reading swap parameters in order of (0 2 3 1)
		print('    v10[{}]=({:3.0f}%), R=({:2d}), A=({:2d}), P=({:6.1f}K)'
				.format(jb_zoneIndex, percent, R, A, P))
##########################################################################################

##########################################################################################
def jb_uartThreadCB(name):
	global heatA
	cnt = 0
	port.flushInput()
	#pm.useDebug(False)
	#pm.stateMachine(True)
	#pm.checkTLV(True)
	JBG_flow = 0
	while True:
		(dck,v8,v9,v10) = pm.tlvRead(False)
		if dck:
			###############################################################################			
			# (5204) new codes insert here
			print(JB_VERSION_TITLE)
			# (5204.05) standard v8 vector to heapMap
			heatA = jb_standardV8ToHeatMap(v8)
			JBG_flow = JBG_flow + 1
			print('JB> flow=({:06d}), heatA sum=({:6.1f})'.format(JBG_flow, sum(sum(heatA))))
			# (5204.01) added flip azimuth left and right view for easy reading 
			heatA = np.flip(heatA, 1)  
			# (5204.02) added zones 
			heatA = jb_plotZoneDefault(heatA) 
			# (5204.03) added zones with high light boder
			heatA = jb_plotZoneHighLight(heatA, v10) 
			# (5204.05) added target location with high light color (ALERT: color is function of power)
			hearA = jb_plotTargetHighLight(heatA, v10)
			# show v10 array for easy coding
			print("JB> flow=({:06d}), v8:len=({:04d}), v9=({:04d}), v10=({:04d})".
					format(JBG_flow, len(v8),len(v9),len(v10)))
			#jb_showV10(v10) # parameters [percent, P, R, A] 
			###############################################################################			

			#print(v9)     
			#print(v10)
			#pm.headerShow()
			port.flushInput()
##########################################################################################

##########################################################################################
def jb_animateCB(xdata, im):
	global heatA
	im.set_data(heatA)
##########################################################################################
    
##########################################################################################
pm = vehicleODR.VehicleODR(port)
heatA = np.zeros((JB_RANGE_GRID_64, JB_AZIMUTH_GRID_48))

thread1 = Thread(target = jb_uartThreadCB, args =("UART",))
thread1.setDaemon(True)
thread1.start()

fig, ax = plt.subplots()
im = ax.imshow(np.random.rand(JB_RANGE_GRID_64, JB_AZIMUTH_GRID_48), interpolation= 'nearest' )
ani = animation.FuncAnimation(fig, jb_animateCB, interval=200, repeat=True, fargs=(im, ))
plt.show()
##########################################################################################
