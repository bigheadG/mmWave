# mmWave-PMB (People Movement Behavior)
This repository contains the Batman Kit- PMB mmWave Sensor SDK. 
The sample code below consists of instruction for using the mmWave lib.
This mmWave-PMB Python Program will work with People Movement Behavior (PMB) based mmWave Batman Kit solution.
This App works with Raspberry Pi 3, Pi 2 and Jetson Nano
The People Movement Behavior (PMB) based Batman Kit is for detecting People movement in a 4 x 4 meter or 16 meter square area (or about 172 square feet). 


# Installing

Library install for Python:

    $sudo pip install mmWave
    $sudo pip3 install mmWave

Library update:

    $sudo pip install mmWave -U
    $sudo pip3 install mmWave -U

Examples:

    PMB_ex0.py is a basic example for reading data from Batman EVK
    PMB_ex1_Thread.py is an example of using thread to read data from Batman EVK
    PMB_ex2_intr18.py is an example of using GPIO Pin18 rise-edge to trigger function to read data from Batman EVK

**** If the following Error is found ******

    Traceback (most recent call last):
      File "PMB_ex2_intr18.py", line 74, in <module>
        GPIO.add_event_detect(18, GPIO.RISING,my_callback)
    RuntimeError: Failed to add edge detection

    *** Plesae use the following command to clear this Error ****
    
    ~#gpio unexport 18 


# Data Structure:

    class header:
	    version = 0
	    platform = 0
	    timestamp = ""
	    totalPackLen = 0
	    frameNumber = 0
	    subframeNumber = 0
	    chirpMargin = 0
	    frameMargin = 0
	    uartSendTime = 0
	    trackProcessTime = 0
	    numTLVs = 0
	    checksum = 0
	
    function call: getHeader(self)
		  return header type data
		 

### TLV Data: Type-Length-Value
    function call: (chk,v6,v7,v8) = tlvRead(dbg)
	    dbg := True, enable debug message
	          False, disable debug message
	       
	    chk := True: Data valid
		      False: Data invalid
		   
	    v6: point cloud 2d infomation
	    v7: Target Object information
	    v8: Target Index information
	
	
### PMB Data Formats:
    PMB Data Format: [Frame Header][V6s][V7s][V8s]

    [V6s]:= [TL][P1][P2]...[Pn pts]
    [V7s]:= [TL][T1][T2]...[Tn tgs]
    [V8s]:= [TL][ID1][ID2]...[IDn pts] 
    [TL]:= Table-Lenght
    [V6] = [P1]..
    [V7] = [T1]..
    [V8] = [ID1]..
	
#### [V6] data Struct:
  
    range:float #Range, in m
    azimuth:float	#Angle, in rad
    doppler:float	#Doppler, in m/s
    snr:float #SNR, ratio

#### [V7] data Struct:
  
    tid: unit32	#TrackID
    posX:float	#Target position in X dimension,m
    posY:float	#Target position in y dimension,m
    velX:float	#Target velocity in X dimension,m/s
    velY:float	#Target velocity in y dimension,m/s
    accX:float	#Target acceleration in X dimension,m/s2
    accY:float	#Target acceleration in Y dimension,m/s2
    EC[9]:float	#Error covariance matrix, [3x3], in range/angle/doppler coordinates
    G:float		#Gating function gain


 #### [V8] data Struct:
  
    TargetID:uint8 


# import lib

    from mmWave import peopleMB

#### raspberry pi 3 use ttyS0
    port = serial.Serial("/dev/ttyS0",baudrate = 921600, timeout = 0.5)

#### raspberry pi 2 use ttyAMA0
    port = serial.Serial("/dev/ttyAMA0",baudrate = 921600, timeout = 0.5)

#### Jetson Nano use ttyTHS1
	port = serial.Serial("/dev/ttyTHS1",baudrate = 921600, timeout = 0.5)
	and please modify: 
	
	#import RPi.GPIO as GPIO
	import Jetson.GPIO as GPIO

# define 
    pm = peopleMB.PeopleMB(port)

# get tlv Data
    (dck,v6,v7,v8) = pm.tlvRead(False)

## Reference:

http://dev.ti.com/tirex/#/?link=Software%2FmmWave%20Sensors%2FIndustrial%20Toolbox%2FLabs%2FPeople%20Counting%20Demo%2F16xx%20-%20People%20Counting%20Demo%2FUser's%20Guide

http://www.ti.com/lit/ug/tidued6/tidued6.pdf
