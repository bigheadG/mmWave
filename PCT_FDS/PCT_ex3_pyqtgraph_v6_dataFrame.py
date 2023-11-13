#=============================================
# File Name: PCT_ex3_pyqtgraph_v6_dataFrame.py
#
# Requirement:
# Hardware: BM502-AOP(V4958)
# Firmware: 
#
# lib: pct
#
# plot tools: pyqtgraph
# Plot point cloud(V6) in 3D figure 
# wall mount people counting with tilt (PCT)
# type: Raw data
# Baud Rate: playback: 119200
#			 real time: 921600
#=============================================

#from pyqtgraph.Qt import QtCore, QtGui
from PyQt5 import QtGui, QtWidgets, QtCore  # for linux
from PyQt5.QtGui import QPen, QColor

import pyqtgraph.opengl as gl
import pyqtgraph as pg
import numpy as np

from mmWave import pct
import serial
from threading import Thread


from datetime import date,datetime,time
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import pandas as pd
pd.options.display.float_format = '{:.2f}'.format

################### Run Time/Playback & parameter setting   ######
#RUN_TIME = False #playback
RUN_TIME = True   #run time

###################################################################################
# Parameters:
PORT = 'COM47'
#PORT = '/dev/tty.usbmodem14303'

JB_TILT_DEGREE = 45 
JB_RADAR_INSTALL_HEIGHT = 2.39 # meter

QUEUE_LEN = 3

BAUD_RATE = 921600 if RUN_TIME == True else 115200
PLAYBACK_FILE  = "pct_2023-02-08-16-48-32.csv" # find file in same directory

####################################################################

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
		a = 0
		#self.GLViewWidget.qglColor(QtCore.Qt.cyan)
		#self.GLViewWidget.renderText(round(self.X), round(self.Y), round(self.Z), self.text)

tt = datetime.now()
dt = tt.strftime("%Y-%m-%d-%H-%M-%S")  # 格式化日期
fileName = "pct{:}.csv".format(dt)

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



#app = QtGui.QApplication([])
app = QtWidgets.QApplication([])     # for linux

w = gl.GLViewWidget()
w.setWindowTitle('PCT (point clouds) demo')
w.show()

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
#port = serial.Serial("/dev/tty.SLAB_USBtoUART3",baudrate = 921600, timeout = 0.5)   
#port = serial.Serial("/dev/tty.usbmodem144403",baudrate = 115200 , timeout = 0.5) 
#for NUC ubuntu 
#port = serial.Serial("/dev/ttyACM1",baudrate = 921600, timeout = 0.5)

port = serial.Serial(PORT,baudrate = BAUD_RATE , timeout = 0.5) 
radar = pct.Pct(port,tiltAngle=JB_TILT_DEGREE,height = JB_RADAR_INSTALL_HEIGHT, df = "DataFrame")


#for playback use
if RUN_TIME == False:
	(v6smu,v7smu,v8smu) = radar.readFile(PLAYBACK_FILE)
	print("------------------ v6smu --------start:{:}  stop:{:}--------------".format(radar.sim_startFN,sim_stopFN))
	print(v6smu)
	print("------------------ v7smu ----------------------")
	print(v7smu)
	print("------------------ v8smu ----------------------")
	print(v8smu)

v6len = 0
v7len = 0
v8len = 0

pos = np.zeros((100,3))
color = [1.0, 0.0, 0.0, 1.0]
sp1 = gl.GLScatterPlotItem(pos=pos,color=color,size = 8.0)
w.addItem(sp1)

#generate a color opacity gradient
pos1 = np.empty((50,3))
uFlag = True
def update():
    ## update volume colors
	global pos1,lblA,color,uFlag
	
	if len(pos1) > 0:
		trA = pos1
		trA = trA[:,(0, 2, 1)] # x, z, y
		#trA[:, 2] = JB_RADAR_INSTALL_HEIGHT - trA[:, 2] # x, z, height  
		sp1.setData(pos=trA,color=color)

t = QtCore.QTimer()
t.timeout.connect(update)
t.start(150)
fn = 0 
prev_fn = 0
lblA =[]
def showData(dck,v6i,v7i,v8i):
	if dck:
		v6len = len(v6i)
		v7len = len(v7i)
		v8len = len(v8i)
		print("Sensor Data: [v6,v7,v8]:[{:d},{:d},{:d}]".format(v6len,v7len,v8len))
		if v6len > 0:
			v6i = v6i.sort_values(by='snr', ascending=False)
			print("\n--------v6-----------fn:{:} len({:})".format(fn,v6len))
			v6i = v6i[:10]
			print(v6i)
			#print(v6i.mean())
			
			
		if 1:
			if v7len > 0:
				print("\n--------v7-----------fn:{:} len({:})".format(fn,v7len))
				print(v7i)
			if v8len > 2:
				lv8 = v8len-2 if v8len > 2 else 0
				print("\n--------v8-----------fn:{:} len({:})".format(fn,lv8))
				print(v8i)

