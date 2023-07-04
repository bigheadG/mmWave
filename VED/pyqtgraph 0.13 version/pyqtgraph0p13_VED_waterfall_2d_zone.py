#=============================================
# File Name: pyqtgraph_VED_waterfall_2d_zone.py
#
# Requirement:
# Hardware: BM201-ISK or BM501-AOP
# Firmware: 
# config file: 
# lib: vehicleODR
# radar installation: wall momunt
#
# plot tools: pyqtgraph
# Plot Target (V8) in 3D figure
# Plot
# Vital Energy Detection(VED)
# type: Raw data
# Baud Rate: playback: 119200
#			 real time: 921600
#=============================================

#pyqtgraph 0.13 version
from PyQt5 import QtGui, QtWidgets, QtCore  
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from pyqtgraph.Qt import mkQApp, QtGui

'''
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import pyqtgraph as pg
'''

import numpy as np
from mmWave import vehicleODR
#import vehicleODR

import serial
from threading import Thread

from datetime import date,datetime,time
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler


class CustomTextItem(gl.GLGraphicsItem.GLGraphicsItem):
	def __init__(self, X, Y, Z, text):
		gl.GLGraphicsItem.GLGraphicsItem.__init__(self)
		self.text = text
		self.X = X
		self.Y = Y
		self.Z = Z

	def setGLViewWidget(self, GLViewWidget):
		self.GLViewWidget = GLViewWidget

	def setText(self, text):
		self.text = text
		self.update()

	def setX(self, X):
		self.X = X
		self.update()

	def setY(self, Y):
		self.Y = Y
		self.update()

	def setZ(self, Z):
		self.Z = Z
		self.update()

	def paint(self):
		self.GLViewWidget.qglColor(QtCore.Qt.cyan)
		self.GLViewWidget.renderText(round(self.X), round(self.Y), round(self.Z), self.text)


#################################################################


st = datetime.now()
sim_startFN = 0
sim_stopFN = 0

################### Real Time or read from file switch ************
rtSwitch = True # real time mode
# rtSwitch = False  # read data from file

#app = QtGui.QApplication([])
app = QtWidgets.QApplication([]) #pyqtgraph 0.13 version
  
##################### init Water fall frame ##############################
traces = dict()
wf = gl.GLViewWidget()
wf.opts['distance'] = 40
wf.setWindowTitle('VED waterfall')
wf.setGeometry(0, 50, 500, 400)
wf.show()

'''
gx = gl.GLGridItem()
gx.rotate(90, 0, 1, 0)
#gx.translate(-10, 0, 0)
gx.translate(-10, 0, 10)
wf.addItem(gx)
'''

gy = gl.GLGridItem()
gy.rotate(90, 1, 0, 0)
gy.translate(0, -48, 15)
gy.setSize(48, 36)
gy.setSpacing(1, 1)

wf.addItem(gy)

gz = gl.GLGridItem()
gz.translate(0, -18, 0)
gz.setSize(48, 66)
gz.setSpacing(1, 1)

wf.addItem(gz)

'''
gy = gl.GLGridItem()
gy.rotate(90, 1, 0, 0)
gy.translate(0, -48, 10)
gy.setSize(48, 24)
gy.setSpacing(1, 1)

wf.addItem(gy)

gz = gl.GLGridItem()
gz.translate(0, -18, 0)
gz.setSize(48, 66)
gz.setSpacing(1, 1)

wf.addItem(gz)
'''

#=====================xy scalter
#win = pg.GraphicsWindow()
win = pg.GraphicsLayoutWidget(show=True) #for pyqrgraph 0.13 verison
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




######### for traces initial ##############################
n = 200
m = 200
y = np.linspace(-10, 10, n)
x = np.linspace(-10, 10, m)

phase = 0

yA = np.zeros(48)
xA = np.linspace(-24, 24, 48)

for i in range(n):
	yi = np.array([y[i]] * m)
	d = np.sqrt(x ** 2 + yi ** 2)
	z = 10 * np.cos(d + phase) / (d + 1)
	pts = np.vstack([x, yi, z]).transpose()
	#shader='heightColor', computeNormals=False, smooth=False
	traces[i] = gl.GLLinePlotItem(pos=pts, color=(0,0,0,0), width=(i + 1) / 10, antialias=True)
	wf.addItem(traces[i])

########## set data for 3d plot ####################

def set_plotdata(name, points, color, width):
	traces[name].setData(pos=points, color=color, width=width)

##################### water fall & 2d diagram update ################################ 

def updateWF():
	global x,y,v8A,sensorA,curveS0
	if len(v8A) != 3072:
		return
	np.set_printoptions(precision=2)
	zA = np.array(v8A).reshape(64,48)
	#print(zA)
	for i in range(len(zA)):
		pts = np.vstack((xA,yA+ float(i) - 48.0,zA[i])).transpose()
		col = np.zeros((48,4))
		for j in range(48):
			#col[j] = colorMapping(j)
			col[j] = colorMapping(zA[i,j])
			#col[j] = colorMapping(yy[j])
		set_plotdata(name=i, points=pts,color= col,width= 3.0)
	#print("-----------------updateWF-------------------")
	
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
port = serial.Serial("COM15",baudrate = 921600, timeout = 0.5)  

#for NUC ubuntu 
#port = serial.Serial("/dev/ttyACM1",baudrate = 921600, timeout = 0.5)

radar = vehicleODR.VehicleODR(port)

v8len = 0
v9len = 0
v10len = 0

def colorMapping(inp):
	#print(inp)
	cx = (0,0,1,1)
	if inp < 0.2:
		cx = (0, 0, 0.7, 0.8) # blue
	elif inp >= 0.2 and inp < 0.6:
		cx = (0, 0, 1, 1)
	elif inp >= 0.6 and inp < 1.4:
		cx = (0,0.13,0.78,1)
	elif inp >= 1.4 and inp < 2.0:
		cx = (0,0.78,0,1)
	elif inp >= 2.0 and inp < 2.8:
		cx = (1,0.5,0,1)
	else: # R 20
		cx = (1,0,0,1)
	return cx


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
	global v9len,v10len,v8len,prev_fn,flag,uFlag,fn,v8A,sensorA

	v8 = []
	v9 = []
	v10 = []
	flag = True
	(dck,v8,v9,v10) = radar.tlvRead(False)
	
	hdr = radar.getHeader()
	fn = hdr.frameNumber
	
	if  fn != prev_fn:
		#print("--------------{:}-----------".format(fn))
		prev_fn = fn
		v8len = len(v8)
		v9len = len(v9)
		v10len = len(v10)
		
		if v8len == 3072:
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
				# Add Zone 
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
'''
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore,'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
'''
if __name__ == '__main__':
	 pg.exec()
 	
    #(3.1) 
if __name__ == '__main__':
	import sys
	if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'): 
		QtWidgets.QApplication.instance().exec_()  # for pyqrgraph 0.13 version
