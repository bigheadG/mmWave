![Platform](https://img.shields.io/badge/Raspberry-Pi3-orange.svg)&nbsp;
![Platform](https://img.shields.io/badge/Raspberry-Pi4-orange.svg)&nbsp;
![Language](https://img.shields.io/badge/python-%3E3.6%20-green.svg)&nbsp;
![License](http://img.shields.io/badge/license-MIT-green.svg?style=flat)

# mmWave-PC3D (People Overhead Counting 3D)-ES2.0  (Deprecated .. Merge to PC3_v2)
# Notes: mmWave Library supports: python Version >= 3.6

Current PI's OS is supports python 3.7.0

https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up/3

This repository contains the Batman Kit- 301(ODS) Overhead Detection Sensing_ mmWave Sensor SDK Device Version:ES2.0 .  The sample code below consists of instruction for using the mmWave lib. This mmWave-PC3D Python Program will work with People Overhead Counting(POC) and Fall Detection Sensing (FDS) based Batman BM301 mmWave Kit solution (BM301-POC or BM301-FDS). This Python Program works with a Raspberry Pi 4 and/or NVIDIA Jetson Nano computer or PC/MAC with Batman BM301-POC or BM301-FDS Kit attached; and that  the BM301 Kit is an easy-to-use mmWave sensor evaluation kit with miniaturized short-range antenna, and with wide horizontal and vertical Field of View (FoV), that connects directly to a Raspberry Pi or NVIDIA Jetson Nano computer via Kit's HAT Board, for detecting multiple objects in a 3-Dimentional Area with ID tag, posX, posY, posZ, Vx, Vy, Vz, accX, accY, accZ parameters and Point Clouds with elevation, azimuth, doppler, range, and snr parameters.

Hardware Sensor: 

    Batman BM301-FDS providd two types of data:

        BM301-FDS provids raw data as:
	
        Point Cloud (V6): posX,posY,posZ,Vx,Vy,Vz,accX,accY,accZ
        Target Object (V7): elevation,azimuth,doppler,range,snr
        Target Index (V8): tid and status
    
        BM301-FDS provids key/value data as:
	
        Target Object(V7) : id,posX,posY,posZ,velX,velY,velZ,accX,accY,accZ parameters.
         
![MainMenu 1](https://github.com/bigheadG/imageDir/blob/master/BM301-FDS-Mounted.png)
        
# Installing

Library install for Python

    $sudo pip3 install mmWave

Library update:

    $sudo pip3 install mmWave -U

# Examples:
    Raw data:
        pc3d_raw_v12_ex0.py is a example output V6(cloud point),V7(object target),V8(target id) data
        pc3d_raw_v12_pointCloud.py is a example use V6 to plot point cloud in 3D diagram (use matplotlib)
    key/value:
 
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
        accX: float     #Target velocity in X, m/s
        accY: float     #Target velocity in Y, m/s
        accZ: float     #Target velocity in Z, m/s
        
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
        (dck,v6,v7,v8) = pc3d.tlvRead(False)
        dck : True  : data avaliable
              False : data invalid
        v6: point cloud of array
        v7: target object of array
        v8: target id of array

        return dck,v6,v7,v8 
		
		
    Based on IWR6843 3D(r,az,el) -> (x,y,z)
    el: elevation φ <Theta bottom -> Obj    
    az: azimuth   θ <Theta Obj ->Y Axis 
    
    z = r * sin(φ)
    x = r * cos(φ) * sin(θ)
    y = r * cos(φ) * cos(θ)
 ![MainMenu 1](https://github.com/bigheadG/imageDir/blob/master/objGeoSmall.png)
 
 # Data Structure(Key/Value):
 
    Detected Object Data Format: <frameNum,numObjs,[op]>
    frameNum: Frame Number
    numObjs: number of Detected Object
    [op]: an Array of Detected Objects Point , the point includes position and object moving speed data
    op: objPoint class
    <frameNum,numObjs,op=[(tid0,x0,y0,z0,vx0,vy0,vz0,accx0,accy0,accz0,state0),(tid1,x1,y1,z1,vx1,vy1,vz1,accx1,accy1,accz1,state1),(tid2,x2,y2,z2,vx2,vy2,vz2,accx2,accy2,accz2,state2)...]>
    
    @dataclass
    class objPoint:
        tid: int 
        x: float
        y: float
        z: float = 0.0
        vx: float = 0.0
        vy: float = 0.0
        vz : float = 0.0
        accX : float = 0.0
        accY : float = 0.0
        accZ : float = 0.0
        state : int = 0
 
    notes:
        state: 1:stand 2:seat 3:lie down 5:falling
        
    @dataclass
    class objSets:
        frameNum: int
        numObjs: int
        op: [objPoint]


# import lib
    raw data:
    
    from mmWave import pc3d
    
    key/value:
    
    from mmWave import pc3d_kv

  ### raspberry pi 3/pi 4 use ttyS0
    port = serial.Serial("/dev/ttyS0",baudrate = 921600, timeout = 0.5)
    
  ### Jetson Nano use ttyTHS1
	
	port = serial.Serial("/dev/ttyTHS1",baudrate = 921600, timeout = 0.5)
	and please modify: 
	
	#import RPi.GPIO as GPIO
	import Jetson.GPIO as GPIO

## define
    raw data:
    
    pc3d = pc3d.Pc3d(port)
    
    key/value:
    
    pc3d = pc3d_kv.Pc3d_kv(port)

## get ODS Sensor Data

    raw data:
    
        (dck,v6,v7,v8)  = pc3d.tlvRead(False)
        if dck:
            print(v6) #you will see v6 data
        
    key/value:
    
        (dck ,pc3) = pc3d_kv.Read(False)
        if dck:
            print(pc3) #you will see v7 key/value data
    
## Reference:

1. LabGuide: https://github.com/bigheadG/mmWaveDocs/blob/master/(V12_PC3_ODS)Overhead_People_Tracking_and_Stance_Detection_users_guide.pdf

2. KeyDataProtocol: https://github.com/bigheadG/mmWaveDocs/blob/master/V12_Protocol%20for%203DPC_KEY_data%20Project%20V1201_pdf.pdf
	
3. Algorithm for Fall Detection based on rule based
https://github.com/bigheadG/mmWaveDocs/blob/master/Algorithm%20for%20Fall%20Detection%20based%20on%20Rule%20based%20v12.01.pdf


