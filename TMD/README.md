 # mmWave-TMD (Traffic Monitor Detection)
This repository contains the Batman Kit- Traffic Monitor Detection mmWave Sensor SDK. 
The sample code below consists of instruction for using the mmWave lib.
This mmWave-TMD Python Program will work with Traffic Monitor Detection (TMD) based mmWave Batman Kit solution.
This App works with Raspberry Pi 3 , Jetson Nano, windows and Mac
The Traffic Monitor Detection (TMD) based on BM201-TMD-ISK for a contactless detect object moving in specify zone.
The detect vehicle range from 5m to 50m  

# Installing

Library install for Python

    $sudo pip install mmWave
    $sudo pip3 install mmWave

Library update:

    $sudo pip install mmWave -U
    $sudo pip3 install mmWave -U

Examples:
    TMD_kv_ex0.py is a basic example for reading data from BM201-TMD-ISK
    TMD_kv_pyqtgraph_xy.py is example for reading data and plot data
  
If Run demo program can not find any Raw data output:
      Please set UART to R/W mode: 
      
      pi 3
      $ls -l /dev/ttyS0
      $sudo chmod 666 /dev/ttyS0
      pi 2 
      $ls -l /dev/ttyS0
      $sudo chmod 666 /dev/ttyAMA0
      
**** If the following Error is found ******

    Traceback (most recent call last):
    File "vitalSign_ex2_intr18.py", line 74, in <module>
    GPIO.add_event_detect(18, GPIO.RISING,my_callback)
    RuntimeError: Failed to add edge detection

    *** Please use the following command to clear this Error ****
    ~#gpio unexport 18 


# Data Structure:

    

  # import lib

    from mmWave import trafficMD

  ### raspberry pi 3 use ttyS0
    port = serial.Serial("/dev/ttyS0",baudrate = 921600, timeout = 0.5)

  ### raspberry pi 2 use ttyAMA0
    port = serial.Serial("/dev/ttyAMA0",baudrate = 921600, timeout = 0.5)
    
  ### Jetson Nano use ttyTHS1
	port = serial.Serial("/dev/ttyTHS1",baudrate = 921600, timeout = 0.5)
	 
  ### windows use COMxxx
	port = serial.Serial("COMxxx",baudrate = 921600, timeout = 0.5)
	COMxxx : please modify COM

  ### MacOS use COMxxx
	port = serial.Serial("/dev/tty.usbmodemGY0052534",baudrate = 921600, timeout = 0.5)
	please use $ls /dev/tty* to check file for example "/dev/tty.usbmodemGY0052534"
  
## data structure
	TMD Data Format: [subHeader][objPoint],[objPoint]...]

## Header:
    class subHeader:
	frame: int = 0 #unsign Long
	target: int = 0 #unsign Int
	pcNum : int = 0 #unsign Int Point Cloud Number
## data:
    class objPoint:
	idx: int = 0
	x: float = 0.0
	y: float = 0.0
	vx: float = 0.0
	vy: float = 0.0
	iten : int = 0 # intensity
	tid : int = 0
## define 
    pm = trafficMD.tmdISK_kv(port)

## get kv Data
    (dck,v0,v1)=pm.tmdRead(False)
    dck: data check true: Data is avaliable, false: Data invalid
    v0: subHeader
    v1: objPoint
    
## Reference:

1. LabGuide: https://github.com/bigheadG/mmWaveDocs/blob/master/V20_TMD_18xx_68xx_traffic_monitoring_users_guide.pdf
2. KeyDataProtocol: https://github.com/bigheadG/mmWaveDocs/blob/master/V20_TMD_Protocol_v20_10_pdf.pdf

