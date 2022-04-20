#=============================================
# File Name: pyqtgraph_3d_pc3_uDoppler_json.py
#
# Requirement:
# Hardware: BM501-ISK or AOP
# Firmware: PC3_v2
# 
# lib: pc3 
# plot tools: pyqtgraph
#
# (1)Plot point cloud(V6) in 3D figure 
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
from mmWave import pc3_v2
#import pc3

import serial
from threading import Thread
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import pandas as pd
import JBUIWidget as jbui

import json 
import time
from datetime import date,datetime,time
import csv

########### read json file ######
with open('mmWave_uDoppler.json') as f:
	jdata = json.load(f)

################### Real Time/Playback & parameter setting   ######
WORKING_MODE = jdata["mmWave"]["working_mode"]["select"]  #select: real-time: 1  playback: 0   recording: 2  runtime(AI):3
FILE_TYPE =  jdata["mmWave"]["working_mode"]["fileType"]
REC_FILE  = jdata["mmWave"]["working_mode"]["playbackFile"]
PORT = jdata["mmWave"]["uart"]["port"] 
JB_RADAR_INSTALL_HEIGHT = jdata["mmWave"]["install_height"]["height"] / 100.0 #2.46 #
QUEUE_LEN = jdata['mmWave']['queueLen']['len']
LABELING_TYPE = jdata["mmWave"]["working_mode"]["labelingType"]


BAUD_RATE = 921600 if (WORKING_MODE == 1 or WORKING_MODE== 2 or WORKING_MODE == 3) else 115200
print("JB> Baud Rate:{:}".format(BAUD_RATE))

uD_Hi = jdata["mmWave"]["uDoppler"]["uD_hi"]   #unit:Hz
uD_Lo = jdata["mmWave"]["uDoppler"]["uD_lo"]   #unit:Hz
sigma = jdata["mmWave"]["uDoppler"]["sigma"]   #uD_Hi * 0.1
enable3D = jdata["mmWave"]["uDoppler"]["3DEnable"] 
######################### Parameter Set ##################################

RANGE_LIMIT = jdata["mmWave"]["v6"]["range_limit_flag"] 
SAMPLE_POINT =  jdata["mmWave"]["v6"]["DBSCAN_sampling_point"] #2.0
X_HI_LIMIT = jdata["mmWave"]["v6"]["range_x_hi"] / 100.0 #3.0
X_LO_LIMIT = jdata["mmWave"]["v6"]["range_x_lo"] / 100.0 #-3.0
Y_HI_LIMIT = jdata["mmWave"]["v6"]["range_z_hi"] / 100.0 #2.0
Y_LO_LIMIT = jdata["mmWave"]["v6"]["range_z_lo"] / 100.0 #-2.0

####################################################################

########################## GUI Method ##################################
def sendConfigData():
	strB = "jb_zoneCfg 1.0 -0.5 8.0 0.0 70.0 -150.0 -0.01"
	tail : bytes = b'\x0d\x0a'
	d = str.encode(strB) + tail
	portCFG.write(d)
	resultString.set(outString)

def callbackFunc():
	#resultString.set("{} - {}".format(landString.get(),cityString.get()))
	outString = "jb_zoneCfg 1.0 {} {} {} {} {} {}".format(
								minXString.get(),maxXString.get(),
								minYString.get(),maxYString.get(),
								minSString.get(),maxSString.get())
	tail : bytes = b'\x0d\x0a'
	d = str.encode(outString) + tail
	portCFG.write(d)
	print(outString)
	resultString.set(outString)
	
rec_Flag = False
def callbackFunc_record():
	global rec_Flag
	if recordButton['fg'] == 'black': # record
		recordButton['fg'] = 'red'
		print("Record Start")
		rec_Flag = True
	else:
		recordButton['fg'] = 'black'
		print("Record Stop")
		rec_Flag = False 

input_flag = False
def labelTypeSelect():
	global input_flag
	wFlag = True
	
	while wFlag:
		input_flag = True
		print("JB>================= [Labeling] ======================")
		print("JB> q: exit")
		print("JB>")
		for i in range(len(LABELING_TYPE)):
			print("JB> {:} : {:}".format(i,LABELING_TYPE[i]))
		print("JB>")
		select = input("JB> Please select(0...n):")
		label = ""
		if select == 'q':
			exit()
			
		if select.isdigit():
			label = select   #LABELING_TYPE[int(select)]
			label = select   #LABELING_TYPE[int(select)]
			print("JB>")
			print("JB>")
			print("==================== {:} [action id]  ======================".format(LABELING_TYPE[int(select)]))
			print("JB> (press to continue)")
			action_id = "JB>"
			action_id = input("JB> Please key in [action id]:")
			print("JB>")
			print("JB>")
		
		if label != "" and action_id != "":
			wFlag = 0
			input_flag = False
			return (label,action_id)
		

 


