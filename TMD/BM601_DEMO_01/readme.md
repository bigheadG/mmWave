![Platform](https://img.shields.io/badge/Raspberry-Pi3-orange.svg)&nbsp;
![Platform](https://img.shields.io/badge/Raspberry-Pi4-orange.svg)&nbsp;
![Platform](https://img.shields.io/badge/ubuntu-NCU-orange.svg)&nbsp;
![Platform](https://img.shields.io/badge/Win-OS-blue)&nbsp;
![Platform](https://img.shields.io/badge/Mac-OS-lightgrey)&nbsp;
![Platform](https://img.shields.io/badge/Jeson-Nano-green.svg)&nbsp;
![Language](https://img.shields.io/badge/python-%3E3.6%20-green.svg)&nbsp;
![License](http://img.shields.io/badge/license-MIT-green.svg?style=flat)

# BM601
# mmWave-TMD I480 (Traffic Monitor Detector) 
# Notes: mmWave Library supports: python Version >= 3.6

Current PI's OS is supports python 3.7.0

https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up/3

This repository contains the Batman mmWave-TMD(I480) Traffic Monitoring Detection mmWave Sensor SDK with Device Version. The sample code below consists of instruction for using the mmWave lib. This mmWave-TMD_I480 Python Program works with Traffic Monitoring Detection (TMD) based Batman BM601-TMD_I480  mmWave Kit solution. This Python Program works with a Raspberry Pi 4 and/or NVIDIA Jetson Nano computer with Batman BM601-TMD Kit attached via Kit’s HAT Board; and that the BM601-TMD(I480) Kit is an easy-to-use mmWave sensor evaluation kit for tracking multiple object's movements simultaneously from 1meter ~ 50meter range with a high degree of accuracy suitable for traffic monitoring applications; and where the Python Program would detect multiple object/vehicle movements in a 3-Dimentional Area with ID tag, posX, posY, posZ, velx, vely, velz, accX, accY, accZ parameters, along with Point Clouds with elevation, azimuth, doppler, and range parameters.
Note: this Python program uses matplotlib for objects movement’s 3D plot, and that the current 3D plot update rate is lagging; and where a faster 3D plot library will be desired (while the parameter data are read in real-time as normal).

Hardware Sensor: 

    Batman BM601-TMD provides two types of data:

      BM601-TMD provides raw data as:

        	Point Cloud Spherical(V6): range,azimuth,elevation,doppler
        	Target Object (V7): tid,posX,posY,velX,velY,accX,accY,posZ,velZ,accZ
        	Target Index (V8): tid and status
		Point Cloud Side Info (V9): snr,noise<br/>
        
		tid: target ID 
		pos: position  m
		vel: velocity  m/s
		acc: acceleration  m/s^2
        
# Physical Setup
        Setup Requirements:
        Elevate EVM: 
        Down tilt: 
        
![MainMenu 1](https://github.com/bigheadG/imageDir/blob/master/physical_setup_lpd.png)

        
# Installing

Library install for Python

    $sudo pip3 install mmWave

Library update:

    $sudo pip3 install mmWave -U

# Examples:
	
    jb04_release_pyqtgraph_TMD_ex1.py is an example output V6(point cloud) and V7(Target Objects) demo.
        
(Demo01)

https://user-images.githubusercontent.com/2010446/143519031-0d363b57-f6ec-40f8-b511-7e3ff29c5ac6.mov

(Demo02)

https://user-images.githubusercontent.com/2010446/143519146-e87895cc-75f4-4073-9303-e68f75b9eafe.mov

(Demo03)

https://user-images.githubusercontent.com/2010446/143519216-0ee8e66c-3995-41ab-8b05-b0b6061dabca.mov




If Run demo program can not find any Raw data output:
      Please set UART to R/W mode: 
      
      pi 3
      $ls -l /dev/ttyS0
      $sudo chmod +777 /dev/ttyS0
      
      pi 2 
      $ls -l /dev/ttyS0
      $sudo chmod +777 /dev/ttyAMA0
      
      Jetson nano
      $ls -l /dev/ttyTHS1
      $sudo chmod +777 /dev/ttyTHS1

# Data Structure(Raw Data):
## Header:
        class header:
            version = 0
            platform = 0
            timeStamp = 0
            totalPacketLen = 0
            frameNumber = 0
            subFrameNumber = 0
            chirpMargin = 0
            frameMargin = 0 
            trackingProcessTime = 0
            uartSendingTime = 0
            numTLVs = 0
            checksum = 0

## Lib import(Raw Data):

	from mmWave import trafficMD_I480
	
	tmd = trafficMD_I480.TrafficMD_I480(port)
   
V6: Point Cloud<br/>
Each Point Cloud list consists of an array of points, Each point data structure is defined as following
   
    point Struct:
		range:    float   #Range in meters
		azimuth:  float   #Azimuth in radians
		elevation: float  #Elevation in radians
		doppler:  float  #Doppler in m/s
		sx: float #point position in X, m
		sy: float #point position in Y, m
		sz: float #point position in Z, m
		V6 =: [(range,azimuth,elevation,velocity,sx,sy,sz),......]
        
V7: Target Object<br/>
Each Target List consists of an array of targets. Each target data structure defind as following:
    
    target Struct:
        tid: Int        #Track ID
        posX: float     #Target position in X, m
        posY: float     #Target position in Y, m
        posZ: float     #Target position in Z, m
        velX: float     #Target velocity in X, m/s
        velY: float     #Target velocity in Y, m/s
        velZ: float     #Target velocity in Z, m/s
        accX: float     #Target acceleration in X, m/s^2
        accY: float     #Target acceleration in Y, m/s^2
        accZ: float     #Target acceleration in Z, m/s^2
	
        V7 =: [(posX,posY,velX,velY,accX,accY,posZ,velZ,accZ,tid),....]
	
        
V8: Target Index<br/>
Each Target List consists of an array of target IDs, A targetID at index i is the target to which point i of the previous frame's point cloud was associated. Valid IDs range from 0-249
        
    TargetIndex Struct:
        tragetID: Int #Track ID
        [targetID0,targetID1,.....targetIDn]
        
        Other Target ID values:
        253:Point not associated, SNR to weak
        254:Point not associated, located outside boundary of interest
        255:Point not associated, considered as noise
   
        V8 =: [id1,id2....]
    
V9:Point Cloud Side Info<br/>

        v9 structure: [(snr,noise),....]    
        
## Function call:

        (dck,v6,v7,v8,v9) = tmd.tlvRead(False)
        dck : True  : data avaliable
              False : data invalid
        v6: point cloud of array
        v7: target object of array
        v8: target id of array
        v9: point cloud side info array

        return dck,v6,v7,v8,v9
		
   	 -----------------
	 |  obj o  |+z  board
	 |       \ |
	 |      el\|
	 | +x<-----o
	 |   az     \
	 ----------- \ --
	 	      \+y
    
    Based on IWR6843/1843 3D(r,az,el) -> (x,y,z)
    el: elevation φ <Theta bottom -> Obj    
    az: azimuth   θ <Theta Obj ->Y Axis 
    
    z = r * sin(φ)
    x = r * cos(φ) * sin(θ)
    y = r * cos(φ) * cos(θ)
   
   
# Data Structure(DataFrame Type):
When tlvRead argument set df = 'DataFrame', v6,v7 and v8 will output DataFrame style data
    
    (dck,v6,v7,v8,v9) = tmd.tlvRead(False, df = 'DataFrame')
    
    Type V6:
    Each Point Cloud list consists of an array of points,Each point data structure is defined as following

        V6 fields :['fN','type','range','azimuth','elv','doppler','sx', 'sy', 'sz']
	
        fN: frame number
        type: 'v6'
        elv: float  #Elevation in radians
        azimuth:  float   #Azimuth in radians
        doppler:  float   #Doppler in m/s
        range:    float   #Range in meters
        sx : float #point position x
        sy : float #point position y
        sz : float #point position z

    Type V7: Target Object<br/>
    Each Target List consists of an array of targets. Each target data structure defind as following:
    
        V7 fields : ['fN','type','posX','posY','velX','velY','accX','accY','posZ','velZ','accZ','tid']

	fN: int       #Frame number
        type: 'v7'
        posX: float     #Target position in X, m
        posY: float     #Target position in Y, m
        posZ: float     #Target position in Z, m
        velX: float     #Target velocity in X, m/s
        velY: float     #Target velocity in Y, m/s
        velZ: float     #Target velocity in Z, m/s
        accX: float     #Target velocity in X, m/s2 
        accY: float     #Target velocity in Y, m/s2
        accZ: float     #Target velocity in Z, m/s2
        tid: Int        #Track ID
        
    Type V8: Target Index<br/>
        Each Target List consists of an array of target IDs, A targetID at index i is the target to which point i of the previous frame's point cloud was associated. Valid IDs range from 0-249
	
        V8 fields : ['fN','type','targetID']
	
    	TargetIndex Struct:
        tragetID: Int #Track ID
        [targetID0,targetID1,.....targetIDn]
        
        Other Target ID values:
        253:Point not associated, SNR to weak
        254:Point not associated, located outside boundary of interest
        255:Point not associated, considered as noise
        
        V8 =: [id1,id2....]
	
        
    Type V9: Point Cloud Side Info
        
        V9 fields : ['fN','type','snr','noise'] 
        fN: frame number
        type: 'V9'
        snr: Signal/Noise Ratio
        noise: Noise
    
    
     
# import lib
    from mmWave import trafficMD_I480
    
  ### raspberry pi 3/pi 4 use ttyS0
    port = serial.Serial("/dev/ttyS0",baudrate = 921600, timeout = 0.5)
    
  ### Jetson Nano use ttyTHS1
	port = serial.Serial("/dev/ttyTHS1",baudrate = 921600, timeout = 0.5)
    
  ### for macOS
      port = serial.Serial("/dev/tty.usbmodemGY00xxxx",baudrate = 921600, timeout = 0.5)
      
  ### for Ubuntu 
      port = serial.Serial("/dev/ttyACM1",baudrate = 921600, timeout = 0.5)
	
## define
     
    tmd = trafficMD_I480.TrafficMD_I480(port)
    

## Get TMD-ISK Sensor Data

    raw data:

        (dck,v6,v7,v8,v9) = tmd.tlvRead(False)
        if dck:
            print(v6) #you will see v6 data
        
    
## Reference:

1. LabGuide: [TMD-I480 Data Structure based on SDK3504 2021.09.16 pdf.pdf](https://github.com/bigheadG/mmWave/files/7176542/TMD-I480.Data.Structure.based.on.SDK3504.2021.09.16.pdf.pdf)


	
    


