''' 
Traffic Monitoring Detection Roadway Sensing (ISK) for BM-201" : 2021/04/18
ex2:
Hardware: BM201-TRS kit


(1)Download lib and install packages:
install:
~#sudo pip3 intall mmWave
update:
~#sudo pip3 install mmWave -U

install numpy
~#sudo pip3 install numpy

instll tkinter
~#sudo pip3 install tkinter



Use two port UART:
	dataBaudRate   = 921600 
	configBaudRate = 115200

will generate dataSet:
	Roadwaytmd_yyyy-mm-dd-hh-mm-ss.csv
	
'''

import serial
import numpy as np

from mmWave import roadwayTMD_kv

from threading import Thread
import tkinter as tk

import csv
from datetime import date,datetime,time


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

########################## GUI Window ##################################
window = tk.Tk()

# Title setting
window.title('Roadway Traffic Monitoring Detection App')
#window.geometry('700x300')
window.columnconfigure(0, pad=10)
window.columnconfigure(1, pad=10)
window.columnconfigure(2, pad=10)
window.columnconfigure(3, pad=10)

#window.configure(background='gray')
#Row 0
labelMinX = tk.Label(window, text = "min X(m)")
labelMaxX = tk.Label(window, text = "max X(m)")
#labelMinX.grid(column=0, row=0, sticky=tk.W)
#labelMaxX.grid(column=2, row=0, sticky=tk.W)
labelMinX.grid(column=0, row=0)
labelMaxX.grid(column=2, row=0)

minXString = tk.StringVar()
entryMinX = tk.Entry(window, width=10, textvariable=minXString)
entryMinX.grid(column=1, row=0, padx=10)
minXString.set(-0.3)

maxXString = tk.StringVar()
entryMaxX = tk.Entry(window, width=10, textvariable=maxXString)
entryMaxX.grid(column=3, row=0, padx=10)
maxXString.set(3.0)

#Row 1
labelMinY = tk.Label(window, text = "min Y(m)")
labelMaxY = tk.Label(window, text = "max Y(m)")
labelMinY.grid(column=0, row=1)
labelMaxY.grid(column=2, row=1)

minYString = tk.StringVar()
entryMinY = tk.Entry(window, width=10, textvariable=minYString)
entryMinY.grid(column=1, row=1, padx=10)
minYString.set(0.0)

maxYString = tk.StringVar()
entryMaxY = tk.Entry(window, width=10, textvariable=maxYString)
entryMaxY.grid(column=3, row=1, padx=10)
maxYString.set(70.0)

#Row 2
labelMinS = tk.Label(window, text = "min Speed(Km/hr)")
labelMaxS = tk.Label(window, text = "max Speed(km/hr)")
labelMinS.grid(column=0, row=2)
labelMaxS.grid(column=2, row=2)

minSString = tk.StringVar()
entryMinS = tk.Entry(window, width=10, textvariable=minSString)
entryMinS.grid(column=1, row=2, padx=10)
minSString.set(-150.0)

maxSString = tk.StringVar()
entryMaxS = tk.Entry(window, width=10, textvariable=maxSString)
entryMaxS.grid(column=3, row=2, padx=10)
maxSString.set(-0.15)

#Row 3
resultString=tk.StringVar()
resultLabel = tk.Label(window, textvariable=resultString)
resultLabel.grid(column=0, columnspan=3, row=3, padx=10)

#Row 4
resultButton = tk.Button(window, text = 'Send Config Data', command=callbackFunc)
resultButton.grid(column=1, row=4, pady=10)

recordButton = tk.Button(window, text = 'Record', command=callbackFunc_record)
recordButton.grid(column=3, row=4, pady=10)

#Row 5
objString=tk.StringVar()
objLabel = tk.Label(window, textvariable=objString)
objLabel.config(font=("Courier", 44))
objLabel.grid(column=0, columnspan=3, row=5, padx=10, sticky=tk.W )

#Row 6
dataString=tk.StringVar()
dataLabel = tk.Label(window,textvariable=dataString)
dataLabel.config(font=("Courier", 30))
dataLabel.grid(column=0, columnspan=3, row=6, padx=10, sticky=tk.W)
#############################################
 