app = QtGui.QApplication([])

if enable3D == 1:
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
	axis = jbui.Custom3DAxis(w, color=(0.2,0.2,0.2,1.0))
	axis.setSize(x=25, y=25, z=25)
	xt = [0,5,10,15,20,25]  
	axis.add_tick_values(xticks=xt, yticks=xt, zticks=xt)
	w.addItem(axis)
	w.setWindowTitle('Position Occupancy(Cluster/Point Cloud)')

	####### create box to represent device ######
	utility = jbui.radar_utility()

	evmBox = gl.GLMeshItem(vertexes=utility.obj(),smooth=False,drawEdges=True,edgeColor=pg.glColor('r'),drawFaces=False)
	w.addItem(evmBox)
else:
	utility = jbui.radar_utility()

######## create uDoppler HeatMap ######
winuD = pg.GraphicsLayoutWidget()
winuD.setWindowTitle('Object Doppler Map')
winuD.setGeometry(100, 100, 1200, 400)

imguD = pg.ImageItem()
#imguD.setScaledMode()


#**********************************
radarFreq = 61.25 * 1e9 #61.25GHz
uDPara =  +2 * 1 / (3 * 1e8 /radarFreq)  #-408.3632
#uD_Hi =  600 #Hz 1500   #  10
#uD_Lo =  -600 #Hz   # -10
uDOffset = uD_Hi #  10


N200 = 500 #1000

uDLength = N200 #200
uDScale_y = 1
 
sampleT = 0.04 # 40ms
ylabels = np.arange(uD_Lo,uD_Hi+1.0,1)
imguD.resetTransform()
imguD.setPos(0,uD_Lo/uDScale_y)
#imguD.scale(0.1, (ylabels[-1] - ylabels[0])/(uDLength * uDScale_y))
imguD.scale(sampleT, (ylabels[-1] - ylabels[0])/(uDLength * uDScale_y))

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
'''
histuD.gradient.restoreState(
        {'mode': 'rgb',
         'ticks': [(1.0, (255,  0, 0 , 255)),
                   (0.75, (255, 233, 0, 255)),
                   (0.5, (26, 255, 0, 255)),
                   (0.2, (0, 187, 255, 255)),
                   (0.0, (23, 0, 255, 255))]})
                   (0.0, (23, 0, 255, 255))]})
'''                   
histuD.gradient.restoreState(
        {'mode': 'rgb',
         'ticks': [(0.45, (255,  0, 0 , 255)),
                   (0.20, (255, 233, 0, 255)),
                   (0.05, (26, 255, 0, 255)),
                   (0.01, (0, 187, 255, 255)),
                   (0.00, (0, 0, 255, 50))]})

                   
histuD.setImageItem(imguD)
winuD.addItem(histuD)
winuD.show()


#****** Position Occupancy Histogram ****
'''
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
                   
hist3.setImageItem(img3)
winH.addItem(hist3)
winH.show()
'''

############################# UART ##################################
port = serial.Serial(PORT,baudrate = BAUD_RATE , timeout = 0.5) 
radar = pc3_v2.Pc3_v2(port)

if WORKING_MODE == 0: #playback use
	_ = radar.readFile(REC_FILE)
	

fn = 0



#============region ===========
#lr = pg.LinearRegionItem([10, 40])
#lr.setZValue(-10)
lr = pg.LinearRegionItem([6, 8])
lr.setZValue(-5)

def regionUpdated(regionItem):
    lo,hi = regionItem.getRegion()
    right_hi = int(fn) + int(radar.sim_startFN)
    left_lo  = right_hi -  (int(hi) - int(lo)) * 4 
    print("JB> left:({:}),leftNum:{:}   right({:})  rightNum:{:}".format(int(lo),int(left_lo),int(hi),int(right_hi)))
    
    
puD.addItem(lr)
lr.sigRegionChanged.connect(regionUpdated)
#============region ===========


v6len = 0
v7len = 0
v8len = 0

pos = np.zeros((100,3))
color = [1.0, 0.0, 0.0, 1.0]

if enable3D == 1:
	sp1 = gl.GLScatterPlotItem(pos=pos,color=color,size = 5.0)
	w.addItem(sp1)

gcolorA = np.empty((100,4), dtype=np.float32)
#generate a color opacity gradient


