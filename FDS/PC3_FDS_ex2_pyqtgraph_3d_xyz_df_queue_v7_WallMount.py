#=============================================
# File Name: PC3_FDS_ex2_pyqtgraph_3d_xyz_df_queue_v7_WallMount.py
#
# Requirement:
# Hardware: BM501-AOP
# Firmware: V5051 PC3-I470 for WallMount
# Lib: pc3OVH 
#
# Plot Tools: pyqtgraph
# Plot Target (V7) in 3D figure 
# Type: Raw Data 
# Baud Rate: PlayBack: 119200
#            RealTime: 921600

# ALERT: use pyqtgraph 0.11.0

#=============================================

from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import pyqtgraph as pg
import numpy as np
from mmWave import pc3OVH

import serial
from threading import Thread

from datetime import date,datetime,time
import pandas as pd



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


tt = datetime.now()
dt = tt.strftime("%Y-%m-%d-%H-%M-%S")  # 格式化日期
fileName = "pc3{:}.csv".format(dt)

st = datetime.now()
sim_startFN = 0
sim_stopFN = 0

colorSet = [[1.0,1.0, 0,1.0], [0, 1.0, 0, 1.0], [0, 0.4, 1.0, 1.0], [0.97, 0.35, 1.0, 1.0], [0.35, 0.99, 0.99, 1.0],
			[0.99, 0.35, 0.88, 1.0],[0.99, 0.9, 0.8, 1.0],[0.2, 1.0, 1.0, 1.0],[0.9, 0.8, 1.0, 1.0], [0.35, 0.99, 0.4, 1.0], 
			[0.5, 1.0, 0.83, 1.0], [0.99, 0.64, 0.35, 1.0],[0.35, 0.9, 0.75, 1.0],[1.0, 0.5, 0, 1.0],[1.0, 0.84, 0, 1.0],[0, 0, 1.0, 1.0]]



class Custom3DAxis(gl.GLAxisItem):
	#Class defined to extend 'gl.GLAxisItem'
	def __init__(self, parent, color=(0.0,0.0,0.0,.6)):
		gl.GLAxisItem.__init__(self)
		self.parent = parent
		self.c = color
		
	def add_tick_values(self, xticks=[], yticks=[], zticks=[]):
		#Adds ticks values. 
		x,y,z = self.size()
		xtpos = np.linspace(0, x, len(xticks))
		ytpos = np.linspace(0, y, len(yticks))
		ztpos = np.linspace(0, z, len(zticks))
		#X label
		for i, xt in enumerate(xticks):
			val = CustomTextItem((xtpos[i]), Y= 0, Z= 0, text='{}'.format(xt))
			val.setGLViewWidget(self.parent)
			self.parent.addItem(val)
		#Y label
		for i, yt in enumerate(yticks):
			val = CustomTextItem(X=0, Y=round(ytpos[i]), Z= 0, text='{}'.format(yt))
			val.setGLViewWidget(self.parent)
			self.parent.addItem(val)
		#Z label
		for i, zt in enumerate(zticks):
			val = CustomTextItem(X=0, Y=0, Z=round(ztpos[i]), text='{}'.format(zt))
			val.setGLViewWidget(self.parent)
			self.parent.addItem(val)

class Custom3Dlabel(gl.GLGraphicsItem.GLGraphicsItem):
	#Class defined to extend 'gl.GLAxisItem'
	def __init__(self, parent, color=(0.0,0.0,0.0,.6)):
		gl.GLGraphicsItem.GLGraphicsItem.__init__(self)
		self.parent = parent
		self.c = color
		
	#def add_values(self, xticks=[], yticks=[], zticks=[]):
	def set_values(self,text, x,y,z):
		val = CustomTextItem(X = x, Y= y, Z= z, text='{}'.format(text))
		val.setGLViewWidget(self.parent)
		self.parent.addItem(val)

##################### Parameter ################################### 
QUEUE_LEN = 15

################### Real Time or read from file switch ************
rtSwitch = True # real time mode
# rtSwitch = False  # read data from file

