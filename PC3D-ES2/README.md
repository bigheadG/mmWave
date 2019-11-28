# mmWave-PC3D (People Overhead Counting 3D)-ES2.0 (Coming Soon...)
# Notes: mmWave Library supports: python Version >= 3.6

Current PI's OS is supports python 3.7.0

https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up/3

This repository contains the Batman Kit- 301(ODS) Overhead Detection Sensing mmWave Sensor SDK Device Version:ES2.0
The sample code below consists of instruction for using the mmWave lib.
This mmWave-PC3D Python Program will work with People Overhead Counting(POC) based mmWave Batman BM301 Kit solution.
This App works with Raspberry pi 4 and NVIDIA Jetson Nano
Batman Kit-301-ODS-POC (or the Batman BM301 Kit) is an easy-to-use mmWave sensor evaluation kit with miniaturized short-range antenna, and with wide horizontal and vertical Field of View (FoV), that connects directly to a Raspberry Pi or NVIDIA Jetson Nano computer via Kit's HAT Board, 
for decting multiple objects in a 3-Dimentional Area with ID tagged, posX,posY,posZ,Vx,Vy,Vz,accX,accY,accZ parameters and  Point Clouds with elevation,azimuth,doppler,range,snr parameters.

Hardware Sensor: 

    Batman BM301-FDS providd two types of data:

        BM301-FDS provids raw data as:
	
        Point Cloud (V6): posX,posY,posZ,Vx,Vy,Vz,accX,accY,accZ
        Target Object (V7): elevation,azimuth,doppler,range,snr
        Target Index (V8): tid and status
    
        BM301-FDS provids key/value data as:
	
        Target Object(V7) : id,posX,posY,posZ,velX,velY,velZ,accX,accY,accZ parameters. 
    
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
        

# Data Structure(Raw Data):
    V6: Point Cloud 
    Each Point Cloud list consists of an array of points, Each point data structure is defined as following
   
    point Struct:
        elevation: float  #Elevation in radians
        azimuth:  float   #Azimuth in radians 
        doppler:  float   #Doppler in m/s
        range:    float   #Range in meters
        snr:      float   #SNR, ratio
        
    V7: Target Object
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
        
    V8: Target Index
    Each Target List consists of an array of target IDs, A targetID at index i is the target to which point i of the previous frame's point cloud was associated. Valid IDs range from 0-249
        
    TargetIndex Struct:
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
		
    -----------------
    |  obj o  |+z  board
    |       \ |  
    |      el\| 
    | +x<-----o        
    |   az     \
    ----------- \ --
                 \+y
    
    Based on IWR6843 3D(r,az,el) -> (x,y,z)
    el: elevation  <Theta bottom -> Obj  
    az: azimuth    <Theta Obj ->Y Axis 
    
    z = r * cos(pi/2 - el)
    x = r * sin(el) * cos(pi/2 - az)
    y = r * sin(e1) * sin(pi/2 - az)
 
 # Data Structure(Key/Value):
 
    Detected Object Data Format: <frameNum,numObjs,[op]>
    frameNum: Frame Number
    numObjs: number of Detected Object
    [op]: an Array of Detected Objects Point , the point includes position and object moving speed data
    op: objPoint class
    <frameNum,numObjs,op=[(tid0,x0,y0,z0,vx0,vy0,vz0,accx0,accy0,accz0),(tid1,x1,y1,z1,vx1,vy1,vz1,accx1,accy1,accz1),(tid2,x2,y2,z2,vx2,vy2,vz2,accx2,accy2,accz2)...]>
    
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
	
    