def update():
	global gcolorA,sensorA,mapSum,dopplerA
	#extract Labels
	#print("labels len:{:}".format(sensorA.shape))
	
	#(1.0) scatterPlot data: sensorA
	if enable3D == 1:
		sp1.setData(pos=sensorA[:,[0,1,2]],color=gcolorA) 
	
	#(2.0) position heatMap  data: mapSum
	#img3.setImage(mapSum)
	
	#(3.0) uDoppler update   data: dopplerA
	imguD.setImage(dopplerA)
	
	#(4.0) AI run time mode
	if WORKING_MODE == 3: # AI runtime mode
		X = dopplerA[-50:-1]
		print(X.shape)

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
dopplerA = np.zeros((N200 + 50, N200))

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

pd.options.display.float_format = '{:,.2f}'.format

# show working time

JB_workingTime = 0
import time
cntt = 0
timeCnt = time.time()
prev = time.time() 

labeling = 0
action_id = 0
if WORKING_MODE == 2:
	(labeling , action_id) = labelTypeSelect()

print("JB> labeling:{:}  name_id:{:}".format(labeling,action_id))

				
def radarExec(writer = None):
	global v6len,v7len,v8len,pos1,gcolorA,zOffSet,sensorA,mapA,mapSum,dopplerA,prev_fn,prev,cntt,timeCnt,labeling,action_id

	#sample_point = 7
	if input_flag: 
		return
		
	flag = True
	(dck,v6,v7,v8)  = radar.tlvRead(False,df = 'DataFrame') #radar.tlvRead(False) #
	print(v6)
	hdr = radar.getHeader()
	#radar.headerShow() # check sensor information
	fn = hdr.frameNumber
	
	#print("JB> fn:{:}   prev_fn:{:}".format(fn,prev_fn))
	
	if WORKING_MODE == 0: #plakback
		if fn != prev_fn:
			print("JB>fn:{:}  tm:{:} : current:{:}-----start:{:}   stop:{:}".format(fn,time.time(),radar.sim_startFN+fn,radar.sim_startFN,radar.sim_stopFN))
			(dck,v6,v7,v8) = radar.getRecordData(fn)
			#print(v6)
		
	if fn != prev_fn:
		prev_fn = fn
		
		#radar.headerShow() # check sensor information
		#v8len = len(v8)
		v6len = len(v6)
		#v7len = len(v7)
		print(v6)
		#print("Sensor Data: [v6,v7,v8]:[{:d},{:d},{:d}]".format(v6len,v7len,v8len))
		if v6len != 0:# and flag == True:
			flag = False
			now = time.time()
			
			#(1)record data, write or not defined by json mode select
			#utility.recording(writer=writer,v6=v6)
			
			prev = now
			cntt += 1
			if cntt % (N200 + 50) == 0 and WORKING_MODE == 2:  # record mode
				print("JB>labeling:{:}  action_id:{:}   fn:{:}  tm:{:}  cnt:{:} timeCnt:{:}".format(labeling,action_id,fn,(now - prev),cntt ,  (now - timeCnt)))
				cntt = 0
				timeCnt = now
				(labeling , action_id) = labelTypeSelect()
				print("JB>")
				print("JB> ********* your labeling and action is following: labeling:{:}  name_id:{:}".format(labeling,action_id))
				print("JB>")
				dopplerA = np.zeros((N200 + 50, N200))
				
			print(v6)
			#For x,y,z test
			#pos1[2] = (0,2,0) #y
			#pos1[1] = (3,0,0) #x
			#pos1[0] = (0,0,1) #z
			#(1)(x,y,z) in range limit
			v6op = v6 
			#v6op = v6[(v6.sx > X_LO_LIMIT) & (v6.sx < X_HI_LIMIT) & (v6.sy < Y_HI_LIMIT) & (v6.doppler != 0)] if RANGE_LIMIT == True else v6
			v6op = v6[(v6.sx > X_LO_LIMIT) & (v6.sx < X_HI_LIMIT) & (v6.sy < Y_HI_LIMIT)] if RANGE_LIMIT == 1 else v6
			
			fNum = int(v6.values[0][0])
			print("JB> labeling: {:} action_id: {:} frameNum:{:}".format(labeling,action_id,fNum))
			
			
			pct  = v6op.loc[:,['sx','sy','sz','doppler','range','snr']]
			d    = v6op.loc[:,['sx','sy','sz']]
			
			
			#if len(d) > SAMPLE_POINT:
			if len(d) > 0:
				#d_std = StandardScaler().fit_transform(d)

				pos1X = pct
				#(1.1) Extract x,y,z,doppler,noise from V6

				'''
				#(1.2)DBSCAN
				db = DBSCAN(eps=0.5, min_samples=SAMPLE_POINT).fit(d_std)
				#labels: -1: non-cluster point 	
				labels = db.labels_
				'''
				
				'''
				# Number of clusters in labels, ignoring noise if present.
				n_clusters_ = len(set(labels)) - (1 if -1 in labels else 0)
				print('Estimated number of clusters: %d' % n_clusters_)
				n_noise_ = list(labels).count(-1)
				print('Estimated number of noise points: %d' % n_noise_)
				labelSet = set(labels)
				print("Label Set:{:}".format(labelSet))
				'''
				
				
				# pos1X_np:['sx','sy','sz','doppler','range','snr']
				pos1X_np = pos1X.to_numpy()
				pos1X_np[:,2] += JB_RADAR_INSTALL_HEIGHT
				
				'''
				#(1.3)insert labels to sensor temp Array(stA) stA:[pos1[X],labels]
				stA = np.insert(pos1X_np,6,values=labels,axis= 1) #stA:[sx,sy,sz,Doppler,range,noise,labels]
				
				#(1.4) remove non-cluster point
				mask = (labels == -1)
				sensorA = stA #stA[~mask]
				lbs = labels[~mask]
				print("frameNo:{:}  stA.shape:{:}  sensorA.shape:{:} lbs:{:}".format(hdr.frameNumber ,stA.shape, sensorA.shape,set(lbs)))
				'''
				
				stA = pos1X_np
				sensorA = stA #stA[~mask]
				
				#print(sensorA[:,3])
				#(1.4.1) insert 
				dpt = dopplerMapping2ArrayNormal(sensorA[:,3])
				print("dopplerA.shape: {:}  dpt.shape:{:}    sensorA.shape:{:}".format(dopplerA.shape,dpt.shape,sensorA.shape))
				dopplerA[:-1] = dopplerA[1:]
				dopplerA[-1] = dpt
				
				if labeling != "" and action_id != "" and WORKING_MODE == 2: 
					# ["walk","boxing","jump","others"]
					utility.recording_uD(writer = writer, uD = dpt.tolist() , fN = fNum ,label = labeling,action_id = action_id)

				#print("JB> dopplerA:{:}".format(dopplerA.shape))
				#print(dpt)
				
				'''
				#(1.5)assign color to cluster 
				gcolorA = np.empty((len(sensorA),4), dtype=np.float32)
				for i in range(len(lbs)):
					gcolorA = colors[lbs[i]%15]
				'''
				
				#(2)get Target Box:
				#get same label id
				
				'''
				for k in set(lbs):
					gpMask = (lbs == k)
					print("Get 3D Box: k:{:} box={:}".format(k,get3dBox(sensorA[gpMask])))
				'''
				
				#(3.0)sensorA data mapping to 10x10 map and insert to mapA(map Array)
				# mapA : 10x10x6
				'''
				if len(sensorA) > 0:
					mapA[:-1] = mapA[1:]
					mapA[-1] = sensorA2Map(sensorA)
					
					#(3.1) Sum map array for position heat map
					# mapsum is data for Plot
					mapSum = np.sum(mapA,axis=0) 
				print("------------------------------------")
				#print(mapSum.transpose())
				
				#print("labels.count= {:} pos1X= {:} len={:}".format(len(labels),len(pos1X),len(gcolor)))
				#print(mapA)
				'''
				flag = True
				
	port.flushInput()

