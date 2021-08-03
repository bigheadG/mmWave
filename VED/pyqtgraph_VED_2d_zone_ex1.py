#=============================================
# File Name: pyqtgraph_VED_2d_zone_ex1.py
#
# Requirement:
# Hardware: BM201-ISK or BM501-AOP
# Firmware: 
# config file: 
# lib: vehicleODR
# radar installation: wall momunt
#
# plot tools: pyqtgraph
# Plot Target (V8) in 2D figure
# 
# Vital Energy Detection(VED)
# type: Raw data
# Baud Rate: playback: 119200
#			 real time: 921600
#=============================================

from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph as pg
import numpy as np
from mmWave import vehicleODR
import serial
from threading import Thread

#################################################################

#=====================xy scatter
win = pg.GraphicsWindow()
win.resize(600,600)
#pg.setConfigOption('background', 'w')
pg.setConfigOption('foreground', 'y')
 
win.setWindowTitle('xy occupation')
w0 = win.addPlot()
w0.setRange(xRange=[0,47],yRange= [0,63])
w0.setLabel('bottom', 'V8 HeatMap', '0~47')
w0.setLabel('left', 'Grid', '0~63')
spots0 = []
curveS0 = pg.ScatterPlotItem(size = 10, pen=pg.mkPen('w'), pxMode=True) #pg.ScatterPlotItem(pxMode=True)   ## Set pxMode=False to allow spots to transform with the view
w0.addItem(curveS0)




##################### 2d diagram update ################################ 

def updateWF():
	global x,y,v8A,sensorA,curveS0
	curveS0.setData(x=sensorA[:,0],y=sensorA[:,1], pen = 'g', symbol='s')
	#curveS0.setData(x=sensorA[:,0],y=sensorA[:,1], pen= sensorA[:,2], symbol='s')


#
#****************** use USB-UART ************************************
#
#port = serial.Serial("/dev/ttyUSB0",baudrate = 921600, timeout = 0.5)
#
#for Jetson nano UART port
#port = serial.Serial("/dev/ttyTHS1",baudrate = 921600, timeout = 0.5) 
#
#for pi 4 UART port
#port = serial.Serial("/dev/ttyS0",baudrate = 921600, timeout = 0.5)
#
#Drone Object Detect Radar initial 
#port = serial.Serial("/dev/tty.usbmodemGY0052534",baudrate = 921600, timeout = 0.5)
#port = serial.Serial("/dev/tty.usbmodem14103",baudrate = 115200 , timeout = 0.5)  
#port = serial.Serial("/dev/tty.usbmodemGY0050674",baudrate = 921600, timeout = 0.5)  
#port = serial.Serial("/dev/tty.SLAB_USBtoUART3",baudrate = 921600, timeout = 0.5)  
#port = serial.Serial("/dev/tty.usbmodemGY0043914",baudrate = 921600, timeout = 0.5)
 
port = serial.Serial("/dev/tty.usbmodemGY0043864",baudrate = 921600, timeout = 0.5)  

#for NUC ubuntu 
#port = serial.Serial("/dev/ttyACM1",baudrate = 921600, timeout = 0.5)

radar = vehicleODR.VehicleODR(port)

v8len = 0
v9len = 0
v10len = 0

 

def jb_mapF32(inp, xMin, xMax, yMin, yMax):
	slope = (yMax - yMin) / (xMax - xMin)
	return (inp - xMin) * slope + yMin
	 
def jb_sigmod(inp, gain, threshold):
	x = gain * (inp - threshold)
	return inp * (1 / (1 + np.exp(-x)))

def jb_charge(inp, tau):
	return 1 - np.exp(-inp / tau)

def jb_chargeKnee(inp, tau, knee):
	inp[inp < knee] = 0
	return 1 - np.exp(-inp / tau)

def jb_normalDistribute(inp, gain, mean, sigma):
	x = (inp - mean) / sigma
	return inp * np.exp(-x*x/2.0) * gain

def jb_limiter(inp, xMin, xMax, yMin, yMax):
	return jb_mapF32(inp, xMin, xMax, yMin, yMax)

v8A = []
sensorA = []
def update():    
	global v8A
	if len(v8A) == 3072:
		#print("======updateWF==================:{:}".format(len(v8A)))
		updateWF()

np.set_printoptions(threshold=np.inf,precision=3,suppress=True) 

t = QtCore.QTimer()
t.timeout.connect(update)
t.start(150)

fn = 0 
prev_fn = 0

