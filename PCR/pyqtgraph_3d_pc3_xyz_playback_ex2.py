#=============================================
# File Name: pyqtgraph_3d_xyz_playback_ex2.py
# Date:2021/04/02
# Requirement:
# Hardware: BM501-AOP
# Firmware: PC3
# config file: (V34_PC3_6m_100m)ISK_6m_default.cfg
# lib: pc3 
# plot tools: pyqtgraph
# Plot point cloud(V6) in 3D figure 
# type: Raw data
# Baud Rate: playback: 115200
#			 real time: 921600
#=============================================

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
		

##################### Parameter ################################### 
HIGH_OFFSET = 0.5
QUEUE_LEN = 15


###################################################################

locBuf = []
objBuf = pd.DataFrame([], columns=['fn','x','y','z','doppler','numPts'])

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
port = serial.Serial("/dev/tty.usbmodem14103",baudrate = 115200, timeout = 0.5)
#port = serial.Serial("/dev/tty.SLAB_USBtoUART3",baudrate = 921600, timeout = 0.5)
#for NUC ubuntu 
#port = serial.Serial("/dev/ttyACM1",baudrate = 921600, timeout = 0.5)


radar = pc3.Pc3(port)

v6len = 0
v7len = 0
v8len = 0

pos = np.zeros((100,3))
color = [1.0, 0.0, 0.0, 1.0]
colorX = [0.0, 0.0, 1.0, 1.0]
sp1 = gl.GLScatterPlotItem(pos=pos,color=color,size = 4.0)
sp2 = gl.GLScatterPlotItem(pos=pos,color=color,size = 30.0)
w.addItem(sp1)
w.addItem(sp2)


#(v6smu,v7smu,v8smu) = radar.readFile("pc3az2021-05-04-11-23-02_2_paperhouse.csv")
#(v6smu,v7smu,v8smu) = radar.readFile("pc3az2021-05-04-11-10-03_3_10cm.csv")
(v6smu,v7smu,v8smu) = radar.readFile("pc3az2021-05-04-11-05-59_2_30cm.csv")
print("------------------ v6smu --------start:{:}  stop:{:}--------------".format(radar.sim_startFN,sim_stopFN))
print(v6smu)
print("------------------ v7smu ----------------------")
print(v7smu)
print("------------------ v8smu ----------------------")
print(v8smu)


#generate a color opacity gradient
pos1 = np.empty((50,3))
pos2 = np.empty((50,3))
uFlag = True
def update():
    ## update volume colors
	global pos1,lblA,color,uFlag,pos2,colorX
	
	if uFlag == True:
		uFlag = False
	#print(len(pos1))
		sp1.setData(pos=pos1,color=color)
		sp2.setData(pos=pos2,color=colorX)

t = QtCore.QTimer()
t.timeout.connect(update)
t.start(50)
fn = 0 
prev_fn = 0
lblA =[]

