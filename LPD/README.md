![Platform](https://img.shields.io/badge/Raspberry-Pi3-orange.svg)&nbsp;
![Platform](https://img.shields.io/badge/Raspberry-Pi4-orange.svg)&nbsp;
![Language](https://img.shields.io/badge/python-%3E3.6%20-green.svg)&nbsp;
![License](http://img.shields.io/badge/license-MIT-green.svg?style=flat)


# mmWave-LPD (Low range People Detect)-ES2.0
# Notes: mmWave Library supports: python Version >= 3.6

Current PI's OS is supports python 3.7.0

https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up/3

This repository contains the Batman Kit- 201(ISK) Sensing mmWave Sensor SDK Device Version:ES2.0 . The sample code below consists of instruction for using the mmWave lib. This mmWave-LPD Python Program will work with Long-Range People Detection based Batman BM201 mmWave Kit solution (BM201-LPD). This Python Program works with a Raspberry Pi 4 and/or NVIDIA Jetson Nano computer with Batman BM201-LPD Kit attached via Kit’s HAT Board; and that the BM201 Kit is an easy-to-use mmWave sensor evaluation kit for tracking multiple people’s movements simultaneously from 1meter ~ 50meter range with a high degree of accuracy suitable for privacy conscious applications; and where the Python Program would detect multiple people movements in a 3-Dimentional Area with ID tag, posX, posY, posZ, velx, vely, velz, accX, accY, accZ parameters, along with Point Clouds with elevation, azimuth, doppler, range, and snr parameters.
Note: this Python program uses matplotlib for people movement’s 3D plot, and that the current 3D plot update rate is lagging; and where a faster 3D plot library will be desired (while the parameter data are read in real-time as normal).

Hardware Sensor: 

    Batman BM201-LPD provid two types of data:

        BM201-LPD provids raw data as:

        Point Cloud Spherical(V6): range,azimuth,elevation,doppler
        Target Object (V7): tid,posX,posY,velX,velY,accX,accY,posZ,velZ,accZ
        Target Index (V8): tid and status
        Point Cloud Side Info (V9): snr,noise
	
	BM201-LPD key/value data as:
	
	outputdata = tid,posX,posY,posZ,velX,velY,velZ,accX,accY,accZ,state
    	tid: target ID 
	pos: position  m
	vel: velocity  m/s
	acc: acceleration  m/s2
        
# Physical Setup
        Setup Requirements:
        Elevate EVM:2.0~2.5m high
        Down tilt:~2-3 degree
![MainMenu 1](https://github.com/bigheadG/mmWave/blob/master/physical_setup_lpd.png)

        
# Installing

Library install for Python

    $sudo pip3 install mmWave

Library update:

    $sudo pip3 install mmWave -U

# Examples:
    Raw data:
        lpd_v09_raw_ex0.py is a example output V6(Point Cloud Spherical),V7(Target Object List),V8(Target Index), V9(Point Cloud Side Info) data
        
    key/value:
        lpd_v09_kv_3dbar.py use key/value to draw object in 3DBar 
        

# Data Structure(Raw Data):
## Lib import(Raw Data):

from mmWave import lpdISK
lpd = lpdISK.LpdISK(port)
   
V6: Point Cloud Spherical<br/>
Each Point Cloud list consists of an array of points, Each point data structure is defined as following
   
    point Struct:
        range:    float   #Range in meters
        azimuth:  float   #Azimuth in radians
        elevation: float  #Elevation in radians
        doppler:  float   #Doppler in m/s
    
        V6 =: [(range,azimuth,elevation,doppler),......]
        
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

        v9 structure: [(snr,noise'),....]    
        
    Function call: 
        (dck,v6,v7,v8,v9) = lpd.tlvRead(False)
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
    
    Based on IWR6843 (r,az,el) -> (x,y,z)
    el: elevation  <Theta bottom -> Obj  
    az: azimuth    <Theta Obj ->Y Axis 
    
    z = r * sin(el)
    x = r * cos(el) * sin(az)
    y = r * cos(e1) * cos(az)
 
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
    
    from mmWave import lpdISK
    
    key/Value:
    
    from mmWave import lpdISK_kv
    
  ### raspberry pi 3/pi 4 use ttyS0
    port = serial.Serial("/dev/ttyS0",baudrate = 921600, timeout = 0.5)
    
  ### Jetson Nano use ttyTHS1
	
	port = serial.Serial("/dev/ttyTHS1",baudrate = 921600, timeout = 0.5)
	and please modify: 
	
	#import RPi.GPIO as GPIO
	import Jetson.GPIO as GPIO

## define
    raw data:
    
    lpd = lpdISK.LpdISK(port)
    
    key/value:
    
    lpd = lpdISK_kv.LpdISK_kv(port)
     

## get LPD-ISK Sensor Data

    raw data:
    
        (dck,v6,v7,v8,v9)  = lpd.tlvRead(False)
        if dck:
            print(v6) #you will see v6 data
        
    key/value:
        
        (dck,pc3x) = pc3d.lpdRead(False)
        if dck:
            print(pc3x) #you will see objPoint infomation
    
## Reference:

https://github.com/bigheadG/mmWaveDocs/blob/master/68xx_long_range_people_det_user_guide.pdf
	
    


