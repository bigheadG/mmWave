# mmWave

This repository contains Batman mmWave-ZOD Zone Occupancy Detection mmWave Sensor SDK. The sample code below consists of instruction for using the mmWave lib. This mmWave-ZOD Python Program will work with Zone Occupancy Detection (ZOD) based Batman BM201-ZOD mmWave Kit solution. This App works with Raspberry pi 4 or Jetson Nano along with Batman BM201-ZOD Kit, and is capable of plotting a Range-Azimuth-Heatmap with a 64 x48 Grid Matrix covering: Range of 3meter/64row (approx. 0.047meter per row) x Azimuth of 120degree/48column (approx. 2.5degree/column).  Subsequently a programmer may write a program to group the Grid(s) into Zone(s) for detecting whether the particular Zone(s) is occupied by Target(s).

# System
    Raspberry pi 4.0
    Jetson Nano
    Windows + USB to UART Bridge
    Mac + USB to UART Bridge
    
# Installing

Library install for Python

    $sudo pip install mmWave
    $sudo pip3 install mmWave

Library update:

    $sudo pip install mmWave -U
    $sudo pip3 install mmWave -U
    
Examples:

    zod_ex0.py
    zod_ex1_heatMap.py
 
![MainMenu 1](https://github.com/bigheadG/imageRepo/blob/master/zodScreen.png)

## Header:
    class header:
	    version = 0
	    totalPackLen = 0
	    platform = 0
	    frameNumber = 0
	    timeCpuCycles = 0
	    numDetectedObj = 0
	    numTLVs = 0
	    subFrameIndex = 0
      
 ## Get mmWave Sensor data:
 
    (dck,v8,v9,v10,v11) = pm.tlvRead(False)
    (pass_fail, v8, v9, v10,v11)
    pass_fail: True: Data available    False: Data not available

  	Output: V8,V9,V10,V11 data:(RAW)")
    	V8 :Range Azimuth Heatmap TLV 
    	V9 :Feature Vector TLV 
    	V10:Decision Vector TLV 
  	V11:Vital Sign Vector TLV 

## V8: Range Azimuth HeatMap
	
	Size: 64 x 48 sizeOf(Int)

	The occupancy Detection Range Azimuth Heatmap is a 2D array of short int, currently defined 
	as 64 range rows with 48 azimuth angles per row. the total range is defined at 3 meters, so
	the range resolution of each row is 3m/64 = 4.69mm. In terms of azimuth, zero degrees is 
	perpendicular to the antennas, with 60 degrees of view on each side. With 48 total angles, 
	there are 24 angles per 60 defress on each side, or 2.55 degress per angle.  

## V9: Feature Vector

	Size: 5 x sizeOf(float)
	
	All values in the feature Vector are normalized by the Mean Vector and Standard Deviation Vectors.
	
	V9: Struct {
	   avgPower1, 	#float
	   avgPower2, 	#float
	   powerRatio1,	#float
	   powerRatio2, #float
	   crossCorr	#float	
	}
	
## V10 Decision Vector:

	The Decision Vector is an array of bytes; one byte per zone. Each byte contains the value 1 
	if a positive (occupied) decision has been calculated. It is zero otherwise.
	
## V11: Vital Signs Vector
	
	V11: Struct {
		unwrapped_waveform[2],  #float unwrapped phase values(plotted)
		heart_waveform[2],	#float Heart waveform values(plotted)
		breathing_waveform[2],  #float Breathing waveform values(plotted)
		heart_rate[2], 		#float Heart rate calculated value(displayed)
		breathing_rate[2]  	#float Breathing Rate calculated value(displayed)
	}
	

# import Library

	import serial
	from mmWave import vehicleOD
 
# UART setting:

	#Jetson nano
	port = serial.Serial("/dev/ttyTHS1",baudrate = 921600, timeout = 0.5)
	#raspberry pi 4
	port = serial.Serial("/dev/ttyS0",baudrate = 921600, timeout = 0.5)
	
	#windows
  	port = serial.Serial("COMXXX",baudrate = 921600, timeout = 0.5) 
		notes: COMXXX please check UART Port then change XXX
	 

  	# MacOS use tty.usbmodem....
	port = serial.Serial("/dev/tty.usbmodemGY0052534",baudrate = 921600, timeout = 0.5)
	please use $ls /dev/tty* to check file for example "/dev/tty.usbmodemGY0052534"
	
# Get Sensor Data

	pm = vehicleOD.VehicleOD(port)
	(dck,v8,v9,v10,v11) = pm.tlvRead(False)
	
	
## Reference:

1. LabGuide: https://github.com/bigheadG/mmWaveDocs/blob/master/V22_ZOD_Occupancy_VitalSigns_Detection_User_Guide.pdf
	