def radarExec():
	global v6len,v7len,v8len,pos1,prev_fn,color,flag,uFlag,sim_stopFN,objBuf,pos2
	v6 = []
	v7 = []
	v8 = []
	sample_point = 10
	
	flag = True
	(dck,v61,v71,v81)  = radar.tlvRead(False,df = 'DataFrame')
	#hdr = radar.getHeader()
	#radar.headerShow() # check sensor information
	#fn = hdr.frameNumber
	fn = radar.frameNumber
	(dck,v6,v7,v8)  = radar.getRecordData(fn)
	
	
	if  fn != prev_fn:

		prev_fn = fn
		v8len = len(v8)
		v6len = len(v6)
		v7len = len(v7)
		print("#############################################################") 
		print("# frameNum: sim_stopFN:{:}  workFrameNumber(sim_startFN:fn)=({:}+{:}) = {:}".format(radar.sim_stopFN,radar.sim_startFN,fn,fn+radar.sim_startFN ))
		print("# Sensor Data: [v6,v7,v8]:[{:d},{:d},{:d}]".format(v6len,v7len,v8len))
		print("#############################################################") 
	
		if v6len != 0 and flag == True:
			flag = False
			posTemp = v6
			v6Temp = v6
			v6op = v6Temp[(v6Temp.sx > -0.5) & (v6Temp.sx < 0.5) & (v6Temp.sy < 0.5) & (abs(v6Temp.doppler) > 0.07) ]
			d = v6op.loc[:,['sx','sy','sz']] 
			dd = v6op.loc[:,['sx','sy','sz','doppler']] 
			 
			#(1.2)DBSCAN 
			#d_std = StandardScaler().fit_transform(xy6A)
			if len(dd) > sample_point:
				d_std = StandardScaler().fit_transform(d)
				
				#db = DBSCAN(eps=1.4, min_samples=3).fit(d_std)
				#db = DBSCAN(eps= 2.0, min_samples=sample_point).fit(d_std) # 2.0
				db = DBSCAN(eps=0.15, min_samples=6).fit(d)  
				
				labels = db.labels_  #cluster ID
				
				dd_np = dd.to_numpy()
				
				#(1.3)insert labels to point cloud Array(stA) stA = [x,y,z,Doppler,labels]
				pcA = np.insert(dd_np,4,values=labels,axis= 1) #[x,y,z,Doppler,labels] 
				print("==[{:}]========== pcA =====d:{:}=======stA:{:}".format(fn,d.shape,pcA.shape))
				print(pcA)
				mask = (labels == -1)
				sensorA = []
				sensorA = pcA[~mask]
				print("==[{:}]====== sensorA ========={:}".format(fn,sensorA.shape))
				print(sensorA)
				lblA = sensorA[:,4]
				
				dm = d[~mask] #
				pos_np = dm.to_numpy()
				pos_np[:,2] += HIGH_OFFSET  
				#print(d)
				
				color = np.empty((len(lblA),4), dtype=np.float32)
				for i in range(len(lblA)):
					x = int(lblA[i])
					color[i] = colorSet[x] 
				
				#(draw 0: pos1)
				pos1 = pos_np
				
				lbs = labels[~mask] 
				print("###########################################")
				print("### mask set:{:}".format(set(lbs)))
				print("###########################################")
				cnt = 0
				for k in set(lbs):
					gpMask = (lbs == k)
					m = sensorA[gpMask]
					mA = (np.mean(m,axis=0))
					dpl_rms = 0
					
					print(mA)
					print("Get 3D Box: k:{:} box= \n{:}".format(k,get3dBox(sensorA[gpMask])))
					(x,xl,y,yl,z,zl,nop) = get3dBox(sensorA[gpMask])
					print("({:})ObjectArea(meter**2):{:}".format(k,xl*yl*10000))
				
					#(1.3)Target trace(push)
					dplr = 0
					objBuf = objBuf.append({'fn':fn,'x':mA[0],'y':mA[1],'z':mA[2],'doppler':mA[3],'numPts':len(m)} , ignore_index=True)
					locBuf.insert(0,fn)
				
					#(1.4) remove data from objBuf(pop) based on locBuf of contains
					if len(locBuf) > QUEUE_LEN:
						objBuf = objBuf.loc[objBuf.fn != locBuf.pop()]
						
					#print("============ ObjBuf ===========locBuf:length:{:}".format(len(locBuf)))
					#print(objBuf)
				
				
				#(draw 1: pos2)
				drawObj = objBuf.loc[:,['x','y','z']] 
				pos2_np = drawObj.to_numpy()
				pos2_np[:,2] += HIGH_OFFSET 
				pos2 = pos2_np
				
				
				uFlag = True
				flag = True
			else:
				
				#(1.4) remove data from objBuf(pop) based on locBuf of contains
				if len(locBuf) > 0:
					objBuf = objBuf.loc[objBuf.fn != locBuf.pop()]
				
				#(draw 1: pos2)
				drawObj = objBuf.loc[:,['x','y','z']] 
				pos2_np = drawObj.to_numpy()
				pos2_np[:,2] += 0.5
				pos2 = pos2_np
				
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
