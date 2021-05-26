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

This repository contains the Batman mmWave-FDS Fall Detection Sensor SDK. The sample code below consists of instruction for using the mmWave lib. This mmWave-FDS Python Program will work with People Fall Detection sensor based Batman BM501-FDS mmWave Kit solution. This Python Program works with a Raspberry Pi 4, NVIDIA Jetson Nano, Windows, Linux, or MAC computer with Batman BM501-FDS Kit attached via Kit’s HAT Board; and that the BM501 Kit is an easy-to-use mmWave sensor evaluation kit for People Fall Detection Sensing in approx. 6m x 6m x 3m region without privacy invasion; and where the Python Program would have multiple People detections in a 3-Dimentional region with ID tag, posX, posY, posZ, velX, velY, velZ, accX, accY, accZ parameters, along with Point Clouds with elevation, azimuth, doppler, range, and snr parameters.

# Hardware:
    Batman BM501-FDS EVM Kit (TI IWR6843AOP ASIC based mmWave solution)

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
      range      float64    #Range in meters
      azimuth    float64    #Azimuth in radians
      elv        float64.   #Elevation in radians
      doppler    float64    #Doppler in m/s
      sx         float64    #point cloud position in X, m
      sy         float64    #point cloud position in Y, m
      sz         float64    #point cloud position in Z, m
      
            ------------------ v6 dataFrame -------- 
              fN type     range   azimuth  ...   doppler        sx        sy        sz
        0   4699   v6  0.643769  0.635912  ...  0.081016  0.382238  0.517790  0.015018
        1   4699   v6  0.697416  0.635771  ...  0.081016  0.414091  0.561105  0.008906
        2   4699   v6  0.751063  0.597407  ...  0.081016  0.422473  0.620976 -0.001160
        3   4699   v6  0.804711  0.597966  ...  0.081016  0.452650  0.664533 -0.032604
        4   4699   v6  0.643769  0.636211  ...  0.162032  0.382238  0.517467  0.023668
        5   4699   v6  0.697416  0.635919  ...  0.162032  0.414091  0.560932  0.016529
        6   4699   v6  0.751063  0.597430  ...  0.162032  0.422473  0.620946  0.006267
        7   4699   v6  0.804711  0.597649  ...  0.162032  0.452650  0.664986 -0.021477
        8   4699   v6  0.643769  0.635715  ... -0.162032  0.382238  0.518005 -0.001914
        9   4699   v6  0.697416  0.635793  ... -0.162032  0.414091  0.561080 -0.010353


    V7 data structure: (Target Object)
      fN        int64     #frameNum
      type     object     #v7
      posX    float64     #Target position in X, m
      posY    float64     #Target position in Y, m
      posZ    float64     #Target position in Z, m
      velX    float64     #Target velocity in X, m/s   
      velY    float64     #Target velocity in Y, m/s
      velZ    float64     #Target velocity in Z, m/s
      accX    float64     #Target acceleration in X, m/s2
      accY    float64     #Target acceleration in Y, m/s2
      accZ    float64     #Target acceleration in Z, m/s2
      ec0..ec15  float64    #Tracking erro covariance matrix,[4x4] in range/azimuth/elevation/doppler coordinates
        g        float64    #Gating function gain
      confi    float64      #Confidence level
      tid     float64     #Track ID

         ------------------ v7 dataFrame ----------------------
          fN  type      posX      posY      posZ  ...      ec14      ec15    g  confi  tid
      0  5212   v7  0.478549  0.557044 -0.047848  ... -0.189876  5.912879  3.0    1.0    0
    
    V8 data structure: (Target Index)
      fN           int64.  #frameNum
      type        object.  #v8
      targetID    object   #Target ID
      
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



    V9 Point Cloud Side info TLV data structure:

        fN        int64.    # frameNumber
        type      object.   #v9
        snr       int64     #SNR, Ratio 
        noise     int64     #Noise
       
          ------------------ v9 dataFrame ----------------------
              fN type  snr  noise
        0   9077   v9  134    517
        1   9077   v9  138    518
        2   9077   v9  274    488
        3   9077   v9  306    488
        4   9077   v9  295    475
        5   9077   v9  220    465
        6   9077   v9  169    478
        7   9077   v9  118    590
        8   9077   v9  123    587
        9   9077   v9  263    481
        10  9077   v9  294    483
      

# Example

    


# the following example work with toolkit-PC3

    

# csv data file for test



# Reference

LabGuide: reference from TI:
https://github.com/bigheadG/mmWaveDocs/blob/master/V2450_FDS_68xx_long_range_people_det_user_guide_pdf.pdf


