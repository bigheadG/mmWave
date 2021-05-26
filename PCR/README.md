![Platform](https://img.shields.io/badge/Raspberry-Pi3-orange.svg)&nbsp;
![Platform](https://img.shields.io/badge/Raspberry-Pi4-orange.svg)&nbsp;
![Platform](https://img.shields.io/badge/ubuntu-NCU-orange.svg)&nbsp;
![Platform](https://img.shields.io/badge/Win-OS-blue)&nbsp;
![Platform](https://img.shields.io/badge/Mac-OS-lightgrey)&nbsp;
![Platform](https://img.shields.io/badge/Jeson-Nano-green.svg)&nbsp;
![Language](https://img.shields.io/badge/python-%3E3.6%20-green.svg)&nbsp;
![License](http://img.shields.io/badge/license-MIT-green.svg?style=flat)

# 🚧   Under Construction -  🚧 
# mmWave_PCR (People/Object Counting short Range sensor)


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

    1. pc3_raw_ex0_record.py                #record data 
    
    The following program is executed and recorded on MacBook Pro
    2. pyqtgraph_3d_pc3_xyz_df_ex1.py       #real time display radar data 
       
https://user-images.githubusercontent.com/2010446/118239936-f3b53800-b4cc-11eb-8e3a-6542b3cf09f8.mov
    
    The following program is executed and recorded on MacBook Pro
    4. pyqtgraph_3d_pc3_uDoppler_Freq_df.py   #Detected object at 10mx10m Area 
      

https://user-images.githubusercontent.com/2010446/118364473-1c235c00-b5cb-11eb-8af6-983bcb16c456.mov


# the following example work with toolkit-PC3

    UART BaudRate: 115200
    3. pyqtgraph_3d_pc3_xyz_playback_ex2.py    #csv file data playback

# csv data file for test
<pre> pc3az2021-05-04-10-58-36_1_10cm.csv       #distance: 10cm 1 object</pre> 
<pre> pc3az2021-05-04-11-05-59_2_30cm.csv       #distance: 30cm 2 object</pre> 
<pre> pc3az2021-05-04-11-10-03_3_10cm.csv       #distance: 10cm 3 object</pre> 
<pre> pc3az2021-05-04-11-25-09_all_1m2.csv      #distance: 1m2 all object</pre>


# Reference

UART Output Data Format
----------- 

The demo outputs the point cloud and tracking information using a TLV(type-length-value) encoding scheme with little endian byte order. For every frame, a packet is sent consisting of a fixed sized **Frame Header** and then a variable number of TLVs depending on what was detected in that scene. The TLVs can be of types representing the 3D point cloud, target list object, and associated points.

<img src="images/packet_structure.png" width="600"/>

### Frame Header
Size: 48 bytes

```Matlab
frameHeaderStructType = struct(...
    'sync',                         {'uint64', 8}, ... % syncPattern in hex is: '02 01 04 03 06 05 08 07' 
    'version',                      {'uint32', 4}, ... % 0xA6843
    'totalPacketLen',               {'uint32', 4}, ... % See description below
    'platform',                     {'uint32', 4}, ... % 600MHz free running clocks
    'frameNumber',                  {'uint32', 4}, ... % In bytes, including header
    'subFrameNumber',               {'uint32', 4}, ... % Starting from 1
    'chirpProcessingMargin',        {'uint32', 4}, ... % Chirp Processing margin, in ms
    'frameProcessingMargin',        {'uint32', 4}, ... % Frame Processing margin, in ms
    'trackProcessTime',             {'uint32', 4}, ... % Tracking Processing time, in ms
    'uartSentTime' ,                {'uint32', 4}, ... % Time spent to send data, in ms
    'numTLVs' ,                     {'uint16', 2}, ... % Number of TLVs in thins frame
    'checksum',                     {'uint16', 2});    % Header checksum

```**Frame Header Structure: name, type, length**

```Matlab
% Input: frameheader is a 48x1 double array, each index represents a byte of the frame header
% Output: CS is checksum indicator. If CS is 0, checksum is valid.

function CS = validateChecksum(frameheader)
    h = typecast(uint8(header),'uint16');
    a = uint32(sum(h));
    b = uint16(sum(typecast(a,'uint16')));
    CS = uint16(bitcmp(b));
end
```**validateChecksum(frameheader) in MATLAB syntax**   

### TLVs 
The TLVs can be of type **POINT CLOUD**, **TARGET LIST**, **TARGET INDEX** or **PRESENCE INDICATION**.

#### **TLV Header**
Size: 8 bytes
```Matlab
% TLV Type: 06 = Point cloud, 07 = Target object list, 08 = Target index
tlvHeaderStruct = struct(...
    'type',             {'uint32', 4}, ... % TLV object 
    'length',           {'uint32', 4});    % TLV object Length, in bytes, including TLV header 
```**TLV header**  

Following the header, is the the TLV-type specific payload

#### **Point Cloud TLV**
Size: sizeof (tlvHeaderStruct) + sizeof(pointUnit) + sizeof (pointStruct) x numberOfPoints 

Each Point Cloud TLV consists of an array of points. Each point is defined in 8 bytes. The pointUnit struct is used to uncompress each point to five floats (20 bytes).

```java
pointUnit = struct(...
    'elevationUnit',        {'float', 4}, ... % Multiply each point by this value - used for compression
    'azimuthUnit',          {'float', 4}, ... % Multiply each point by this value - used for compression
    'dopplerUnit',          {'float', 4}, ... % Multiply each point by this value - used for compression
    'rangeUnit',            {'float', 4}, ... % Multiply each point by this value - used for compression
    'snrUnit',              {'float', 4});    % Multiply each point by this value - used for compression
```**Point Structure** 

```java
pointStruct = struct(...
    'elevation',        {'int8_t', 1}, ... % Elevation in radians
    'azimuth',          {'int8_t', 1}, ... % Azimuth, in radians
    'doppler',          {'int16_t', 2}, ... % Doppler, in m/s
    'range',            {'uint16_t', 2}, ... % Range, in meters
    'snr',              {'uint16_t', 2});    % SNR, ratio
```**Point Structure**  

#### **Target List TLV**
Size: sizeof (tlvHeaderStruct) + sizeof (trackerProc_Target) x numberOfTargets
 
The Target List TLV consists of an array of targets. Each target object is defined as given below.


```java
targetStruct3D = struct(...
    'tid',             {'uint32', 4}, ... % Track ID
    'posX',            {'float', 4}, ... % Target position in X dimension, m
    'posY',            {'float', 4}, ... % Target position in Y dimension, m
    'posZ',            {'float', 4}, ... % Target position in Z dimension, m
    'velX',            {'float', 4}, ... % Target velocity in X dimension, m/s
    'velY',            {'float', 4}, ... % Target velocity in Y dimension, m/s
    'velZ',            {'float', 4}, ... % Target velocity in Z dimension, m/s
    'accX',            {'float', 4}, ... % Target acceleration in X dimension, m/s2
    'accY',            {'float', 4}, ... % Target acceleration in Y dimension, m/s
    'accZ',            {'float', 4}, ... % Target acceleration in Z dimension, m/s
    'ec[16]',          {'float', 16x4}, ... % Tracking error covariance matrix, [4x4] in range/azimuth/elevation/doppler coordinates
    'g',               {'float', 4}, ... % Gating function gain
    'confidenceLevel'  {'float', 4}, ... % Confidence Level

```**Target Structure**  

#### **Target Index TLV**
Size: sizeof (tlvHeaderStruct) + sizeof(uint8) x numberOfPoints (NOTE: here the number of points are for frame n-1)
 
The Target Index TLV consists of an array of target IDs. A targetID at index ***i*** is the target to which point ***i*** of the previous frame's point cloud was associated.
Valid IDs range from 0-249. 

```java
targetIndex = struct(...
'targetID',         {'uint8', 1});    % Track ID

```**Target ID Structure**   

Other Target ID values:

Value       | Meaning
------------|-----------
253         | Point not associated, SNR too weak
254         | Point not associated, located outside boundary of interest
255         | Point not associated, considered as noise

#### **Presence Indication TLV**
Size: sizeof (tlvHeaderStruct) + sizeof(uint32)
 
The Presence Indication TLV consists of a single uint32 value to provide a binary indication of presence in the presence boundary box. A value of 1 represents presence detected and 0 represents no presence detected.



