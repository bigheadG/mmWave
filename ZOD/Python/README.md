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

 


  
