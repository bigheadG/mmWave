![Platform](https://img.shields.io/badge/Raspberry-Pi3-orange.svg)&nbsp;
![Platform](https://img.shields.io/badge/Raspberry-Pi4-orange.svg)&nbsp;
![Platform](https://img.shields.io/badge/ubuntu-NCU-orange.svg)&nbsp;
![Platform](https://img.shields.io/badge/Win-OS-blue)&nbsp;
![Platform](https://img.shields.io/badge/Mac-OS-lightgrey)&nbsp;
![Platform](https://img.shields.io/badge/Jeson-Nano-green.svg)&nbsp;
![Language](https://img.shields.io/badge/python-%3E3.6%20-green.svg)&nbsp;
![License](http://img.shields.io/badge/license-MIT-green.svg?style=flat)


# mmWave-TMD (Traffic Monitor Detector)-ES2.0
# Notes: mmWave Library supports: python Version >= 3.6

Current PI's OS is supports python 3.7.0

https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up/3

This repository contains the Batman Kit- 201(ISK) Sensing mmWave Sensor SDK Device Version:ES2.0 . The sample code below consists of instruction for using the mmWave lib. This mmWave-TMD Python Program will work with Traffice Monitor Detector based Batman BM201 mmWave Kit solution (BM201-TMD). This Python Program works with a Raspberry Pi 4 and/or NVIDIA Jetson Nano computer with Batman BM201-TMD Kit attached via Kit’s HAT Board; and that the BM201 Kit is an easy-to-use mmWave sensor evaluation kit for tracking multiple object’s movements simultaneously from 1meter ~ 50meter range with a high degree of accuracy suitable for privacy conscious applications; and where the Python Program would detect multiple people movements in a 2-Dimentional Area with ID tag, posX, posY, posZ, velx, vely, velz, accX, accY, accZ parameters, along with Point Clouds with elevation, azimuth, doppler, range, and snr parameters.
Note: this Python program uses matplotlib for objects movement’s 3D plot, and that the current 3D plot update rate is lagging; and where a faster 3D plot library will be desired (while the parameter data are read in real-time as normal).

Hardware Sensor: 

    Batman BM201-TMD provid two types of data:

      BM201-TMD provids raw data as:

        	Point Cloud Spherical(V6): range,azimuth,elevation,doppler
        	Target Object (V7): tid,posX,posY,velX,velY,accX,accY,posZ,velZ,accZ
        	Target Index (V8): tid and status
		Point Cloud Side Info (V9): snr,noise<br/>
        
		tid: target ID 
		pos: position  m
		vel: velocity  m/s
		acc: acceleration  m/s2
        
# Physical Setup
        Setup Requirements:
        Elevate EVM: 
        Down tilt: 
        
![MainMenu 1](https://github.com/bigheadG/mmWave/blob/master/physical_setup_lpd.png)

        
# Installing

Library install for Python

    $sudo pip3 install mmWave

Library update:

    $sudo pip3 install mmWave -U

# Examples:

        TMD_ex0.py is an example output V6(Point Cloud),V7(Target Objects),V8(Target Index), V9(Point Cloud Side Info) data
        pyqtgraph_TMD_ex1.py is an example show point cloud in real time graphic use pyqtgraph
        TMD_ex2_pointCloud.py is an example plot point cloud in 3D use matplotlib
	pyqtgraph_3d_tmd.py is an example plot point cloud in 3D use pyqtgraph. The display speed is fast than matplotlib
    

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
            totalPackLen = 0
            platform = 0
            totalPacketLen = 0
            frameNumber = 0
            subFrameNumber = 0
            chirpMargin = 0
            frameMargin = 0 
            trackProcessTime = 0
            uartSendTime = 0
            numTLVs = 0
            checksum = 0

## Lib import(Raw Data):

from mmWave import trafficMD
tmd = trafficMD.TrafficMD(port)
   
V6: Point Cloud<br/>
Each Point Cloud list consists of an array of points, Each point data structure is defined as following
   
    point Struct:
        range:    float   #Range in meters
        azimuth:  float   #Azimuth in radians
        elevation: float  #Elevation in radians
        velocity:  float   #Doppler in m/s
    
        V6 =: [(range,azimuth,elevation,velocity),......]
        
V7: Target Object<br/>
Each Target List consists of an array of targets. Each target data structure defind as following:
    
    target Struct:
        tid: Int        #Track ID
        posX: float     #Target position in X, m
        posY: float     #Target position in Y, m
        velX: float     #Target velocity in X, m/s
        velY: float     #Target velocity in Y, m/s
        accX: float     #Target velocity in X, m/s
        accY: float     #Target velocity in Y, m/s
        posZ: float     #Target position in Z, m
        velZ: float     #Target velocity in Z, m/s
        accZ: float     #Target velocity in Z, m/s
        
        V7 =: [(tid,posX,posY,velX,velY,accX,accY,posZ,velZ,accZ),....]
        
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
    
    Based on IWR6843 3D(r,az,el) -> (x,y,z)
    el: elevation φ <Theta bottom -> Obj    
    az: azimuth   θ <Theta Obj ->Y Axis 
    
    z = r * sin(φ)
    x = r * cos(φ) * sin(θ)
    y = r * cos(φ) * cos(θ)
 
 
# import lib

    from mmWave import trafficMD
    
  ### raspberry pi 3/pi 4 use ttyS0
    port = serial.Serial("/dev/ttyS0",baudrate = 921600, timeout = 0.5)
    
  ### Jetson Nano use ttyTHS1
	port = serial.Serial("/dev/ttyTHS1",baudrate = 921600, timeout = 0.5)
    
  ### for macOS
      port = serial.Serial("/dev/tty.usbmodemGY00xxxx",baudrate = 921600, timeout = 0.5)
      
  ### for Ubuntu 
      port = serial.Serial("/dev/ttyACM1",baudrate = 921600, timeout = 0.5)
	
## define
     
    tmd = trafficMD.TrafficMD(port)
    

## Get TMD-ISK Sensor Data

    raw data:

        (dck,v6,v7,v8,v9) = tmd.tlvRead(False)
        if dck:
            print(v6) #you will see v6 data
        
    
## Reference:

1. LabGuide: https://github.com/bigheadG/mmWaveDocs/blob/master/V20_TMD_18xx_68xx_traffic_monitoring_users_guide.pdf

2. KeyDataProtocol: https://github.com/bigheadG/mmWaveDocs/blob/master/V20_TMD_Protocol_v20_11_pdf.pdf
	
    


