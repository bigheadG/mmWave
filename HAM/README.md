# mmWave-HAM (High Accuracy Measurement)
This repository contains the Batman Kit- HAM mmWave Sensor SDK. 
The sample code below consists of instruction for using the mmWave lib.
This mmWave-HAM Python Program will work with High Accuracy Measurement (HAM) based mmWave Batman Kit solution.
This App works with Raspberry Pi 3 / Pi 2
The High Accuracy Measurement (HAM) based Batman Kit is for measuring object distance 
from the mmWave Sensor Module with the range of 30cm ~ 3meters(about 1~10 feet) 
with millimeter resolution.

https://

## Installing

Library install for python

	$sudo pip install mmWave
	$sudo pip3 install mmWave

Library update:

	$sudo pip install mmWave -U
	$sudo pip3 install mmWave -U

Examples:

	HAM_ex0.py is a basic example for reading data from Batman EVK
 	HAM_ex1_Thread.py is an example of using thread to read data from Batman EVK
 	HAM_ex2_intr18.py is an example of using GPIO Pin18 rise-edge to trigger function 
	to read data from Batman EVK

# Data Structure:

Header:

	class header: 
		version = ""
		totalPackLen =0
		tvlHeaderLen = 8
		platform = ""
		frameNumber = 0
		timeCpuCycles = 0
		numDetectedObj = 0
		numTLVs = 0
		
	function call: 
		getHeader(self)
		return header type data
				
Detected Objects:

	class dos: #Detected Object
		structureTag = 0
		lengthOfStruct  = 0 
		descriptor_val = 0
		descriptor_q = 0
		rangeEst_low = 0
		padding0_low = 0
		padding1_low = 0
		rangeEst_high = 0
		padding0_high = 0
		padding1_high = 0
		rangeValue = 0.0
	
	function call:
		getDetectedObject(self)
		return dos type data

Stats Information:

	class stats: #Stats Info
		stt = 0    #Structure Tag
		los = 0    #Length of Struct
		ifpt = 0.0 #Inter-frame Processing Time
		tot = 0.0  #Transmit Output Time
		ifpm = 0.0 #Inter-frame Processing Margin
		icpm = 0.0 #Inter-chirp Processing Margin
		afcl = 0.0 #Active Frame CPU Load
		icl = .0   #Interframe CPU Load

	function call: 
		getStatsInfo(self)
		return stats type data
				
# tlv Data:
function call:

	(chk,hd,rangeBuf) = tlvRead(dbg)

	dbg := True, enable debug message
	       False, disable debug message
         
	chk := True: Data valid
		   False: Data invalid
		   
	hd := Detected Objects Data (dos type)
	
	rangeBuf := Range Profile data. Contains the magnitude of Range FFTs
				Size: 512 RangeBins * 2
				RangesBins = (Real part for 4Bytes(float), Image part for 4 Bytes(float))
				totalBins = 512 Bins
				rangeBuf = [r0,i0,r1,i1,r2,i2.....r511,i511]
				Ex. point0 = sqrt(r0**2 + r0**2)
					point1 = sqrt(r1**2 + r1**2)
					....
				len(rangeBuf) = 1024 points => r:512points + i:512 points
				unit: meter


# import lib

	from mmWave import highAccuracy

# raspberry pi 3 use ttyS0
	port = serial.Serial("/dev/ttyS0",baudrate = 921600, timeout = 0.5)

# raspberry pi 2 use ttyAMA0
	port = serial.Serial("/dev/ttyAMA0",baudrate = 921600, timeout = 0.5)

# define 
ham = highAccuracy.HighAccuracy(port)

# get tlv Data
	get tlv data tlv:table-length-value
	
	(dck , hd, rangeBuf) = ham.tlvRead(False)

More detailed information please reference:
http://
