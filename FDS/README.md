![Platform](https://img.shields.io/badge/Raspberry-Pi3-orange.svg)&nbsp;
![Platform](https://img.shields.io/badge/Raspberry-Pi4-orange.svg)&nbsp;
![Platform](https://img.shields.io/badge/ubuntu-NCU-orange.svg)&nbsp;
![Platform](https://img.shields.io/badge/Win-OS-blue)&nbsp;
![Platform](https://img.shields.io/badge/Mac-OS-lightgrey)&nbsp;
![Platform](https://img.shields.io/badge/Jeson-Nano-green.svg)&nbsp;
![Language](https://img.shields.io/badge/python-%3E3.7%20-green.svg)&nbsp;
![License](http://img.shields.io/badge/license-MIT-green.svg?style=flat)

# 🚧  Under Construction 🚧 
# mmWave_FDS (Falling Detection Sensing)


Current PI's OS is supports python 3.7.0

https://projects.raspberrypi.org/en/projects/raspberry-pi-setting-up/3

This repository contains the Batman mmWave-PCR People/Object-Counting short Range sensor SDK. The sample code below consists of instruction for using the mmWave lib. This mmWave-PCR Python Program will work with People/Object-Counting short Range sensor based Batman BM501-PCR mmWave Kit solution. This Python Program works with a Raspberry Pi 4, NVIDIA Jetson Nano, Windows, Linux, or MAC computer with Batman BM501-PCR Kit attached via Kit’s HAT Board; and that the BM501 Kit is an easy-to-use mmWave sensor evaluation kit for People/Object Sensing in approx. 30cm ~ 1m short range region; and where the Python Program would have multiple People/Object detection in a 3-Dimentional Area with ID tag, posX, posY, posZ, velX, velY, velZ, accX, accY, accZ parameters, along with Point Clouds with elevation, azimuth, doppler, range, and snr parameters.

# Hardware:
    Batman BM501-PCR EVM Kit (TI IWR6843AOP ASIC based mmWave solution)

![BM501 EVM Kit Structure](https://user-images.githubusercontent.com/2010446/118910376-ed084400-b956-11eb-8d10-defee8be9c49.png)
  
# installing
Library install for Python

    $sudo pip install mmWave
    $sudo pip3 install mmWave
    
    pySerial Library
    $sudo pip3 install pySerial
    
    install pandas
    $sudo install pandas
    
Library update:

    $sudo pip install mmWave -U
    $sudo pip3 install mmWave -U
    
Other packages install:
  


# import lib:

    from mmWave import pc3
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

# Define:
      radar = pc3.Pc3(port)
  
  ## (Real Time: BaudRate:921600) 
     
     (dck,v6,v7,v8) = radar.tlvRead(False,df = 'DataFrame')
     
      dck: True: data avaliable
          false: data invalid
      df = 'DataFrame' will output dataFrame type  
   
  ## (playback: BaudRate:115200)
  
    #read file
   
      (v6smu,v7smu,v8smu) = radar.readFile("pc3az2021-04-01-23-18-25.csv")
   
    #get frame number from header
   
      hdr = radar.getHeader()
      fn = hdr.frameNumber
   
    #get v6,v7 and v8 based on fn(frameNum)
   
      (dck,v6,v7,v8)  = radar.getRecordData(fn)
   
   
   
# V6(point cloud),V7(target object) and V8(target index) DataFrame Structure:

    V6 data structure: (point cloud)
      fN           int64    #frameNum
      type        object    #v6
      elv        float64.   #Elevation in radians
      azimuth    float64    #Azimuth in radians
      doppler    float64    #Doppler in m/s
      range      float64    #Range in meters
      snr        float64    #SNR, ratio
      sx         float64    #point cloud position in X, m
      sy         float64    #point cloud position in Y, m
      sz         float64    #point cloud position in Z, m
      
            ------------------ v6 dataFrame -------- 
               fN type   elv  azimuth  ...          snr        sx        sy        sz
      0      2352   v6  0.04     0.09  ...     0.640000  0.034059  0.377413  0.015166
      1      2352   v6  0.04     0.10  ...     0.640000  0.037832  0.377054  0.015166
      2      2352   v6  0.04     0.11  ...     0.640000  0.041600  0.376656  0.015166
      3      2352   v6  0.04     0.12  ...     0.640000  0.045365  0.376222  0.015166
      4      2352   v6  0.04     0.13  ...     0.640000  0.049124  0.375749  0.015166
  
    V7 data structure: (Target Object)
      fN        int64     #frameNum
      type     object     #v7
      posX    float64     #Target position in X, m
      posY    float64     #Target position in Y, m
      velX    float64     #Target velocity in X, m/s   
      velY    float64     #Target velocity in Y, m/s
      accX    float64     #Target acceleration in X, m/s2
      accY    float64     #Target acceleration in Y, m/s2
      posZ    float64     #Target position in Z, m
      velZ    float64     #Target velocity in Z, m/s
      accZ    float64     #Target acceleration in Z, m/s2
      tid     float64     #Track ID

         ------------------ v7 dataFrame ----------------------
               fN type                   posX      posY  ...  posZ  velZ  accZ   tid
      145    2352   v7  -0.053493354469537735  0.538154  ...   0.0   0.0   0.0  13.0
      299    2353   v7  -0.053493354469537735  0.538154  ...   0.0   0.0   0.0  13.0
      438    2354   v7  -0.053493354469537735  0.538154  ...   0.0   0.0   0.0  13.0
      2091   2365   v7    -0.1375218629837036  0.860848  ...   0.0   0.0   0.0   7.0
      2261   2366   v7   -0.13885363936424255  0.869185  ...   0.0   0.0   0.0   7.0
    
    V8 data structure: (Target Index)
      fN           int64
      type        object
      targetID    object
      
      Other Target ID values:
      253:Point not associated, SNR to weak
      254:Point not associated, located outside boundary of interest
      255:Point not associated, considered as noise
      
      
            ------------------ v8 dataFrame ----------------------
               fN type                                           targetID
      144    2352   v8  [254, 254, 254, 254, 254, 254, 254, 254, 254, ...
      298    2353   v8  [254, 254, 254, 254, 254, 254, 254, 254, 254, ...
      437    2354   v8  [254, 254, 254, 254, 254, 254, 254, 254, 254, ...
      2090   2365   v8  [255, 255, 255, 255, 255, 255, 7, 7, 7, 7, 7, ...
      2260   2366   v8  [254, 254, 254, 254, 254, 254, 254, 254, 254, ...
      

# Example

    


# the following example work with toolkit-PC3

    

# csv data file for test