def objectRuleBasedReport(distance,doppler,area,nop):
	obj = "CAR"
	speed = -doppler*3600.0/1000.0
	#############################
	# JUDGE OBJECT BY RULE BASED
	#############################
					
	#from last test
	if speed > 82.8: # frameOffset 349..367
		obj = "NotObject"
	elif distance < 40 and distance >= 10 and nop <= 15 and nop >= 1: # and -doppler <= 3.0: #doppler
		obj = "MAN"
	elif distance < 40 and distance >= 10 and nop <= 2: 
		obj = "NotObject"
	elif distance < 60 and distance >= 50 and nop <= 2: 
		obj = "NotObject"
	elif distance < 20 and distance >= 10  and nop <= 3 and area >= 10: 
		obj = "NotObject"
	#elif area > 7.0:
	#	obj = "TRUCK"
	elif distance < 60 and distance >= 50 and nop >= 2: # added for TRUCK
		obj = "CAR"
	elif distance < 50 and distance >= 40 and nop >= 3: # added for TRUCK
		obj = "CAR"
	elif distance < 40 and distance >= 30 and nop >= 10: # added for TRUCK
		obj = "CAR"
	elif distance < 30 and distance >= 20 and nop >= 20: # added for TRUCK
		obj = "CAR"
	elif distance < 20 and distance >= 10 and nop >= 22: # added for TRUCK
		obj = "CAR"
	elif distance < 40 and distance >= 10 and nop >= 2 and area < 4.00 and speed >= 70: 
		obj = "NotObject"
	elif distance < 40 and distance >= 30 and nop >= 2 and area < 1.50: 
		obj = "MotorCycle"
	elif distance < 30 and distance >= 20 and nop >= 3 and area < 2.00: 
		obj = "MotorCycle"
	elif distance < 20 and distance >= 10 and nop >= 3 and area < 4.00: 
		obj = "MotorCycle"
	
	return (obj,distance,speed)


def getFileName():
	tt = datetime.now()
	dt = tt.strftime("%Y-%m-%d-%H-%M-%S") 
	return  "RoadwayTMD_{:}.csv".format(dt)


#Output:v21:['flow','fn','indexMax','index','x','y','range','doppler','area','ptsNum','cid']")
# ytA: [NotObject,MAN,MotorCycle,car,CAR]
ytA = {'NotObject':[1,0,0,0,0],'MAN':[0,1,0,0,0] ,'MotorCycle':[0,0,1,0,0] ,'car':[0,0,0,1,0],'CAR':[0,0,0,0,1]}

fieldsA = ['fn','x','y','range','doppler','area','ptsNum','NotObject','MAN','MotorCycle','car','CAR']

############## Baud Rate Setting ########### 

dataBaudRate = 921600 
configBaudRate = 115200

############################################

#port = serial.Serial("COM189",baudrate = 921600, timeout = 0.5)

port = serial.Serial("/dev/tty.usbmodemGY0052534",baudrate = dataBaudRate , timeout = 0.5)   # Data port
portCFG = serial.Serial("/dev/tty.usbmodemGY0052531",baudrate = configBaudRate , timeout = 0.5) # config port


callbackFunc()

trs = roadwayTMD_kv.roadwayTmdISK_kv(port)

def uartThread(name):
	global rec_Flag,fieldsA
	print("mmWave: {:} example:".format(name))
	port.flushInput()
	
	with open(getFileName(), 'w', newline='') as csvfile:
		writer = csv.writer(csvfile)
		writer.writerow(fieldsA)
		while True:
			(dck,v21)=trs.tmdRead(False) 
			if dck and len(v21) > 0:
					#print(v21)
				if v21.indexMax[0] != 0:
					#(1)extract data for operation
					opA = v21.loc[:,['fn','x','y','range','doppler','area','ptsNum']]
					objA = []
					opAn = opA.to_numpy()
					
					
					#(2)Judge Object based on range/doppler/ptsNum/area and Save Detected Object to csv file
					for i in range(len(opAn)):
						(obj,rng,speed)  = objectRuleBasedReport(opAn[i][1],opAn[i][2],opAn[i][3],opAn[i][4]) 
						print("================= result ===========================")
						print("object({:})  range:{:5.2f}m  speed:{:5.2f}km/hr".format(obj,rng,speed))
						print("====================================================")
						
						objString.set('# {:10s}'.format(obj))
						dataString.set('r={:3.0f}m,v={:5.0f}Km/Hr'.format(rng, speed))
						
						fn = opAn[i][0]
						x =  opAn[i][1]
						y =  opAn[i][2]
						ran = opAn[i][3]
						dop = opAn[i][4]
						area = opAn[i][5]
						ptsNum = opAn[i][6]
						
						if rec_Flag == True: 
							csvData = [fn,x,y,ran,dop,area,ptsNum] + ytA[obj] 
							writer.writerow(csvData)
							csvfile.flush()
							print(csvData)
					

thread1 = Thread(target = uartThread, args =("Traffic Monitoring Detection Roadway Sensing (TRS)",))
thread1.setDaemon(True)
thread1.start()
window.mainloop()
