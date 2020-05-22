#=============================================
# File Name: pyqtgraph_3d_drn.py
#
# Requirement:
# Hardware: BM201-ISK
# Firmware: DRN
# lib: droneRN  
# Plot point cloud(V1) in 3D figure 
# type: Raw data
# Baud Rate:
#=============================================

from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import pyqtgraph as pg
import numpy as np
from mmWave import droneRN
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

app = QtGui.QApplication([])
w = gl.GLViewWidget()
w.show()

#size=50:50:50
g = gl.GLGridItem()
g.setSize(x=50,y=50,z=50)
#g.setSpacing(x=1, y=1, z=1, spacing=None)
w.addItem(g)

#
axis = Custom3DAxis(w, color=(0.2,0.2,0.2,1.0))
axis.setSize(x=25, y=25, z=25)
xt = [0,5,10,15,20,25]  
axis.add_tick_values(xticks=xt, yticks=xt, zticks=xt)
w.addItem(axis)

#use USB-UART
#port = serial.Serial("/dev/ttyUSB0",baudrate = 921600*2, timeout = 0.5)
#
#for Jetson nano UART port
#port = serial.Serial("/dev/ttyTHS1",baudrate = 921600*2, timeout = 0.5) 
#
#for pi 4 UART port
#port = serial.Serial("/dev/ttyS0",baudrate = 921600*2, timeout = 0.5)
#
#Drone Object Detect Radar initial 
port = serial.Serial("/dev/tty.usbmodemGY0052854",baudrate = 921600*2, timeout = 0.5)
#for NUC ubuntu 
#port = serial.Serial("/dev/ttyACM1",baudrate = 921600*2, timeout = 0.5)

drn = droneRN.DroneRN(port)

v1len = 0
v2len = 0
v3len = 0
v6len = 0
v7len = 0

pos = np.zeros((100,3))
color = [1.0, 0.0, 0.0, 1.0]
sp1 = gl.GLScatterPlotItem(pos=pos,color=color)
w.addItem(sp1)

#generate a color opacity gradient
'''
color = np.zeros((pos.shape[0],4), dtype=np.float32)
color[:,0] = 1
color[:,1] = 0
color[:,2] = 0.5
color[0:100,3] = np.arange(0,100)/100.
'''
pos1 = np.empty((50,3))

def update():
    ## update volume colors
    global color,pos1
    color = np.empty((len(pos1),4), dtype=np.float32)
    color[:,3] = 1.0
    color[:,0] =  np.clip(pos1[:,0] * 3.0, 0, 1)
    color[:,1] =  np.clip(pos1[:,1] * 1.0, 0,1)
    color[:,2] =  np.clip(pos1[:,2] ** 3, 0, 1)
    #print(len(pos1))
    sp1.setData(pos=pos1,color=color)

t = QtCore.QTimer()
t.timeout.connect(update)
t.start(50)


def drnExec():
	global v1len,v2len,v3len,v6len,v7len,pos1
	flag = True
	(dck,v1,v2,v3,v6,v7) = drn.tlvRead(False)
	
	#hdr = drn.getHeader()
	#drn.headerShow()
	 
	if dck == 1:
		v1len = len(v1)
		v2len = len(v2)
		v3len = len(v3)
		v6len = len(v6)
		v7len = len(v7)
		print("Sensor Data: [v1,v2,v3,v6,v7]:[{:d},{:d},{:d},{:d},{:d}]".format(v1len,v2len,v3len,v6len,v7len))
		#print(v1)	
		if v1len != 0 and flag == True:
			flag = False
			#v1:[(x,y,z,vel))...]
			#posTemp = np.empty((50,3))
			posTemp = v1
			
			''' #For x,y,z test
			pos1[2] = (0,2,0)
			pos1[1] = (3,0,0)
			pos1[0] = (0,0,1)
			'''
			pos1X = np.empty((len(posTemp),3))
			for i in range(len(posTemp)):
				pos1X[i] = (posTemp[i][0],posTemp[i][1],posTemp[i][2])
				#print(pos1X[i])
			pos1 = pos1X
			flag = True
			
	port.flushInput()
		
		 
def uartThread(name):
	port.flushInput()
	while True:
		drnExec()
					
thread1 = Thread(target = uartThread, args =("UART",))
thread1.setDaemon(True)
thread1.start()

## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore,'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
