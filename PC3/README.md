![Platform](https://img.shields.io/badge/Raspberry-Pi3-orange.svg)&nbsp;
![Platform](https://img.shields.io/badge/Raspberry-Pi4-orange.svg)&nbsp;
![Platform](https://img.shields.io/badge/ubuntu-NCU-orange.svg)&nbsp;
![Platform](https://img.shields.io/badge/Win-OS-blue)&nbsp;
![Platform](https://img.shields.io/badge/Mac-OS-lightgrey)&nbsp;
![Platform](https://img.shields.io/badge/Jeson-Nano-green.svg)&nbsp;
![Language](https://img.shields.io/badge/python-%3E3.6%20-green.svg)&nbsp;
![License](http://img.shields.io/badge/license-MIT-green.svg?style=flat)

# mmWave-PC3 (People Counting 3D SDK)

Current PI's OS is supports python 3.7.0

https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up/3

This repository contains the Batman mmWave-PC3 People Counting & Detection mmWave Sensor SDK. The sample code below consists of instruction for using the mmWave lib. This mmWave-PC3 Python Program will work with People Counting & Detection based Batman BM201-PC3 mmWave Kit solution. This Python Program works with a Raspberry Pi 4 , NVIDIA Jetson Nano, windows/linux computer or MAC with Batman BM201-PC3 Kit attached via Kit’s HAT Board; and that the BM201 Kit is an easy-to-use mmWave sensor evaluation kit for People Sensing, People Counting, or People Occupancy Density Estimation in approx. 6m x 6m area without privacy invasion; and where the Python Program would have multiple people detection in a 3-Dimentional Area with ID tag, posX, posY, posZ, velx, vely, velz, accX, accY, accZ parameters, along with Point Clouds with elevation, azimuth, doppler, range, and snr parameters.


# Hardware:
    Batman kit-201 (ISK)
    Measure Range: 6 meters
    
# Installing

Library install for Python

    $sudo pip install mmWave
    $sudo pip3 install mmWave

Library update:

    $sudo pip install mmWave -U
    $sudo pip3 install mmWave -U

Examples:

	    PC3_ex0.py # show v6,v7,v8 and v8 data
	    PC3_ex1_pandas.py # show v6,v7 data using dataFrame
	    PC3_ex2_record.py # recording v6,v7 and v8 data
	    PC3_ex3_pyqtgraph_xyz_playback.py # v6 data playback
	       pc3_2021-12-19-21-25-28.csv # for PC3_ex3_pyqtgraph_xyz_playnback.py playback use
	    pyqtgraph_3d_pc3_xyz.py # show detected point cloud in 3D
	    pyqtgraph_3d_pc3_occupancy.py # show occupancy detection
    
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

## pyqtgraph_3d_pc3_xyz.py screenshot

![MainMenu 1](https://github.com/bigheadG/imageDir/blob/master/pc3_xyz.png)

## pyqtgraph_3d_pc3_occupancy.py screenshot

 
https://user-images.githubusercontent.com/2010446/118247174-7510c880-b4d5-11eb-91a2-173c0d3ddb3b.mov



 # import lib

    from mmWave import pc3

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

    radar = pc3.Pc3(port)

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
        velX: float     #Target velocity in X, m/s
        velY: float     #Target velocity in Y, m/s
        accX: float     #Target velocity in X, m/s2 
        accY: float     #Target velocity in Y, m/s2
        posZ: float     #Target position in Z, m
        velZ: float     #Target velocity in Z, m/s
        accZ: float     #Target velocity in Z, m/s2
        
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
    
 ![MainMenu 1](https://github.com/bigheadG/imageDir/blob/master/objGeoSmall.png)
			
## Get data use dataFrame: (reference: PC3_ex1_pandas.py)

	v6_col_names = ['time','fN','type','elv','azimuth','doppler','range' ,'snr','sx', 'sy', 'sz']
	v7_col_names = ['time','fN','type','posX','posY','velX','velY','accX','accY','posZ','velZ','accZ','tid']
	v8_col_names = ['time','fN','type','targetID']

    Function call: 
        (dck,v6,v7,v8) = radar.tlvRead(False,df = 'DataFrame') 
        dck : True  : data avaliable
              False : data invalid
        v6: point cloud of array
        v7: target object of array
        v8: target id of array

        return dck,v6,v7,v8 
	
    v6 & v7 data: ex: print(v6) and print(v7)
    
	    -------------- v6 ---------------
	      fN type   elv  azimuth  doppler    range   snr        sx        sy        sz
	0  16944   v6  0.32    -0.33  0.06972  1.07475  5.36 -0.330586  0.965144  0.338080
	1  16944   v6  0.25    -0.32  0.06972  1.13800  5.24 -0.346848  1.046648  0.281546
	
	-------------- v7 ---------------
	     fN type      posX      posY      velX      velY      accX      accY      posZ      velZ      accZ         tid
	0  7971   v7 -0.040078  0.829420  0.061835 -0.248975  0.013546 -0.153394  0.040553 -0.450048  0.132277           3

## read record data file(csv) and extract csv data based on frame number:
 	
	(1) read record data from csv file (for playback)
	
	# read csv record file for playback(csv file in same directory)
	ex: fileName = "pc3_2021-12-19-21-25-28.csv" 
	(v6smu,v7smu,v8smu) = radar.readFile(fileName)
	
	# tlvRead provides header and frame Number for 
	(dck,v6,v7, v8) = radar.tlvRead(False,df = 'DataFrame')
	
	(2) get a record data based on frame number (for playback)
	
	hdr = radar.getHeader()
	fn = hdr.frameNumber
	(dck,v6,v7,v8) = radar.getRecordData(fn)
	
	chk: data check true: Data is avaliable, false: Data invalid	
	fN: means frameNumber
	
	    -------------- v6 ---------------
	      fN type   elv  azimuth  doppler    range   snr        sx        sy        sz
	0  16944   v6  0.32    -0.33  0.06972  1.07475  5.36 -0.330586  0.965144  0.338080
	1  16944   v6  0.25    -0.32  0.06972  1.13800  5.24 -0.346848  1.046648  0.281546
	
	-------------- v7 ---------------
	     fN type      posX      posY      velX      velY      accX      accY      posZ      velZ      accZ         tid
	0  7971   v7 -0.040078  0.829420  0.061835 -0.248975  0.013546 -0.153394  0.040553 -0.450048  0.132277           3
    
    More detailed information please reference PC3_ex3_pyqtgraph_xyz_playback.py 
	
## Reference

 
1. LabGuide: https://github.com/bigheadG/mmWaveDocs/blob/master/3d_pplcount_user_guide.pdf



