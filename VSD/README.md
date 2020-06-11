# mmWave-VSD (Vital Signs Detection)
This repository contains the Batman Kit- VSD mmWave Sensor SDK. 
The sample code below consists of instruction for using the mmWave lib.
This mmWave-VSD Python Program will work with Vital Signs Detection (VSD) based mmWave Batman Kit solution.
This App works with Raspberry Pi 3 / Pi 2 and Jetson Nano
The Vital Signs Detection (VSD) based Batman Kit is for a contactless and wearableless and 30cm ~ 90cm (about 1~3 feet) distance detection of Vital Signs (Heartbeat Rate & Respiration Rate) of a person, a pet, or an animal. 


# Installing

Library install for Python

    $sudo pip install mmWave
    $sudo pip3 install mmWave

Library update:

    $sudo pip install mmWave -U
    $sudo pip3 install mmWave -U

Examples:

    vitalSign_ex0.py is a basic example for reading data from Batman EVK
    vitalSign_ex1_Thread.py is an example of using thread to read data from Batman EVK
    vitalSign_ex2_intr18.py is an example of using GPIO Pin18 rise-edge to trigger function to read data from Batman EVK
    pyqtgraph_vsd_ex3.py is an example of use [chest displacement waveform] -> [filter] -> 
    [windowing] -> fft to get Breathing & heart rate
   
    
![MainMenu 1](https://github.com/bigheadG/imageDir/blob/master/vitalSignFFT.png)
pyqtgraph_vsd_ex3.py screen shot

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

    VS Data Format: [Frame Header][VSOS][Range Profile]

## Header:
    class header:
	    version = ""
	    totalPackLen =0
	    tvlHeaderLen = 8
	    platform = ""
	    frameNumber = 0
	    timeCpuCycles = 0
	    numDetectedObj = 0
	    numTLVs = 0
	    rsv = 0
	
    function call: getHeader(self)
		    return header type data
		
    Show header infomation:
    function call: headerShow(self)
		

## Vital Signs Output Stats:

    class vsos:
	    rangeBinIndexMax  = 0 
	    rangeBinIndexPhase = 0 
	    maxVal  = float(0.0)
	    processingCyclesOut =  0 
	    processingCyclesOut1 =  0 
	    rangeBinStartIndex  =  0 
	    rangeBinEndIndex    =  0  
	    unwrapPhasePeak_mm  = float(0.0)
	    outputFilterBreathOut = float(0.0)
	    outputFilterHeartOut = float(0.0)
	    heartRateEst_FFT     = float(0.0)
	    heartRateEst_FFT_4Hz  = float(0.0)
	    heartRateEst_xCorr   = float(0.0)
	    heartRateEst_peakCount  = float(0.0)
	    breathingRateEst_FFT   = float(0.0)
	    breathingEst_xCorr     = float(0.0)
	    breathingEst_peakCount  = float(0.0)
	    confidenceMetricBreathOut  = float(0.0)
	    confidenceMetricBreathOut_xCorr  = float(0.0)
	    confidenceMetricHeartOut   = float(0.0)
	    confidenceMetricHeartOut_4Hz  = float(0.0)
	    confidenceMetricHeartOut_xCorr  = float(0.0)
	    sumEnergyBreathWfm = float(0.0)
	    sumEnergyHeartWfm  = float(0.0)
	    motionDetectedFlag = float(0.0)
	    rsv  = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]


# TLV Data: Type-Length-Value
    function call: (chk,vd,rangeBuf) = tlvRead(dbg)
	    dbg := True, enable debug message
	         False, disable debug message
	       
	    chk := True: Data valid
		         False: Data invalid
		   
	    vd := Vital Signs Output Stats
	 
	    rangeBuf := [Complex(r0,i0),Complex(r1,i1)...Complex(r18,i18)]
	      Length of rangeBuf is 38 equal to 19 sets complex data
        rangeBuf is range profile data



# import lib

    from mmWave import vitalsign

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
    vts = vitalsign.VitalSign(port)

## get tlv Data
    (dck , vd, rangeBuf) = vts.tlvRead(False)

## Reference:

1. LabGuide: https://github.com/bigheadG/mmWaveDocs/blob/master/DriverVitalSigns_DevelopersGuide.pdf
2. KeyDataProtocol: https://github.com/bigheadG/mmWaveDocs/blob/master/V1_vitalSignsBLEProtocol_v01_02_pdf.pdf
3. KeyDataProtocol_withStatus: https://github.com/bigheadG/mmWaveDocs/blob/master/V01_VSD_vitalSignsBLEProtocol_v01_03_pdf.pdf
   
   ALERT: above Status feature is supported on version V01.54 or V30.02 or later
