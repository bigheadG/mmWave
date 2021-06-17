#=============================================
# File Name: pyqtgraph_3d_xyz_df_ex1_forGesture.py
#
# Requirement:
# Hardware: BM501-AOP
# Firmware: V5050-PCR
# Lib: pc3 
# Plot tools: pyqtgraph
# Plot point cloud(V6) in 3D figure 
# Type: Raw data
# Baud Rate: Playback: 119200
#			 RealTime: 921600
#=============================================

##############################################
# Set parameters for wanted zone size depends 
REALTIME = True
LIMIT_X_LO = -0.5   # width Left
LIMIT_X_HI = +0.5   # width Right
LIMIT_Y_HI = +1.0   # depth 
##############################################


from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import pyqtgraph as pg
import numpy as np
from mmWave import pc3
#import pc3 as pc3
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



use = "play"

tt = datetime.now()
dt = tt.strftime("%Y-%m-%d-%H-%M-%S")  # 格式化日期
fileName = "pc3{:}.csv".format(dt)

st = datetime.now()
sim_startFN = 0
sim_stopFN = 0

colorSet = [[255,255, 0,255], [0, 255, 0, 255], [0, 100, 255, 255], [248, 89, 253, 255], [89, 253, 242, 255],[89, 253, 253, 255],
		  [253, 89, 226, 255],[253, 229, 204, 255],[51, 255, 255, 255],[229, 204, 255, 255], [89, 253, 100, 255], 
		  [127, 255, 212, 255], [253, 165, 89, 255],[255, 140, 0, 255],[255, 215, 0, 255],[0, 0, 255, 255]]




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

app = QtGui.QApplication([])
w = gl.GLViewWidget()
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
#port = serial.Serial("/dev/tty.SLAB_USBtoUART3",baudrate = 921600 , timeout = 0.5)


#for NUC ubuntu 
#port = serial.Serial("/dev/ttyACM1",baudrate = 921600, timeout = 0.5)
port = serial.Serial("/dev/ttyUSB1",baudrate = 921600, timeout = 0.5)

radar = pc3.Pc3(port)

v6len = 0
v7len = 0
v8len = 0

pos = np.zeros((100,3))
color = [1.0, 0.0, 0.0, 1.0]
sp1 = gl.GLScatterPlotItem(pos=pos,color=color,size = 4.0)
w.addItem(sp1)

'''
#######################################
REALTIME = True
LIMIT_X_LO = -0.5
LIMIT_X_HI = 0.5
LIMIT_Y_HI = 1.0
#######################################
'''

if REALTIME == False:
	#for playback use
	(v6smu,v7smu,v8smu) = radar.readFile("pc3az2021-04-01-23-18-25.csv")
	print("------------------ v6smu --------start:{:}  stop:{:}--------------".format(radar.sim_startFN,sim_stopFN))
	print(v6smu)
	print("------------------ v7smu ----------------------")
	print(v7smu)
	print("------------------ v8smu ----------------------")
	print(v8smu)


#generate a color opacity gradient
pos1 = np.empty((50,3))
uFlag = True
def update():
    ## update volume colors
	global pos1,lblA,color,uFlag

	if uFlag == True:
		uFlag = False
	#print(len(pos1))
		sp1.setData(pos=pos1,color=color)

t = QtCore.QTimer()
t.timeout.connect(update)
t.start(50)
fn = 0 
prev_fn = 0
lblA =[]


def radarExec():
	global v6len,v7len,v8len,pos1,prev_fn,color,flag,uFlag,sim_stopFN
	v6 = []
	v7 = []
	v8 = []
	sample_point = 7
	flag = True
	(dck,v6,v7,v8) = radar.tlvRead(False,df = 'DataFrame')
	hdr = radar.getHeader()
	#radar.headerShow() # check sensor information
	fn = hdr.frameNumber
	
	#(playback)
	if REALTIME == False:
		(dck,v6,v7,v8)  = radar.getRecordData(fn)
		print("\n--------v6-----------fn:{:} len({:})".format(fn,len(v6)))
		print(v6)
		print("\n--------v8-----------fn:{:} len({:})".format(fn,len(v8)))
		print(v8)
		if fn + radar.sim_startFN > radar.sim_stopFN:
			print("-------- Last record[{:}]----{:}-----------".format(radar.sim_stopFN,fn-1) )
			return
	 
	if  fn != prev_fn:
		print("--------------{:}-----------".format(fn))
		prev_fn = fn
		v8len = len(v8)
		v6len = len(v6)
		v7len = len(v7)
		
		print("Sensor Data: [v6,v7,v8]:[{:d},{:d},{:d}]".format(v6len,v7len,v8len))
		if v6len != 0 and flag == True:
			flag = False
			posTemp = v6
			v6Temp = v6
			
			v6op = v6Temp[(v6Temp.sx > LIMIT_X_LO) & (v6Temp.sx < LIMIT_X_HI) & (v6Temp.sy < LIMIT_Y_HI) & (v6Temp.doppler != 0) ]
			d = v6op.loc[:,['sx','sy','sz']] 
			dd = v6op.loc[:,['sx','sy','sz','doppler']] 
			
			#(1.2)DBSCAN 
			#d_std = StandardScaler().fit_transform(xy6A)
			if len(d) > sample_point:
				d_std = StandardScaler().fit_transform(d)
				
				#db = DBSCAN(eps=1.4, min_samples=3).fit(d_std)
				#db = DBSCAN(eps= 2.0, min_samples=sample_point).fit(d_std) # 1.2
				db = DBSCAN(eps=0.15, min_samples=6).fit(d)  
					
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
				pos_np = dm.to_numpy()
				pos_np[:,2] += 0.5
				#print(d)
				
				color = np.empty((len(lblA),4), dtype=np.float32)
				for i in range(len(lblA)):
					x = int(lblA[i])
					color[i] = colorSet[x] 
				
				pos1 = pos_np
				
				lbs = labels[~mask] 
				print("mask set:{:}".format(set(lbs)))
				cnt = 0
				for k in set(lbs):
					gpMask = (lbs == k)
					m = sensorA[gpMask]
					mA = (np.mean(m,axis=0))
					print(mA)
					print("Get 3D Box: k:{:} box= \n{:}".format(k,get3dBox(sensorA[gpMask])))
					(x,xl,y,yl,_,_,nop) = get3dBox(sensorA[gpMask])
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
