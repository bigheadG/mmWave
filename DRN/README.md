# mmWave-DRN (Surface Velocity Detection Radar)
This repository contains the Batman Kit-201 DRN Drone Radar Navigation SDK.  The sample code below consists of instruction for using the mmWave lib. This mmWave-DRN Python Program will work with Drone Radar Navigation (DRN) based Batman BM201-DRN mmWave EVM Kit solution. This App works with Raspberry Pi 4 or Jetson Nano along with Batman BM201-DRN EVM Kit, and will report DRN data that include Doppler-Range Data, Point Cloud Data, and Range Profile; for application such as drone navigation with range of approx. 20 meters.

# Hardware:
    Batman kit-201 (ISK)
    Measure Range: 20 meters
    
# Installing

Library install for Python

    $sudo pip install mmWave
    $sudo pip3 install mmWave

Library update:

    $sudo pip install mmWave -U
    $sudo pip3 install mmWave -U

Examples:

    pyqtgraph_drn.py # show detected object, doppler and range profile
    
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
    
![MainMenu 1](https://github.com/bigheadG/imageDir/blob/master/svd.png)
    
## Header:

    class header:
        version = 0
        totalPackLen = 0
        platform = 0
        frameNumber = 0
        timeCpuCycles = 0
        numDetectedObj = 0
        numTLVs = 0
        subFrameIndex = 0

## Data Structure

### V1 Point Cloud Detected Object: Contains (X,Y,Z) coordinate and Doppler information of objects seen by the mmWave device
    
    V1 : [((float(x),float(y),float(z),float(Velocity)).....]
	tlvNDOCnt : Number of Detected Object Count
	x : X coordinate in meters
	y : Y coordinate in meters
	z : Z coordinate in meters
	Velocity : Doppler velocity estimate in m/s. Positive velocity means target 
		is moving away from the sensor and Negative velocity means target 
		is moving towards the sensor.
	
	
### V2 Range Profile: Array of range profile points at 0th Doppler (stationary objects). the points represent the sum of log2 magnitudes of received antennas.
    
	V2: (Range FFT) * 512
	size: 512 points  

### V3 Noise Profile: this is the same format as range porfilebut the profile is at the maximum Doppler bin(maximum speed objects). In general for stationary scene, there would be no objects or clutter at maximum speed so the range profile at such speed represents the receiver noise floor.

      V3: (Range FFT) * 512
      size: 512 points
    
### V6 Stats Information:

	V6: (interFrameProcessingTime ,   #interFrame processing time in usec
            transmitOutputTime ,        #Transmission time of output detection information in usec
            interFrameProcessingMargin, #interFrame processing margin in usec
            interChirpProcessingMargin, #interChirp processing margin in usec
            activerFrameCPULoad,        #CPU Load (%) during active frame duration
            interFrameCPULoad)          #CPU Load (%) during inter frame duration
	
		
### V7 Point Cloud Side Infomation:
    
     V7: [(snr,noise).....]
     
     snr: CFAR cell to side noise in dB expressed in 0.1 steps of dB
     noise: CFAR noise level of the side of the detected cell in dB expressed in 0.1 steps of dB
			
# function call:
	 
	getHeader()
      headerShow()
	tlvRead()
	usage: (dck,v1,v2,v3,v6,v7) = drn.tlvRead(False)
		    

# import lib

    from mmWave import droneRN

  ### raspberry pi 4 use ttyS0
    port = serial.Serial("/dev/ttyS0",baudrate = 921600*2, timeout = 0.5)

    
  ### Jetson Nano use ttyTHS1
  	port = serial.Serial("/dev/ttyTHS1",baudrate = 921600*2, timeout = 0.5)
	and please modify: 
	

## define

    drn = droneRN.DroneRN(port)

## get tlv Data

    (dck,v1,v2,v3,v6,v7) = drn.tlvRead(False)
    dck: data check 1: available 0: data not ready

    v1 :Point Cloud
    v2 :Range Profile
    v3 :Noise Profile
    v6 :Stats Information
    v7 :Side Information of Detected Object

## Reference



