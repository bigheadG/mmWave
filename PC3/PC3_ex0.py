''' 
PC3_ex0: People Counting 3d-People Occupancy (ISK) for BM-201" : 2020/07/15
ex0:
Hardware: Batman-201 ISK

V6: Point Cloud Spherical
	v6 structure: [(range,azimuth,elevation,doppler),......]
	
V7: Target Object List
	V7 structure: [(tid,posX,posY,velX,velY,accX,accY,posZ,velZ,accZ),....]
	
V8: Target Index
	V8 structure: [id1,id2....]
	
V9:Point Cloud Side Info
	v9 structure: [(snr,noise'),....]

(1)Download lib:
install:
~#sudo pip intall mmWave
update:
~#sudo pip install mmWave -U
'''

import serial
import numpy as np
from mmWave import pc3
import serial
from sklearn.cluster import DBSCAN

#UART initial

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
port = serial.Serial("/dev/tty.usbmodemGY0052534",baudrate = 921600, timeout = 0.5)
#for NUC ubuntu 
#port = serial.Serial("/dev/ttyACM1",baudrate = 921600, timeout = 0.5)
#
############################################################################



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
zOffSet = 1.0

sensorA = np.empty((100,6))
mapSum = np.zeros((mapSizeX,mapSizeY))
mapA = np.zeros((3,mapSizeX,mapSizeY))

#serialData: ([[x,y,z,range,Doppler,noise,labels]....])
def sensorA2Map(serialData):
	map_10x10 = np.zeros((mapSizeX,mapSizeY))
	for item in serialData:
		#print( "x:{:} y:{:} z:{:}".format(item[0],item[1],item[2]))
		if item[0] < 10 and item[1] < 10: 
			map_10x10[int(item[0] + offSetX),int(item[1])] += 1
	return map_10x10

radar = pc3.Pc3(port)

def radarExec(name):
	global v6len,v7len,v8len,pos1,gcolorA,zOffSet,sensorA,mapA,mapSum
	print("mmWave: {:} example:".format(name))
	port.flushInput()
	while(True):
		flag = True
		(dck,v6,v7,v8)  = radar.tlvRead(False)

		#hdr = radar.getHeader()
		#radar.headerShow() # check sensor information
		if dck:
			v8len = len(v8)
			v6len = len(v6)
			v7len = len(v7)
		
			#print("Sensor Data: [v6,v7,v8]:[{:d},{:d},{:d}]".format(v6len,v7len,v8len))
			if v6len != 0 and flag == True:
				flag = False
				pct = v6
				#For x,y,z test
				#pos1[2] = (0,2,0) #y
				#pos1[1] = (3,0,0) #x
				#pos1[0] = (0,0,1) #z
			
				# v6 struct = [(e,a,d,r,sn),(e,a,d,r,sn),(e,a,d,r,sn)..]
				pos1X = np.empty((len(pct),6)) 
				gcolorA = np.empty((len(pct),4), dtype=np.float32)
			
				#(1.1) Extract x,y,z,doppler,noise from V6
				for i in range(len(pct)):
					zt = pct[i][3] * np.sin(pct[i][0]) + zOffSet
					xt = pct[i][3] * np.cos(pct[i][0]) * np.sin(pct[i][1])
					yt = pct[i][3] * np.cos(pct[i][0]) * np.cos(pct[i][1])
					pos1X[i] = (xt,yt,zt,pct[i][3],pct[i][2],pct[i][4]) #[x,y,z,range,Doppler,noise]
					
				#(1.2)DBSCAN 
				db = DBSCAN(eps=0.5, min_samples=8).fit(pos1X[:,[0,1,2]])
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
			
				#(1.3)insert labels to sensor temp Array(stA) stA = [pos1[X],labels]
				stA = np.insert(pos1X,6,values=labels,axis= 1) #[x,y,z,range,Doppler,noise,labels]
			
				#(1.4)remove non-cluster point
				mask = (labels == -1)
				sensorA = stA[~mask]
				lbs = labels[~mask]
				#print("stA.shape:{:}  sensorA.shape:{:}".format(stA.shape, sensorA.shape))
			
				#(2)get Target Box:
				#get same label id
				'''
				for k in set(lbs):
					gpMask = (lbs == k)
					print("Get 3D Box: k:{:} box={:}".format(k,get3dBox(sensorA[gpMask])))
				'''
			
				#(3.0)sensorA data mapping to 10x10 map and insert to mapA(map Array)
				# mapA : 10x10x6
				mapA[:-1] = mapA[1:]
				mapA[-1] = sensorA2Map(sensorA)
			
				#(3.1) Sum map array
				# mapsum is data for Plot
				mapSum = np.sum(mapA,axis=0) 
				print("------------------------------------")
				print(mapSum.transpose())
			
				#print("labels.count= {:} pos1X= {:} len={:}".format(len(labels),len(pos1X),len(gcolor)))
				#pos1 = sensorA[:,[0,1,2]]
				flag = True
		 
		port.flushInput()



radarExec("PC3 Position Occupancy Detector")





