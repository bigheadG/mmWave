# Vehicle Occupancy Detection Based on BM201-VOD

This repository contains Batman mmWave-VOD Vehicle Occupancy Detection and Child Presence Detection mmWave Sensor SDK. The sample code below consists of instruction for using the mmWave lib. This mmWave-VOD Python Program will work with Vehicle Occupancy Detection (VOD) based Batman BM201-VOD mmWave Kit solution. This App works with Raspberry pi 4, Jetson Nano, Intel NUC PC, etc. along with the Batman BM201-VOD EVM Kit hardware; and it is capable of plotting a Range-Azimuth-Heatmap with a 64 x 48 Grid Matrix covering: Range of 3meter/64row (approx. 0.047meter per row) x Azimuth of 120degree/48column (approx. 2.5degree/column).  Subsequently a programmer may write a program to group the Grid(s) into Zone(s) for detecting whether the particular Zone(s) is occupied by Target(s) for Vehicle Seat/Zone Occupany Detection, etc.

# System
    Raspberry pi 4.0
    Jetson Nano
    Windows PC + USB to UART Bridge
    Mac + USB to UART Bridge
    Intel NUC + USB to UART Bridge 
    
# Installing

Library install for Python:

    $sudo pip install mmWave
    $sudo pip3 install mmWave

Library update:

    $sudo pip install mmWave -U
    $sudo pip3 install mmWave -U

pySerial Library:

    $sudo pip3 install pySerial
 
Examples:

   BM201_V5205_VOD_ex1_heatMap_V5205_02R.py
   
   ![MainMenu 1](https://github.com/bigheadG/imageDir/blob/master/V5205_02R_VOD_Screenshot%20from%202021-01-05%2019-28-32_text.png)
    
    above screen shot based on running BM201_V5205_VOD_ex1_heatMap_V5205_02R.py 
 
   ![MainMenu 1](https://github.com/bigheadG/imageDir/blob/master/V5205_02R_VOD_Screenshot%20from%202021-01-05%2019-30-56_zoneDetected.png)
    
    above screen shot based on running BM201_V5205_VOD_ex1_heatMap_V5205_02R.py
 
## Header:

    class header:
	    totalPackLen = 0
	    platform = 0
	    frameNumber = 0
	    timeCpuCycles = 0
	    numDetectedObj = 0
	    numTLVs = 0

      
 ## Get mmWave Sensor data:
 
    from mmWave import vehicleODR    
    pm = vehicleODR.VehicleODR(port)
    (dck,v8,v9,v10) = pm.tlvRead(False)
    (pass_fail, v8, v9, v10)
    pass_fail: True: Data available    False: Data not available

  	Output: V8,V9,V10 data:(RAW)
    	V8 :Range Azimuth Heatmap TLV 
    	V9 :Feature Vector TLV 
    	V10:Decision Vector TLV 


## V8: Range Azimuth HeatMap
	
	Size: 64 x 48 sizeOf(Int)

	The occupancy Detection Range Azimuth Heatmap is a 2D array of short int, currently defined 
	as 64 range rows with 48 azimuth angles per row. the total range is defined at 3 meters, so
	the range resolution of each row is 3m/64 = 46.9mm. In terms of azimuth, zero degrees is 
	perpendicular to the antennas, with 60 degrees of view on each side. With 48 total angles, 
	there are 24 angles per 60 degrees on each side, or 2.55 degrees per angle.  

## V9: Feature Vector (ALERT: not used in this lab)

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

      V10: Struct {
        percent,  #float
        power,    #float
        rangeIdx,  #uint16 
        azimuthIdx #uint16
      }
     
	The Decision Vector is an array of bytes; one byte per zone. Each byte contains the value 1 
	if a positive (occupied) decision has been calculated. It is zero otherwise.
	

## Import Library

	import serial
	from mmWave import vehicleODR  
 
## UART setting: (ALERT: serial port name based on platform)

	# (1) Raspberry pi 4
	port = serial.Serial("/dev/ttyS0",baudrate = 921600, timeout = 0.5)

	# (2) Jetson nano
	port = serial.Serial("/dev/ttyTHS1",baudrate = 921600, timeout = 0.5)
		
	# (3) Windows PC
  	port = serial.Serial("COMXXX",baudrate = 921600, timeout = 0.5) 
	notes: COMXXX please check UART Port then change XXX
	 
  	# (4) MacOS use tty.usbmodem....
	port = serial.Serial("/dev/tty.usbmodemGY0052534",baudrate = 921600, timeout = 0.5)
	please use $ls /dev/tty* to check device and use "/dev/tty.usbmodemGY0052534"
	
	# (5) Intel NUC on ubuntu 
	port = serial.Serial("/dev/ttyACM1",baudrate = 921600, timeout = 0.5)

	
## Reference:

1. LabGuide: https://github.com/bigheadG/mmWaveDocs/blob/master/(V52_VOD_A320)ODdemo_usersguide.pdf
	
