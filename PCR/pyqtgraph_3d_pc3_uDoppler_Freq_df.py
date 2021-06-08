#=============================================
# File Name: pyqtgraph_3d_pc3_uDoppler_freq_df.py
#
# Requirement:
# Hardware: BM201-ISK or AOP
# Firmware: PC3
# config file: (V34_PC3_6m_100m)ISK_6m_default.cfg
# lib: pc3 
# plot tools: pyqtgraph
#
# (1)Plot point cloud(V6) in 3D figure 
# (2)Plot Cluster point in 10mx10m HeatMap
#		get V6 point cloud -> DBSCAN -> Object Cluster->
#       -> mapping to 10mx10m -> plot HeatMap
# type: Raw data
# Baud Rate: 921600
#
# fd = -2V/λ  where λ = c/f
# fd = -2 * c/f * V = -2 * Doppler/(3 * 1e8 / 61.25 * 1e9 ) 
# ex: fd(Hz) = -2 * Doppler/ 0.00489796  
#            = -408.3632 * Doppler
#=============================================

from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import pyqtgraph as pg
import numpy as np
import scipy.stats as stats
from mmWave import pc3
import serial
from threading import Thread
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import pandas as pd

################### Class #######################################
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
			
			
######################### Parameter Set ##################################
TARGET_OBJ = True     # False = point cloud  True = Target
Z_OFFSET = 1.0

SAMPLE_POINT = 20.0
X_HI_LIMIT = 1.5
X_LO_LIMIT = -1.5
Y_HI_LIMIT = 2.0
Y_LO_LIMIT = 0.0

##########################################################################

app = QtGui.QApplication([])
w = gl.GLViewWidget()
w.show()

####### camera position #######
w.setCameraPosition(distance=7, elevation=50, azimuth=90)
#size=50:50:50
g = gl.GLGridItem()
g.setSize(x=50,y=50,z=50)
#g.setSpacing(x=1, y=1, z=1, spacing=None)
w.addItem(g)

####### draw axis ######
axis = Custom3DAxis(w, color=(0.2,0.2,0.2,1.0))
axis.setSize(x=25, y=25, z=25)
xt = [0,5,10,15,20,25]  
axis.add_tick_values(xticks=xt, yticks=xt, zticks=xt)
w.addItem(axis)
w.setWindowTitle('Position Occupancy(Cluster/Point Cloud)')

####### create box to represent device ######
verX = 0.0625
verY = 0.05
verZ = 0.125
zOffSet = 1.0
verts = np.empty((2,3,3))
verts[0,0,:] = [-verX, 0, verZ + zOffSet]
verts[0,1,:] = [-verX, 0,-verZ + zOffSet]
verts[0,2,:] = [verX,  0,-verZ + zOffSet]
verts[1,0,:] = [-verX, 0, verZ + zOffSet]
verts[1,1,:] = [verX,  0, verZ + zOffSet]
verts[1,2,:] = [verX,  0, -verZ + zOffSet]
 
evmBox = gl.GLMeshItem(vertexes=verts,smooth=False,drawEdges=True,edgeColor=pg.glColor('r'),drawFaces=False)
w.addItem(evmBox)


######## create uDoppler HeatMap ######
winuD = pg.GraphicsLayoutWidget()
winuD.setWindowTitle('Object Doppler Map')


imguD = pg.ImageItem()
#imguD.setScaledMode()

#**********************************
radarFreq = 61.25 * 1e9 #61.25GHz
uDPara =  -2 * 1 / (3 * 1e8 /radarFreq)  #-408.3632
uD_Hi =  600 #Hz 1500   #  10
uD_Lo =  -1500 #Hz   # -10
uDOffset = uD_Hi #  10
uDLength = 200
uDScale_y = 1
 
sampleT = 0.1 #100ms 
ylabels = np.arange(uD_Lo,uD_Hi+1.0,1)
imguD.resetTransform()
imguD.setPos(0,uD_Lo/uDScale_y)
imguD.scale(0.1, (ylabels[-1] - ylabels[0])/(uDLength * uDScale_y))

puD = winuD.addPlot()
puD.setLabel('bottom', 'time', 'unit:sec')
puD.setLabel('left', 'uDoppler Frequency', 'Hz')
puD.addItem(imguD)

histuD = pg.HistogramLUTItem()
'''
histuD.gradient.restoreState(
        {'mode': 'rgb',
         'ticks': [(0.5, (0, 182, 188, 255)),
                   (1.0, (246, 111, 0, 255)),
                   (0.0, (75, 0, 113, 255))]})
                   
'''                  
histuD.gradient.restoreState(
        {'mode': 'rgb',
         'ticks': [(1.0, (255,  0, 0 , 255)),
                   (0.75, (255, 233, 0, 255)),
                   (0.5, (26, 255, 0, 255)),
                   (0.2, (0, 187, 255, 255)),
                   (0.0, (23, 0, 255, 255))]})
                   
                   
