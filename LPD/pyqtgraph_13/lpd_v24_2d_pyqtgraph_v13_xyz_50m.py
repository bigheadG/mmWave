#=======================================================================
# File Name: lpd_v24_2d_pyqtgraph_xyz_50m.py
#
# Requirement:
# Hardware: BM201-ISK (AWR6843)
# Firmware: LPD
# config file:(V24_JB)people_detection_and_tracking_50m_2D_advanced.cfg
# lib: lpdISK 
# plot tools: pyqtgraph 3D
# Plot point cloud(V6) in 3D figure 
# type: Raw data
# Baud Rate:
#=======================================================================

#from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.Qt import mkQApp ,QtCore ,QtGui
from PyQt5 import QtGui, QtWidgets

import pyqtgraph.opengl as gl
import pyqtgraph as pg
import numpy as np
from mmWave import lpdISK
import serial
from threading import Thread

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
		self.GLViewWidget.renderText(self.X, self.Y, self.Z, self.text)


class Custom3DAxis(gl.GLAxisItem):
	#Class defined to extend 'gl.GLAxisItem'
	def __init__(self, parent, color=(0,0,0,.6)):
		gl.GLAxisItem.__init__(self)
		self.parent = parent
		self.c = color
		
	def add_labels(self):
		#Adds axes labels. 
		x,y,z = self.size()
		#X label
		self.xLabel = CustomTextItem(X=x/2, Y=-y/20, Z=-z/20, text="X")
		self.xLabel.setGLViewWidget(self.parent)
		self.parent.addItem(self.xLabel)
		#Y label
		self.yLabel = CustomTextItem(X=-x/20, Y=y/2, Z=-z/20, text="Y")
		self.yLabel.setGLViewWidget(self.parent)
		self.parent.addItem(self.yLabel)
		#Z label
		self.zLabel = CustomTextItem(X=-x/20, Y=-y/20, Z=z/2, text="Z")
		self.zLabel.setGLViewWidget(self.parent)
		self.parent.addItem(self.zLabel)
		
	def add_tick_values(self, xticks=[], yticks=[], zticks=[]):
		#Adds ticks values. 
		x,y,z = self.size()
		xtpos = np.linspace(0, x, len(xticks))
		ytpos = np.linspace(0, y, len(yticks))
		ztpos = np.linspace(0, z, len(zticks))
		#X label
		for i, xt in enumerate(xticks):
			val = CustomTextItem(X=xtpos[i], Y=0, Z=0, text='{}'.format(xt))
			val.setGLViewWidget(self.parent)
			self.parent.addItem(val)
		#Y label
		for i, yt in enumerate(yticks):
			val = CustomTextItem(X=0, Y=ytpos[i], Z=0, text='{}'.format(yt))
			val.setGLViewWidget(self.parent)
			self.parent.addItem(val)
		#Z label
		for i, zt in enumerate(zticks):
			val = CustomTextItem(X=0, Y=0, Z=ztpos[i], text='{}'.format(zt))
			val.setGLViewWidget(self.parent)
			self.parent.addItem(val)

#app = QtGui.QApplication([])
app = QtWidgets.QApplication([]) 

w = gl.GLViewWidget()
w.show()

g = gl.GLGridItem()
g.setSize(x=200,y=200,z=5)
w.addItem(g)

axis = Custom3DAxis(w, color=(0.2,0.2,0.2,1.0))
axis.setSize(x=100, y=100, z=5)
zt = [0,1,2,3,4,5]
xt = [0,20,40,60,80,100]  
axis.add_tick_values(xticks=xt, yticks=xt, zticks=zt)
w.addItem(axis)

#
#use USB-UART
#port = serial.Serial("/dev/ttyUSB0",baudrate = 921600, timeout = 0.5)
#
#for Jetson nano UART port
#port = serial.Serial("/dev/ttyTHS1",baudrate = 921600, timeout = 0.5) 
#
#for pi 4 UART port
#port = serial.Serial("/dev/ttyS0",baudrate = 921600, timeout = 0.5)
#
#Drone Object Detect Radar initial 
#port = serial.Serial("/dev/tty.usbmodemGY0052854",baudrate = 921600, timeout = 0.5)
port = serial.Serial("COM4",baudrate = 921600, timeout = 0.5)
#for NUC ubuntu 
#port = serial.Serial("/dev/ttyACM1",baudrate = 921600, timeout = 0.5)

#Firmware verion before v0910 use:
#radar = lpdISK.LpdISK(port)

#Firmware v0910 and v0985 use: 
radar = lpdISK.LpdISK(port,seq = "xyz")


v6len = 0
v7len = 0
v8len = 0
v9len = 0

pos1 = np.empty((100,3))
pos = np.zeros((100,3))
color = [1.0, 0.0, 0.0, 1.0]
sp1 = gl.GLScatterPlotItem(pos=pos1,color=color,size = 3.0)
w.addItem(sp1)

#generate a color opacity gradient



def update():
    ## update volume colors
    global color,pos1
    '''
    color = np.empty((len(pos1),4), dtype=np.float32)
    color[:,3] = 1.0
    color[:,0] =  np.clip(pos1[:,0] * 3.0, 0, 1)
    color[:,1] =  np.clip(pos1[:,1] * 1.0, 0,1)
    color[:,2] =  np.clip(pos1[:,2] ** 3, 0, 1)
    '''
    #print(len(pos1))
    sp1.setData(pos=pos1,color=[1.0,1.0,0.0,1.0])


t = QtCore.QTimer()
t.timeout.connect(update)
t.start(50)
zOffset = 0.0
def radarExec():
	global v6len,v7len,v8len,v9len,pos1,zOffset
	flag = True
	(dck,v6,v7,v8,v9)  = radar.tlvRead(False)

	#hdr = radar.getHeader()
	radar.headerShow() # check sensor information
	if dck:
		v8len = len(v8)
		v6len = len(v6)
		v7len = len(v7)
		v9len = len(v9)
		print("Sensor Data: [v6,v7,v8]:[{:d},{:d},{:d},{:d}]".format(v6len,v7len,v8len,v9len))
		if v6len != 0 and flag == True:
			flag = False
			pct = v6
			#For x,y,z test
			
			#pos1[2] = (0,2,0) #y
			#pos1[1] = (3,0,0) #x
			#pos1[0] = (0,0,1) #z
			 
			# v6 struct = [(r,a,e,d),(r,a,e,d),(r,a,e,d)..]
			pos1X = np.empty((len(pct),3))
			for i in range(len(pct)):
				zt = pct[i][0] * np.sin(pct[i][2]) + zOffset
				xt = pct[i][0] * np.cos(pct[i][2]) * np.sin(pct[i][1])
				yt = pct[i][0] * np.cos(pct[i][2]) * np.cos(pct[i][1])
				#print("x={:} y={:}".format(xt,yt))
				pos1X[i] = (xt,yt,zt)
				#print(pos1X[i])
				
			pos1 = pos1X
			flag = True
		 
	port.flushInput()
		
		 
def uartThread(name):
	port.flushInput()
	while True:
		radarExec()
					
thread1 = Thread(target = uartThread, args =("UART",))
thread1.setDaemon(True)
thread1.start()

## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
	 pg.exec()
'''
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore,'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
'''