def radarExec():
	global v9len,v10len,v8len,flag,v8A,sensorA

	v8 = []
	v9 = []
	v10 = []
	flag = True
	(dck,v8,v9,v10) = radar.tlvRead(False)
	
	if  dck: 
		v8len = len(v8)
		v9len = len(v9)
		v10len = len(v10)
		
		if v8len != 0:
			#print("Sensor Data: [v8,v9,v10]:[{:d},{:d},{:d}]".format(v8len,v9len,v10len))
			
			#
			#(1) data normalize and filter out unwant data
			# input data => (filter + normalize) 
			#
			'''
			vs2 = np.log(v8) #np.sqrt(np.sqrt(v8))
			print("===> Normalized={:.2f}, {:.2f}".format(max(v8), min(v8)))
			v8A = (vs2 /  np.linalg.norm(vs2)) * 100.0
			
			'''
			vs = np.array(v8)
			vs = jb_mapF32(vs, 0.0, 32000.0/ 4.0, 0.0, 2.8)
			
			#vs = jb_sigmod(vs, 2.0, 32000.0 / 10000.0)
			jb_gain = 40.0 * 10000000
			jb_mean = 0.0
			vs = jb_normalDistribute(vs, jb_gain, jb_mean, 32000.0 / 2000.0)
			jb_limitValue = 1.0
			vs = jb_limiter(vs, 0, jb_gain, 0, jb_limitValue) 
			
			# for higher sensitivity tune lower tao, default 0.05 
			tau  = 0.060 # default 0.050
			knee = 0.005 / 16.0 # default 0.005
			vsc = jb_chargeKnee(vs, tau, knee)
			
			#
			#(2) remove unwant data 
			#
			xx = [ jb_limitValue if vsc[i] > jb_limitValue-0.2 else 0 for i in range(len(vsc))]
			xxe = np.array(xx) #[0::2])
			xr = xxe.reshape(64,48)
			d = sortByLimitXY(jb_limitValue,xr)
			 
			#
			#(3)setup the zone location
			# 	mask: true  => only show data locate in zone
			# 	mask: false => show all point data 
			#
			mask = True 
			if len(d) > 0:
				sensorA0 = np.array(d)
				#
				# Add Zone here
				#
				(zoneA0 , ratio0) = pointsInZone( 9,35,42,51,sensorA0,'b')
				(zoneA1 , ratio1) = pointsInZone(20,40,30,40,sensorA0,'r')
				
				if mask == True:
					sensorA = np.array(zoneA0 + zoneA1)
				else:
					sensorA = np.array(d)
					
				print("ratio0:{:} ratio1:{:}".format(ratio0,ratio1)) 
				
			
			#print(vs) 
			v8A = vs
			 
			
		
	port.flushInput()


#==========================================
#
# input: pointCloud
# square Zone: x_lo,x_hi, y_lo,y_hi 
# 
# output: (pointsArray, ratio)
#
def pointsInZone(x_lo,x_hi,y_lo,y_hi,pointCloud,color):
	pc = pointCloud
	zone = (y_hi - y_lo) * (x_hi - x_lo)
	pointA = []
	print("-----pointInZone-----------")
	for i in pc:
		if i[0] >= x_lo and i[0] <= x_hi: #range : x(Height)
			if i[1] >= y_lo and i[1] <= y_hi: # (y)Bed width about:80 cm
				pointA.append([i[0],i[1],'g'])  #pg.intColor(i, v1len)
	inPoint = len(pointA)
	if zone > 0: 
		ratio = len(pointA) / zone
	else:
		ratio = 0
	
	for i in range(x_lo,x_hi+1,1):
		pointA.append([i,y_hi,color])
		pointA.append([i,y_lo,color])
		
	for i in range(y_lo,y_hi+1,1):
		pointA.append([x_hi,i,color])
		pointA.append([x_lo,i,color])
		
	return (pointA, ratio)

#
#  get zA: Matrix data
#  and filter out data under limit
#
def sortByLimitXY(limit,zA):
	ptsA = []
	for i in range(len(zA)): 
		d = zA[i]
		for j in range(len(zA[i])):
			if d[j] >= limit:
				ptsA.append([float(j),float(i),d[j]])
	return ptsA
	
	
		 
def uartThread(name):
	port.flushInput()
	while True:
		radarExec()
					
thread1 = Thread(target = uartThread, args =("UART",))
thread1.setDaemon(True)
thread1.start()

## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore,'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