histuD.setImageItem(imguD)
winuD.addItem(histuD)
winuD.show()


#****** Position Occupancy Histogram ****

winH = pg.GraphicsLayoutWidget()
winH.setWindowTitle('Position Occupancy Heat Map')
img3 = pg.ImageItem()
img3.setScaledMode()

p3h = winH.addPlot()
p3h.setLabel('bottom', 'Position Occupancy(X)', 'unit:meter')
p3h.resize(800, 800)
p3h.setLabel('left', 'Y', 'unit:meter')

#scale 
yscale3 = 1.0
xscale3 = 1.0
img3.scale(xscale3,yscale3)

#p3h.setLimits(xMin=-5, xMax=5, yMin=10,yMax= 10)
p3h.addItem(img3)

hist3 = pg.HistogramLUTItem()
hist3.gradient.restoreState(
        {'mode': 'rgb',
         'ticks': [(1.0, (255,  0, 0 , 255)),
                   (0.75, (255, 233, 0, 255)),
                   (0.5, (26, 255, 0, 255)),
                    
                   (0.2, (0, 187, 255, 255)),
                   (0.0, (23, 0, 255, 255))]})
'''
hist3.gradient.restoreState(
        {'mode': 'rgb',
         'ticks': [(0.5, (0, 182, 188, 255)),
                   (1.0, (246, 111, 0, 255)),
                   (0.0, (75, 0, 113, 255))]})
'''
                   
                   
                   
hist3.setImageItem(img3)
winH.addItem(hist3)
winH.show()


#############################       UART     ##################################
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
#port = serial.Serial("/dev/tty.usbmodemGY0052534",baudrate = 921600*2, timeout = 0.5)
#for NUC ubuntu 
#port = serial.Serial("/dev/ttyACM2",baudrate = 921600, timeout = 0.5)

#port = serial.Serial("/dev/ttyUSB1",baudrate = 921600, timeout = 0.5)
port = serial.Serial("/dev/tty.SLAB_USBtoUART3",baudrate = 921600 , timeout = 0.5)
#
###############################################################################

radar = pc3.Pc3(port)

v6len = 0
v7len = 0
v8len = 0

pos = np.zeros((100,3))
color = [1.0, 0.0, 0.0, 1.0]
sp1 = gl.GLScatterPlotItem(pos=pos,color=color,size = 5.0)
w.addItem(sp1)

gcolorA = np.empty((100,4), dtype=np.float32)
#generate a color opacity gradient


def update():
	global gcolorA,sensorA,mapSum,dopplerA
	#extract Labels
	#print("labels len:{:}".format(sensorA.shape))
	sp1.setData(pos=sensorA[:,[0,1,2]],color=gcolorA)
	img3.setImage(mapSum)
	imguD.setImage(dopplerA)

t = QtCore.QTimer()
t.timeout.connect(update)
t.start(80.0/2.0)

colors = [[255,0,0,255], [0, 255, 0, 255],[248, 89, 253, 255], [89, 253,242, 255],[89, 253,253, 255],
			[253, 89,226, 255],[253, 229,204, 255],[51,255,255, 255],[229,204,255,255], [89,253,100, 255], 
			 [127,255,212, 255], [253,165,89, 255],[255,140,0,255],[255,215,0,255],[0, 0, 255, 255]]

########################################################################
#
# [cloudPoint] -> DBSCAN -> [cluster] -> dispatch Cluster points
#											to Map Array 
#	-> [Show Sum of map Array]
#  
########################################################################
mapSizeX = 10
mapSizeY = 10
offSetX = 5.0

sensorA = np.empty((100,6))
mapSum = np.zeros((mapSizeX,mapSizeY))
dopplerA = np.zeros((200,200))

#serialData: ([[x,y,z,range,Doppler,noise,labels]....])
def sensorA2Map(serialData):
	map_10x10 = np.zeros((mapSizeX,mapSizeY))
	for item in serialData:
		#print( "x:{:} y:{:} z:{:}".format(item[0],item[1],item[2]))
		if item[0] < 10 and item[1] < 10: 
			if (item[0] + offSetX) < 10:
				map_10x10[int(item[0] + offSetX),int(item[1])] += 1
	return map_10x10

mapA = np.zeros((3,mapSizeX,mapSizeY))

fn = 0 
prev_fn = 0


