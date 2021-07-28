# Vital Energy Detection Based on BM201-VED

This repository contains Batman mmWave-VED Vital Energy Detection SDK. The sample code below consists of instruction for using the mmWave lib. This mmWave-VED Python Program will work with Vital Energy Detection (VED) based Batman BM201-VED mmWave Kit solution. This Python Program works with Raspberry Pi 4, NVIDIA Jetson Nano, Windows/Linux Computer (such as Intel NUC PC), or a Mac Computer with Batman BM201-VED EVM Kit hardware; and it is capable of plotting a Range-Azimuth-Heatmap with a 64 x 48 Grid Matrix covering: Range of 3meter/64row (approx. 0.05meter per row) x Azimuth of 108degree/48column (approx. 2.25degree/column); and also capable of plotting a 3-Dimensional WaterFall Plot, and where the Z-axis will indicate the Vital Energy Level in range. Subsequently a programmer may write a program for detecting whether a particular region(s) is occupied by a Vital Target(s) in approx. 3meter x 3meter area. 
    
    
    Use VED to implement 
    Hardware: BM-201 
    Firmware: v5205R
    pypi lib: vehicleODR
    range: 3m x 3m


# example
    pyqtgraph_VED_waterfall.py           # Represented v8 heatmap data by waterfall
    pyqtgraph_VED_waterfall_record.py    #record v8 data 
    pyqtgraph_VED_waterfall_2d.py        # 
    
## Demo Video & Screen shot

    pyqtgraph_VED_waterfall_2d.py


https://user-images.githubusercontent.com/2010446/127278655-d739df53-fba4-4493-b6ea-2e337c102837.mp4

    pyqtgraph_VED_waterfall.py

https://user-images.githubusercontent.com/2010446/122055863-a3a6f980-ce1b-11eb-8fca-ad65fbbfb6db.mov

	

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
	**
	
	
## Import Library

	import serial
	from mmWave import vehicleODR  
	
# Define:
    radar = vehicleODR.VehicleODR(port)
  
# Port:
    port = serial.Serial("/dev/tty.usbmodemGY0043914",baudrate = 921600, timeout = 0.5)
    
    #for Jetson nano UART port
    #port = serial.Serial("/dev/ttyTHS1",baudrate = 921600, timeout = 0.5) 
    #
    #for pi 4 UART port
    #port = serial.Serial("/dev/ttyS0",baudrate = 921600, timeout = 0.5)
    #
    port = serial.Serial("/dev/tty.usbmodemGY0052534",baudrate = 921600, timeout = 0.5)
    port = serial.Serial("/dev/tty.usbmodem14103",baudrate = 115200 , timeout = 0.5)  
    port = serial.Serial("/dev/tty.usbmodemGY0050674",baudrate = 921600, timeout = 0.5)
    
    port = serial.Serial("/dev/tty.SLAB_USBtoUART3",baudrate = 921600, timeout = 0.5)  

    #for NUC ubuntu 
    port = serial.Serial("/dev/ttyACM1",baudrate = 921600, timeout = 0.5)
   
 # get data function
 
    (dck,v8,v9,v10) = radar.tlvRead(False)
    dck : True  : data avaliable
    False : data invalid
    v8:  Range Azimuth HeatMap
    v9:  Feature Vector (ALERT: not used in this lab)
    v10: Decision Vector
    
    
 # record cvs data file
    ved_yyyy-mm-dd-hh-MM-ss.csv
    
    ex:
    ved_2021-06-15-22-39-47.csv
    
## Reference:

1. LabGuide: https://github.com/bigheadG/mmWaveDocs/blob/master/(V52_VOD_A320)ODdemo_usersguide.pdf