# ALERT: Assume RADAR board tilt 0 degree
# ALERT: This value may be changed depends on your RADAR installation
#JB_RADAR_INSTALL_HEIGHT = 2.46 # OVER HEAD
JB_RADAR_INSTALL_HEIGHT = 2.00 # WALL MOUNT 


app = QtGui.QApplication([])
w = gl.GLViewWidget()
w.show()


####### create box to represent device ######
verX = 0.0625
verY = 0.05
verZ = 0.125
zOffSet =  JB_RADAR_INSTALL_HEIGHT
verts = np.empty((2,3,3))
verts[0,0,:] = [-verX, 0, verZ + zOffSet]
verts[0,1,:] = [-verX, 0,-verZ + zOffSet]
verts[0,2,:] = [verX,  0,-verZ + zOffSet]
verts[1,0,:] = [-verX, 0, verZ + zOffSet]
verts[1,1,:] = [verX,  0, verZ + zOffSet]
verts[1,2,:] = [verX,  0, -verZ + zOffSet]
 
evmBox = gl.GLMeshItem(vertexes=verts,smooth=False,drawEdges=True,edgeColor=pg.glColor('r'),drawFaces=False)
w.addItem(evmBox)
#############################################

#size=50:50:50
g = gl.GLGridItem()
g.setSize(x=50,y=50,z=50)
#g.setSpacing(x=1, y=1, z=1, spacing=None)
w.addItem(g)

axis = Custom3DAxis(w, color=(0.2,0.2,0.2,1.0))
axis.setSize(x=5, y=5, z=5)
xt = [0,1,2,3,4,5]  
axis.add_tick_values(xticks=xt, yticks=xt, zticks=xt)
w.addItem(axis)


lblA = []
for i in range(15):
	#lbl = Custom3Dlabel(w,color=(0.2,0.2,0.2,1.0))
	lbl = Custom3Dlabel(w,color=colorSet[i])
	lbl.set_values('',1,1,1)
	lblA.append(lbl)


###################################################################
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
#port = serial.Serial("/dev/tty.usbmodemGY0052534",baudrate = 921600, timeout = 0.5)
#port = serial.Serial("/dev/tty.usbmodem14103",baudrate = 115200 , timeout = 0.5)  
#port = serial.Serial("/dev/tty.usbmodemGY0050674",baudrate = 921600, timeout = 0.5)  
port = serial.Serial("/dev/tty.SLAB_USBtoUART3",baudrate = 921600, timeout = 0.5)  

#for NUC ubuntu 
#port = serial.Serial("/dev/ttyACM1",baudrate = 921600, timeout = 0.5)

# for PC3 WINDOWS10
#port = serial.Serial("COM125",baudrate = 921600, timeout = 0.5)  


radar = pc3OVH.Pc3OVH(port)


v6len = 0
v7len = 0
v8len = 0


color = [1.0, 0.0, 0.0, 1.0]
pos = np.zeros((100,3))
sp1 = gl.GLScatterPlotItem(pos=pos,color=color,size = 12.0)
w.addItem(sp1)


#for playback use
if rtSwitch == False:
	(v6smu,v7smu,v8smu) = radar.readFile("pc3Aop2021-04-07-23-52-34.csv")
	print("------------------ v6smu --------start:{:}  stop:{:}--------------".format(radar.sim_startFN,sim_stopFN))
	print(v6smu)
	print("------------------ v7smu ----------------------")
	print(v7smu)
	print("------------------ v8smu ----------------------")
	print(v8smu)


pos1 = np.empty((50,3))
lblTextA = []
gcolorA = []
uFlag = True

def update():    
	global pos1,uFlag,gcolorA,lblA,lblTextA
	if uFlag == True:
		uFlag = False
		gcolor = np.array(gcolorA)
		#print("------------------ pos1 ----------------------:{:}".format(len(gcolor)))
		#print(gcolor)
		sp1.setData(pos=pos1,color=gcolor)
		
		'''
		#labeling id in target
		for i in range(15):
			if i > len(lblA):
				lblA[i].set_values('',0,0,0)
			else:
				lblA[i].set_values(lblTextA[i],pos1[i,0],pos1[i,1],pos1[i,2])
		'''
    
t = QtCore.QTimer()
t.timeout.connect(update)
t.start(150)
fn = 0 
prev_fn = 0

