# mmWave-PCT (People-Counting with Tilt Sensing SDK)

![Platform](https://img.shields.io/badge/Raspberry-Pi4-orange.svg)&nbsp;
![Platform](https://img.shields.io/badge/ubuntu-NCU-orange.svg)&nbsp;
![Platform](https://img.shields.io/badge/Win-OS-blue)&nbsp;
![Platform](https://img.shields.io/badge/Mac-OS-lightgrey)&nbsp;
![Platform](https://img.shields.io/badge/Jeson-Nano-green.svg)&nbsp;
![Language](https://img.shields.io/badge/python-%3E3.6%20-green.svg)&nbsp;
![License](http://img.shields.io/badge/license-MIT-green.svg?style=flat)

Current PI's OS is supports python 3.7.0

https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up/3

This repository contains the Batman mmWave-PCT People-Counting with Tilt Sensor SDK. The sample code below consists of instruction for using the mmWave library. This mmWave-PCT Python Program will work with People-Counting Wall Mount with Tilt Sensing Batman BM502-PCT mmWave Kit solution. This Python Program works with a Raspberry Pi 4, Windows, Linux, or MAC computer with Batman BM502-PCT Kit attached via Kit’s HAT Board; and that the BM502 Kit is an easy-to-use mmWave sensor evaluation kit for People Sensing, People Counting, or People Occupancy Density Estimation in approx. 4.5m x 4.5m x 3m region without privacy invasion; and where the Python Program have multiple people detection in a 3-Dimentional Area with ID tag, posX, posY, posZ, velX, velY, velZ, accX, accY, accZ parameters, along with Point Clouds with elevation, azimuth, doppler, range, and snr parameters.

Note: For People Fall Detection please refer to “PCT_FDS: People Fall Detection demo application based on mmWave-PCT” section. 


# BM502-PCT EVM Kit Mounting and Scene Conditions
The BM502 Module from the EVM Kit needs to be mounted at a heigh of 2.8-3.0m top-down in the center of the area of interest, with the BM501 Module sensor directly facing the ground. Notes: If you use Tripod to elevate the EVM, Please make sure that it has an extension arm (minimun 305mm ~ 381mm or 12-15 inches) to set apart the EVM away from the Tripod's stem.
    

# Hardware:
    Batman BM502-PCT EVM Kit (TI IWR6843AOP ASIC based mmWave solution)
 
 
 ![BM502 EVM Kit Structure](https://github.com/bigheadG/mmWave_pct/assets/2010446/165c397a-2676-49ca-b32b-4876f657dd28)

 Note : Specifications subject to change without prior notice

    
    Measure Range: 4.5m x 4.5m x 3.0m 
    Power supply: 5Vdc/2.1A 

# Installing

Library install for Python

    $sudo pip install mmWave
    $sudo pip3 install mmWave

Library update:

    $sudo pip install mmWave -U
    $sudo pip3 install mmWave -U

Examples:

    PCT_ex0.py                              # show v6,v7 and v8 data
    PCT_ex2_record.py                       # record v6,v7 and v8 data. file output: pct_2023-xx-xx-xx-xx.csv
    PCT_ex3_pyqtgraph_v6_dataFrame.py       # runtime/playback plot v6 point cloud, playback mode work with TK-101

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

    from mmWave import pct
  ### UART Baud Rate:
    RUN time(AOP): 921600 bps
    Playback(TK-101): 115200 bps
    
  ### raspberry pi 4 use ttyS0
    port = serial.Serial("/dev/ttyS0",baudrate = 921600, timeout = 0.5)
 
  ### Jetson Nano use ttyTHS1
    port = serial.Serial("/dev/ttyTHS1",baudrate = 921600, timeout = 0.5)
    
  ### use USB-UART
    port = serial.Serial("/dev/ttyUSB0",baudrate = 921600, timeout = 0.5)
 
  ### Mac OS use tty.usbmodemxxxx
    port = serial.Serial("/dev/tty.usbmodemGY0052854",baudrate = 921600, timeout = 0.5)
  
  ### ubuntu NUC
    port = serial.Serial("/dev/ttyACM1",baudrate = 921600, timeout = 0.5)


## define

    radar = pct.Pct(port)
    
    radar = pct.Pct(port, tiltAngle= 45.0, height = 2.0)
    Pct argument: 
        port: UART port
        tileAngle: mmWave board install angle,  ex: tileAngle is 45.0° , height: 2 meter
        height:    mmWave Board install heigh, unit: meter
        df:        tlvRead output data type. df = "DataFrame" v6,v7 output DataFrame types data.
    ex:   
        port = serial.Serial(PORT,baudrate = BAUD_RATE , timeout = 0.5) 
        # df = "DataFrame" tlvRead will output DataFrame types data
        radar = pct.Pct(port,tiltAngle=JB_TILT_DEGREE,height = JB_RADAR_INSTALL_HEIGHT, df = "DataFrame") 
        
     

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
   
    point Struct(xyzreadsf type):
        sx :      float   #point position x
        sy :      float   #point position y
        sz :      float   #point position z
        range:    float   #Range in meters
        elevation: float  #Elevation in radians
        azimuth:  float   #Azimuth in radians
        doppler:  float   #Doppler in m/s
        snr:      float   #SNR, ratio
        fn:       Int     #frame number
   
 

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
 

## Run PCT_ex0.py
     JB_TILT_DEGREE = 45
     JB_RADAR_INSTALL_HEIGHT = 2.41 #unit: meter
     radar = pct.Pct(port,tiltAngle=JB_TILT_DEGREE,height = JB_RADAR_INSTALL_HEIGHT)
     (dck,v6,v7,v8) = radar.tlvRead(False)
     Show v6,v7 and v8 data as following:
 List types:
<img width="940" alt="listData" src="https://user-images.githubusercontent.com/2010446/217446819-a8561f94-fc09-410d-acc1-ecb42c28220d.png">

    
# Data Structure(DataFrame Type):
    When tlvRead argument set df = 'DataFrame', v6,v7 and v8 will output DataFrame style data
    
    JB_TILT_DEGREE = 45 
    JB_RADAR_INSTALL_HEIGHT = 2.41 #unit: meter
    radar = pct.Pct(port,tiltAngle=JB_TILT_DEGREE,height = JB_RADAR_INSTALL_HEIGHT, df = "DataFrame")
    (dck,v6,v7,v8) = radar.tlvRead(False)
    
    Type V6:
        ['fN','type','sx', 'sy', 'sz','range','elv','azimuth','doppler','snr']
        fN: frame number
        type: 'v6'
        sx : point position x
        sy : point position y
        sz : point position z
        range:    float   #Range in meters
        elv: float  #Elevation in radians
        azimuth:  float   #Azimuth in radians
        doppler:  float   #Doppler in m/s
        snr: #SNR, ratio
        
  
  
    Type v7:
        ['fN','type','posX','posY','posZ','velX','velY','velZ','accX','accY','accZ','ec0','ec1','ec2','ec3','ec4','ec5','ec6','ec7','ec8','ec9','ec10','ec11','ec12','ec13','ec14','ec15','g','confi','tid']
        
        fN: frame number
        type: 'v7'
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
        
    
    Type v8: 
        ['fN','type','targetID']
        
        fN: frame Number
        type: 'v8'
        Other Target ID values:
        253:Point not associated, SNR to weak
        254:Point not associated, located outside boundary of interest
        255:Point not associated, considered as noise
        
    <br/>   
    DataFrame types:
   <img width="890" alt="dataFrame" src="https://user-images.githubusercontent.com/2010446/217446343-e518e34b-2a1a-4bb7-a5c7-71b68c9ca4ef.png">
      
# Read Record Data File for Analysis point cloud Step by Step.
    
    this subroutine work with Point Cloud tool kit TK-001 then you can step by step to analysis point cloud:
    
    (1)Read record file
    readFile(fileName)
    (v6smu,v7smu,v8smu) = radar.readFile("pct_2021-xx-xx-xx-xx-34.csv")
   
    (2)based on frameNumber output v6,v7 and v8 data
    getRecordData(frameNumber)
    (dck,v6,v7,v8) = radar.getRecordData(frameNumber)
    dck : True : data avaliable
    v6: point cloud of dataframe type data
    v7: target object of dataframe type data  
    v8: target id of dataframe type data
    
## PCT_ex3_pyqtgraph_v6_dataFrame.py example

        ################### Run Time/Playback & parameter setting   ######
        #RUN_TIME = False #playback
        RUN_TIME = True   #run time

        # Parameters:
        PORT = '/dev/tty.SLAB_USBtoUART5'
        #PORT = '/dev/tty.usbmodem14303'

        JB_TILT_DEGREE = 45 
        JB_RADAR_INSTALL_HEIGHT = 2.41 # meter

        QUEUE_LEN = 3

        BAUD_RATE = 921600 if RUN_TIME == True else 115200
        PLAYBACK_FILE  = "pct_2023-02-08-16-48-32.csv" # find file in same directory

        ####################################################################

## ex3 playback demo
https://user-images.githubusercontent.com/2010446/217719084-ee076820-0923-4d88-8284-b1d3906d6070.MOV



# AOP Coordinate Geometry


![BM502-PCT_wall_H_001](https://user-images.githubusercontent.com/2010446/218928431-74adfabd-78ed-4163-b004-113db1d9bbda.jpg)
![BM502-PCT_wall_H_002](https://user-images.githubusercontent.com/2010446/222321945-513f67d7-9156-4ab3-8c4a-b671f7d8bbf0.jpg)
![BM502-PCT_wall_H_003](https://user-images.githubusercontent.com/2010446/222327980-f80a2a31-ac76-4bdd-a963-6867ee594832.jpg)
## Reference

 
1. LabGuide: [People counting Overhead reference guide](https://dev.ti.com/tirex/explore/node?node=AGn5r.xojDrrAKHxSfvzFg__VLyFKFf__LATEST)

2. TuningGuide_01: 
[3D_people_counting_tracker_layer_tuning_guide.pdf](https://github.com/bigheadG/mmWave_elink/files/7465690/3D_people_counting_tracker_layer_tuning_guide.pdf)

3. TuningGuide_02:
[3D_people_counting_detection_layer_tuning_guide.pdf](https://github.com/bigheadG/mmWave_elink/files/7502420/3D_people_counting_detection_layer_tuning_guide.pdf)