#objBuf = [[0,0,0],[0,0,0],[0,0,0],[0,0,0],[0,0,0]]
locBuf = []

objBuf = pd.DataFrame([], columns=['fN','sx','sy','sz'])

def radarExec():
	global v6len,v7len,v8len,pos1,prev_fn,color,sim_stopFN,fn,objBuf,locBuf,JB_RADAR_INSTALL_HEIGHT,QUEUE_LEN
	v6 = []
	v7 = []
	v8 = []
	sample_point = 7
	flag = True
	(dck,v6,v7, v8)  = radar.tlvRead(False)
	
	hdr = radar.getHeader()
	fn = hdr.frameNumber
	
	#(playback) 
	if RUN_TIME== False:
		#print("-----------fn:{:}--------start:{:}   stop:{:}".format(fn,radar.sim_startFN,radar.sim_stopFN))
		(dck,v6,v7,v8) = radar.getRecordData(fn)
		
	#showData(dck,v6,v7,v8)
	 
	if  fn != prev_fn:
		
		prev_fn = fn
		
		
		print(f"---------------fn:{fn}  prev_fn: {prev_fn}---------")
		
		
		v8len = len(v8)
		v8len = v8len-2 if v8len > 2 else 0
		v6len = len(v6)
		v7len = len(v7)
		print("Sensor Data: [v6,v7,v8]:[{:d},{:d},{:d}]".format(v6len,v7len,v8len))
		showData(dck,v6,v7,v8)
		
		
		if v6len != 0: #and flag == True:
			flag = False
			posTemp = v6
			v6Temp = v6
			#print(v6)
			v6op = v6    #v6Temp[(v6Temp.sx > -0.5) & (v6Temp.sx < 0.5) & (v6Temp.sy < 1.0) & (v6Temp.doppler != 0) ]
			d = v6op.loc[:,['sx','sy','sz']] 
			dd = v6op.loc[:,['sx','sy','sz','doppler']] 
			
			#(1.1) insert v6 to data Queue(objBuf) 
			objBuf = objBuf._append(v6op.loc[:,['fN','sx','sy','sz']], ignore_index=False)
			locBuf.insert(0,fn)
			if len(locBuf) > QUEUE_LEN:
				objBuf = objBuf.loc[objBuf.fN != locBuf.pop()]
			
			#(1.2)DBSCAN 
			#d_std = StandardScaler().fit_transform(xy6A)
			if len(d) > sample_point:
				d_std = StandardScaler().fit_transform(d)
				
				#db = DBSCAN(eps=1.4, min_samples=3).fit(d_std)
				db = DBSCAN(eps= 2.0, min_samples=sample_point).fit(d_std) # 1.2
				#db = DBSCAN(eps=0.15, min_samples=6).fit(d)  # 
					
				labels = db.labels_  #cluster ID
				
				dd_np = dd.to_numpy()
				#(1.3)insert labels to sensor temp Array(stA) stA = [x,y,z,Doppler,labels]
				stA = np.insert(dd_np,4,values=labels,axis= 1) #[x,y,z,Doppler,labels]
				print("==[{:}]========== stA =====d:{:}=======stA:{:}".format(fn,d.shape,stA.shape))
				print(stA)
				mask = (labels == -1)
				sensorA = []
				sensorA = stA[~mask]
				print("==[{:}]====== sensorA ========={:}".format(fn,sensorA.shape))
				print(sensorA)
				lblA = sensorA[:,4]
				
				dm = d[~mask] #
				
				xBuf = objBuf.loc[:,['sx','sz','sy']]
				pos_np = xBuf.to_numpy()  #dm.to_numpy()
			
				#pos_np[:,2] = JB_RADAR_INSTALL_HEIGHT - pos_np[:,2]
				color = np.empty((len(lblA),4), dtype=np.float32)
				for i in range(len(lblA)):
					x = int(lblA[i])
					color[i] = colorSet[x] 
				
				pos1 = pos_np
				print(f"pos_np = {pos_np}" )
				lbs = labels[~mask] 
				print("mask set:{:}".format(set(lbs)))
				cnt = 0
				for k in set(lbs):
					gpMask = (lbs == k)
					m = sensorA[gpMask]
					#print(f"m({k}) =  {m}")
					mA = (np.mean(m,axis=0))
					#print(mA)
					 
					print("Get 3D Box: k:{:} box= \n{:}".format(k,get3dBox(sensorA[gpMask])))
					(x,xl,y,yl,_,_,nop) = get3dBox(sensorA[gpMask])
					 
		 
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
        #QtGui.QApplication.instance().exec_()
        QtWidgets.QApplication.instance().exec_()  # for linux