'''
def dopplerMapping2ArrayAcc(valA):
	length = N200
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
'''

xline = np.linspace(uD_Lo,uD_Hi, uDLength)

def dopplerMapping2ArrayNormal(valA):
	global xline,uD_Lo,uD_Hi,sigma
	xA = np.zeros(uDLength)
	for item in valA:
		mu = item * uDPara 
		#print("mu:{:}".format(mu))
		
		if item < uD_Hi and item > uD_Lo and (item != 0):
			y = stats.norm.pdf(xline, mu, sigma) 
			#print("item={:} y={:}".format(item,y))
			xA+= y
		'''
		if item < uD_Hi and item > uD_Lo and (item != 0):
			y = - mu / 1000.0 
			#print("item={:} y={:}".format(item,y))
			xA+= y
		'''
	#print(xA.shape)
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
	if WORKING_MODE == 2: #0: playback  1:real_time  2:record 3: AI
		with open(utility.getFileName(), 'w', newline='') as csvfile:
			if FILE_TYPE == 0:
				fieldsA = ['frameNum','labelType','action_id','doppler']
			else:
				fieldsA = ['time','frameNum','type','elv/px','azimuth/py','doppler/pz','range/vx','snr/vy','sx/vz','sy/ax','sz/ay','na/az','na/ID']
			writer = csv.writer(csvfile)
			writer.writerow(fieldsA)
			while True:
				radarExec(writer=writer)
				csvfile.flush()
	if WORKING_MODE != 2 : #0:playback  1:real_time 3: AI
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