def showData(dck,v6i,v7i,v8i):
	if dck:
		v6len = len(v6i)
		v7len = len(v7i)
		v8len = len(v8i)
		print("Sensor Data: [v6,v7,v8]:[{:d},{:d},{:d}]".format(v6len,v7len,v8len))
		if v6len > 0:
			print("\n--------v6-----------fn:{:} len({:})".format(fn,v6len))
			print(v6i)
		if v7len > 0:
			print("\n--------v7-----------fn:{:} len({:})".format(fn,v7len))
			print(v7i)
		if v8len > 2:
			print("\n--------v8-----------fn:{:} len({:})".format(fn,v8len-2))
			print(v8i)


locBuf = []
objBuf = pd.DataFrame([], columns=['fN','posX','posY','posZ','tid'])

def radarExec():
	global v6len,v7len,v8len,pos1,prev_fn,flag,uFlag,sim_stopFN,fn,objBuf,locBuf,JB_RADAR_INSTALL_HEIGHT,QUEUE_LEN,colorSet,gcolorA,lblTextA
	v6 = []
	v7 = []
	v8 = []
	
	flag = True
	(dck,v6,v7, v8)  = radar.tlvRead(False,df = 'DataFrame')
	
	hdr = radar.getHeader()
	
	fn = hdr.frameNumber
	#(playback) 
	if rtSwitch == False:
		print("-----------fn:{:}--------start:{:}   stop:{:}".format(fn,radar.sim_startFN,radar.sim_stopFN))
		(dck,v6,v7,v8) = radar.getRecordData(fn)
	
	#showData(dck,v6,v7,v8)
	
	if  fn != prev_fn:
		print("--------------{:}-----------".format(fn))
		prev_fn = fn
		v8len = len(v8)
		v6len = len(v6)
		v7len = len(v7)
		
		print("Sensor Data: [v6,v7,v8]:[{:d},{:d},{:d}]".format(v6len,v7len,v8len-2))
		if v7len != 0 and flag == True:
			flag = False
			
			#(1.1) insert v7 to data Queue(objBuf) 
			objBuf = objBuf.append(v7.loc[:,['fN','posX','posZ','posY','tid']], ignore_index=True)
			locBuf.insert(0,fn)
			if len(locBuf) > QUEUE_LEN:
				objBuf = objBuf.loc[objBuf.fN != locBuf.pop()]
			#print("========objBuf:len:{:}".format(len(objBuf)))
			#print(locBuf)
			#print(objBuf)
			
			
			#(1.2)set color based on tid
			tidA = objBuf['tid'].values.tolist()  #tidA.astype(int)
			gcolorA = []
			
			for i in range(len(tidA)):
				gcolorA.append(colorSet[int(tidA[i])%15])
				
				#labeling id in target 
				#idString = "" # "id{:}".format(int(tidA[i])%15)
				#lblTextA.append(idString)
				
			
			#(1.3)TargetID 
			#xBuf = objBuf.loc[:,['posX','posZ','posY']] # OVER HEAD
			xBuf = objBuf.loc[:,['posX','posY','posZ']]  # WALL MOUNT
			pos_np = xBuf.to_numpy()
			
			#Radar install position
			#pos_np[:,2] = JB_RADAR_INSTALL_HEIGHT - pos_np[:,2]  # OVER HEAD
			pos_np[:,2] =  JB_RADAR_INSTALL_HEIGHT + pos_np[:,2]  # WALL MOUNT
			
			pos1 = pos_np
			
			uFlag = True
			flag = True
			
	port.flushInput()

def get3dBox(targetCloud): 
	xMax = np.max(targetCloud[:,0])
	xr   = np.min(targetCloud[:,0])
	xl = np.abs(xMax-xr)

	yMax = np.max(targetCloud[:,1])
	yr = np.min(targetCloud[:,1])
	yl = np.abs(yMax-yr)
	
	zMax = np.max(targetCloud[:,2])
	zr = np.min(targetCloud[:,2])
	zl = np.abs(zMax-zr)
	
	nop = len(targetCloud)
	return (xr,xl,yr,yl,zr,zl,nop)	
		 
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
