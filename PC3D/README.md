# mmWave-PC3D (People Overhead Counting 3D)
# Notes: Library only supports: python Version >= 3.6
This repository contains the Batman Kit- 301(ODS) Overhead Detection Sensing mmWave Sensor SDK. 
The sample code below consists of instruction for using the mmWave lib.
This mmWave-PC3D Python Program will work with People Overhead Counting(POC) based mmWave Batman BM301 Kit solution.
This App works with Raspberry Pi 3 / Pi 2 /pi 4 and NVIDIA Jetson Nano
Batman Kit-301-ODS-POC (or the Batman BM301 Kit) is an easy-to-use mmWave sensor evaluation kit with miniaturized short-range antenna, 
and with wide horizontal and vertical Field of View (FoV), that connects directly to a Raspberry Pi or NVIDIA Jetson Nano computer via Kit's HAT Board, 
for decting people movement behavior in a 3-Dimentional Area with ID tagged x,y,z,Vx,Vy,Vz (Doppler),dimX,dimY,dimZ parameters. 


# Installing

Library install for Python

    $sudo pip install mmWave
    $sudo pip3 install mmWave

Library update:

    $sudo pip install mmWave -U
    $sudo pip3 install mmWave -U

Examples:

    pc3d_ex1.py is a basic example for reading data from Batman EVK
    
    

# Data Structure:

    Detected Object Data Format: <frameNum,numObjs,[op]>
    frameNum: Frame Number
    numObjs: number of Detected Object
    [op]: an Array of Detected Objects Point , the point includes position and object moving speed data
    op: objPoint class
    <frameNum,numObjs,op=[(tid0,x0,y0,z0,vx0,vy0,vz0,dimx0,dimy0,dimz0),(tid1,x1,y1,z1,vx1,vy1,vz1,dimx1,dimy1,dimz1),(tid2,x2,y2,z2,vx2,vy2,vz2,dimx2,dimy2,dimz2)...]>
    
    
## Header:
    @dataclass
    class objPoint:
        tid: int 
        x: float
        y: float
        z: float = 0.0
        vx: float = 0.0
        vy: float = 0.0
        vz : float = 0.0
        dimX : float = 0.0
        dimY : float = 0.0
        dimZ : float = 0.0
        state : int = 0
    
    @dataclass
    class objSets:
        frameNum: int
        numObjs: int
        op: [objPoint]
	
    function call: pc3dRead(self)
		    return objSets
		

# import lib

    from mmWave import people3D

  ### raspberry pi 3 use ttyS0
    port = serial.Serial("/dev/ttyS0",baudrate = 921600, timeout = 0.5)

  ### raspberry pi 2 use ttyAMA0
    port = serial.Serial("/dev/ttyAMA0",baudrate = 921600, timeout = 0.5)
    
  ### Jetson Nano use ttyTHS1
	port = serial.Serial("/dev/ttyTHS1",baudrate = 921600, timeout = 0.5)
	and please modify: 
	
	#import RPi.GPIO as GPIO
	import Jetson.GPIO as GPIO

## define 
    pc3d = people3D.People3D(port)

## get ODS Sensor Data
    (dck ,pc3) = pc3d.Read(False)
    if dck:
        print(pc3) #you will see the data
        
## Reference:

