![Platform](https://img.shields.io/badge/Raspberry-Pi3-orange.svg)&nbsp;
![Platform](https://img.shields.io/badge/Raspberry-Pi4-orange.svg)&nbsp;
![Platform](https://img.shields.io/badge/ubuntu-NCU-orange.svg)&nbsp;
![Platform](https://img.shields.io/badge/Win-OS-blue)&nbsp;
![Platform](https://img.shields.io/badge/Mac-OS-lightgrey)&nbsp;
![Platform](https://img.shields.io/badge/Jeson-Nano-green.svg)&nbsp;
![Language](https://img.shields.io/badge/python-%3E3.6%20-green.svg)&nbsp;
![License](http://img.shields.io/badge/license-MIT-green.svg?style=flat)

# 🚧  Under Construction 🚧 
# mmWave-pc3POS (People Counting Overhead Sensor SDK)

Current PI's OS is supports python 3.7.0

https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up/3

This repository contains the Batman mmWave-PC3 People Counting & Detection mmWave Sensor SDK. The sample code below consists of instruction for using the mmWave lib. This mmWave-PC3 Python Program will work with People Counting & Detection based Batman AOP-PC3 mmWave Kit solution. This Python Program works with a Raspberry Pi 4 and/or NVIDIA Jetson Nano computer with Batman AOP-PC3 Kit attached via Kit’s HAT Board; and that the BM501 Kit is an easy-to-use mmWave sensor evaluation kit for People Sensing, People Counting, or People Occupancy Density Estimation in approx. 6m x 6m area without privacy invasion; and where the Python Program would have multiple people detection in a 3-Dimentional Area with ID tag, posX, posY, posZ, velx, vely, velz, accX, accY, accZ parameters, along with Point Clouds with elevation, azimuth, doppler, range, and snr parameters. 

# AOP-PC3 Kit Mouting and Scene Conditions
    The EVM Sensor needs to be mounted at a heigh of 2.8-3.0m in the center of area of interest, with the sensor directly facing the ground. Notes: If you use Tripod to elevate the EVM, Please make sure that it has an extension arm(minimun 12-15 inches) to project the EVM away from the Triple stem.
    

# Hardware:
    Batman kit-501 (AOP)
    Measure Range: 6x6 meters
    Power supply: 5Vdc/3.0A 
    
# Installing

Library install for Python

    $sudo pip install mmWave
    $sudo pip3 install mmWave

Library update:

    $sudo pip install mmWave -U
    $sudo pip3 install mmWave -U

Examples:

    
    pc3OVH_pyqtgraph_3d_xyz_df_queue_v6.py  #point cloud
    pc3OVH_pyqtgraph_3d_xyz_df_queue_v7.py  #object tracking
    
https://user-images.githubusercontent.com/2010446/118780152-55efad80-b8be-11eb-9927-ee296dfaed8e.mov
    
    pc3OVH_record.py                            # record data 
    pc3OVH_pyqtgraph_3d_xyz_df_playback.py  # point cloud data playback
    
    
If Run demo program can not find any Raw data output:
      Please set UART to R/W mode: 
      
      pi 3
      $ls -l /dev/ttyS0
      $sudo chmod +777 /dev/ttyS0
      
      pi 2 
      $ls -l /dev/ttyS0
      $sudo chmod +777 /dev/ttyAMA0
      
      jetson
      $ls -l /dev/ttyTHS1
      $sudo chmod +777 /dev/ttyTHS1

 
 # import lib

    from mmWave import pc3OVH

  ### raspberry pi 4 use ttyS0
    port = serial.Serial("/dev/ttyS0",baudrate = 921600, timeout = 0.5)

    
  ### Jetson Nano use ttyTHS1
      port = serial.Serial("/dev/ttyTHS1",baudrate = 921600, timeout = 0.5)
    and please modify: 
    
  ### use USB-UART
    port = serial.Serial("/dev/ttyUSB0",baudrate = 921600, timeout = 0.5)
 
  ### Mac OS use tty.usbmodemxxxx
    port = serial.Serial("/dev/tty.usbmodemGY0052854",baudrate = 921600, timeout = 0.5)
  
  ### ubuntu NUC
    port = serial.Serial("/dev/ttyACM1",baudrate = 921600, timeout = 0.5)


## define

    radar = pc3OVH.Pc3OVH(port)

## Header:

    class header:
        version = 0
        totalPackLen = 0
        platform = 0
        frameNumber = 0
        subframeNumber = 0
        chirpMargin = 0
        frameMargin = 0 
        trackProcessTime = 0
        uartSendTime = 0
        numTLVs = 0
        checksum = 0

# Data Structure(Raw Data):
V6: Point Cloud<br/>
Each Point Cloud list consists of an array of points,Each point data structure is defined as following
   
    point Struct:
        elevation: float  #Elevation in radians
        azimuth:  float   #Azimuth in radians 
        doppler:  float   #Doppler in m/s
        range:    float   #Range in meters
        snr:      float   #SNR, ratio
        
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
        accX: float     #Target velocity in X, m/s2 
        accY: float     #Target velocity in Y, m/s2
        accZ: float     #Target velocity in Z, m/s2
        ec[16]: float   #Tracking error covariance matrix, 
                        [4x4] in range/azimuth/elevation/doppler coordinates
        g: float        #Gating function gain
        confidenceLevel: float #Confidence Level
        
V8: Target Index<br/> 
Each Target List consists of an array of target IDs, A targetID at index i is the target to which point i of the previous frame's point cloud was associated. Valid IDs range from 0-249
        
    TargetIndex Struct(V8):
        tragetID: Int #Track ID
        {targetID0,targetID1,.....targetIDn}
        
        Other Target ID values:
        253:Point not associated, SNR to weak
        254:Point not associated, located outside boundary of interest
        255:Point not associated, considered as noise
   
    Function call: 
        
        (dck,v6,v7,v8) = radar.tlvRead(False)
        dck : True  : data avaliable
              False : data invalid
        v6: point cloud of array
        v7: target object of array
        v8: target id of array

        return dck,v6,v7,v8 
      
        getHeader()
        headerShow()
        
    Based on IWR6843 3D(r,az,el) -> (x,y,z)
    el: elevation φ <Theta bottom -> Obj    
    az: azimuth   θ <Theta Obj ->Y Axis 
    
    z = r * sin(φ)
    x = r * cos(φ) * sin(θ)
    y = r * cos(φ) * cos(θ)
    
# Data Structure(DataFrame Type):
    When tlvRead argument set df = 'DataFrame', v6,v7 and v8 will output DataFrame style data
    
    (dck,v6,v7,v8) = radar.tlvRead(False, df = 'DataFrame')
    
    Type V6:
        ['fN','type','elv','azimuth','range','doppler','snr','sx', 'sy', 'sz']
        fN: frame number
        type: 'v6'
        elv: float  #Elevation in radians
        azimuth:  float   #Azimuth in radians
        doppler:  float   #Doppler in m/s
        range:    float   #Range in meters
        snr: #SNR, ratio
        sx : point position x
        sy : point position y
        sz : point position z
        
    Type v7:
        ['fN','type','posX','posY','posZ','velX','velY','velZ','accX','accY','accZ','ec0','ec1','ec2','ec3','ec4','ec5','ec6','ec7','ec8','ec9','ec10','ec11','ec12','ec13','ec14','ec15','g','confi','tid']
        
        fN: frame number
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
        ec[16]: float   #Tracking error covariance matrix, 
                        [4x4] in range/azimuth/elevation/doppler coordinates
        g: float        #Gating function gain
        confidenceLevel: float #Confidence Level  
        tid: Int        #Track ID
    
    Type v8: 
        ['fN','type','targetID']
        
        fN: frame Number
        type: 'v8'
        Other Target ID values:
        253:Point not associated, SNR to weak
        254:Point not associated, located outside boundary of interest
        255:Point not associated, considered as noise
        
# Read Record Data File for Analysis point cloud Step by Step.
    
    this subroutine work with Point Cloud tool kit PCA-001 then you can step by step to analysis point cloud:
    
    (1)Read record file
    readFile(fileName)
    (v6smu,v7smu,v8smu) = radar.readFile("pc3Aop2021-xx-xx-xx-xx-34.csv")
   
    (2)based on frameNumber output v6,v7 and v8 data
    getRecordData(frameNumber)
    (dck,v6,v7,v8) = radar.getRecordData(frameNumber)
    dck : True : data avaliable
    v6: point cloud of dataframe type data
    v7: target object of dataframe type data  
    v8: target id of dataframe type data
    
    
    
 ![MainMenu 1](https://github.com/bigheadG/imageDir/blob/master/objGeoSmall.png)
			


## Reference

 
1. LabGuide: https://github.com/bigheadG/mmWaveDocs/blob/master/3d_pplcount_user_guide.pdf