def radarExec():
	global v6len,v7len,v8len,pos1,gcolorA,zOffSet,sensorA,mapA,mapSum,dopplerA,prev_fn
	#sample_point = 7
	flag = True
	(dck,v6,v7,v8)  = radar.tlvRead(False,df = 'DataFrame') #radar.tlvRead(False) #
	
	hdr = radar.getHeader()
	#radar.headerShow() # check sensor information
	fn = hdr.frameNumber

	if fn != prev_fn:
		prev_fn = fn
		#radar.headerShow() # check sensor information
		v8len = len(v8)
		v6len = len(v6)
		v7len = len(v7)
		#print(v6)
		#print("Sensor Data: [v6,v7,v8]:[{:d},{:d},{:d}]".format(v6len,v7len,v8len))
		if v6len != 0:# and flag == True:
			flag = False
			
			#For x,y,z test
			#pos1[2] = (0,2,0) #y
			#pos1[1] = (3,0,0) #x
			#pos1[0] = (0,0,1) #z
			#(1)(x,y,z) in range limit
			 
			v6op = v6[(v6.sx > X_LO_LIMIT) & (v6.sx < X_HI_LIMIT) & (v6.sy < Y_HI_LIMIT) & (v6.doppler != 0)] if TARGET_OBJ == True else v6
			pct = v6op.loc[:,['sx','sy','sz','range','doppler','snr']]
			d = v6op.loc[:,['sx','sy','sz']]
			
			if len(d) > SAMPLE_POINT:
				d_std = StandardScaler().fit_transform(d)

				pos1X = pct
				#(1.1) Extract x,y,z,doppler,noise from V6
					 
				#(1.2)DBSCAN
				db = DBSCAN(eps=0.5, min_samples=SAMPLE_POINT).fit(d_std)
				#labels: -1: non-cluster point 
				labels = db.labels_
				
				
				'''
				# Number of clusters in labels, ignoring noise if present.
				n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
				print('Estimated number of clusters: %d' % n_clusters_)
				n_noise_ = list(labels).count(-1)
				print('Estimated number of noise points: %d' % n_noise_)
				labelSet = set(labels)
				print("Label Set:{:}".format(labelSet))
				'''
				
				pos1X_np = pos1X.to_numpy()
				pos1X_np[:,2] += Z_OFFSET
				
				#(1.3)insert labels to sensor temp Array(stA) stA = [pos1[X],labels]
				stA = np.insert(pos1X_np,6,values=labels,axis= 1) #[sx,sy,sz,range,Doppler,noise,labels]
				
				#(1.4) remove non-cluster point
				mask = (labels == -1)
				sensorA = stA[~mask]
				lbs = labels[~mask]
				print("frameNo:{:}  stA.shape:{:}  sensorA.shape:{:} lbs:{:}".format(hdr.frameNumber ,stA.shape, sensorA.shape,set(lbs)))
				
				#print(sensorA[:,4])
				#dpt = dopplerMapping2ArrayAcc(sensorA[:,4])
				#(1.4.1) insert 
				dpt = dopplerMapping2ArrayNormal(sensorA[:,4])
				dopplerA[:-1] = dopplerA[1:]
				dopplerA[-1] = dpt
				#print(dpt)
				
				#(1.5)assign color to cluster 
				gcolorA = np.empty((len(sensorA),4), dtype=np.float32)
				for i in range(len(lbs)):
					gcolorA = colors[lbs[i]%15]
				
				#(2)get Target Box:
				#get same label id
				
				'''
				for k in set(lbs):
					gpMask = (lbs == k)
					print("Get 3D Box: k:{:} box={:}".format(k,get3dBox(sensorA[gpMask])))
				'''
				
				#(3.0)sensorA data mapping to 10x10 map and insert to mapA(map Array)
				# mapA : 10x10x6
				if len(sensorA) > 0:
					mapA[:-1] = mapA[1:]
					mapA[-1] = sensorA2Map(sensorA)
					
					#(3.1) Sum map array
					# mapsum is data for Plot
					mapSum = np.sum(mapA,axis=0) 
				print("------------------------------------")
				#print(mapSum.transpose())
				
				#print("labels.count= {:} pos1X= {:} len={:}".format(len(labels),len(pos1X),len(gcolor)))
				print(mapA)
				flag = True
				
	port.flushInput()

def dopplerMapping2ArrayAcc(valA):
	length = 200
	offset = 100  #length/2.0
	ymax = 10
	ymin = -10
	scale = length/(ymax-ymin)
	xA = np.zeros(length)
	for item in valA:
		if item < 10 and item > -10: # and item != 0:
			idx = int(np.round( item * scale ,1)) 
			idx += offset
			xA[idx] += 1
	return xA


xline = np.linspace(uD_Lo,uD_Hi, uDLength)
sigma = uD_Hi * 0.1
def dopplerMapping2ArrayNormal(valA):
	global xline,uD_Lo,uD_Hi,sigma
	xA = np.zeros(uDLength)
	for item in valA:
		mu = item * uDPara #* 3 
		#print("mu:{:}".format(mu))
		if item < uD_Hi and item > uD_Lo and (item != 0):
			y = stats.norm.pdf(xline, mu, sigma) 
			#print("item={:} y={:}".format(item,y))
			xA+= y 
	#print(xA)
	return xA 
	
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
	return (xr,xl,yr,yl,zr,zl)
	
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
