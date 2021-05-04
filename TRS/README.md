 # 🚧  Under Construction 🚧 
 # mmWave-TRS (Traffic_Monitoring_Detection Roadway Sensing)
 This repository contains the Batman Kit- Traffic_Monitoring_Detection Roadway Sensing mmWave Sensor SDK.
 The sample code below consists of instruction for using the mmWave lib.
 This mmWave-TRS Python Program will works with Traffic_Monitoring_Detection Roadway Sensing(TRS) based Batman BM201-TRS Kit solution.
 This Python Program works with Raspberry Pi 3/4, Jetson Nano, Windows or Mac computer with Batman BM201-TRS Kit attached via Kit's HAT Board;
 and that the BM201-TRS Kit is an easy-to-use mmWave sensor evaluation kit suitable for tracking multiple object's movements simultaneously from
 5 meter~50 meter range with a high degree of accuracy suitable for traffic monitoring detection's roadway sensing applications for detecting distance,
 speed and direction of trucks & cars (~50 meter), motorcycles (~35 meter), bicycles (~25 meter), and/or walking persons (~20 meter) within a given Zone.
  

# Installing

Library install for Python

    $sudo pip install mmWave
    $sudo pip3 install mmWave

Library update:

    $sudo pip install mmWave -U
    $sudo pip3 install mmWave -U

Examples:

    TRS_kv_ex0.py is a basic example for reading data from BM201-TRS-ISK
    TRS_kv_ex1.py is a basic example for reading data from BM201-TRS-ISK and judge Detected Object
    TRS_kv_ex3_pyqtgraph_2d_xy_config.py is example for config BM201 detect zone and Doppler and plot data
    
    Record and playback:
    
    TRS_kv_ex2_config_rec_DataSet.py is example for record data and config detect zone and object behavior
    TRS_kv_ex4_pyqtgraph_2d_df_recfile_playback is example for record data playback
  
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

    from mmWave import roadwayTMD_kv
 
  ## UART Port Setting
            Data Port: This port is read data from BM201. The data output is dataframe format.
            Config Port: This port provides user to config area and doppler for detect object.
            
            Mac example:
            dataBaudRate = 921600
            configBaudRate = 115200
            port = serial.Serial("/dev/tty.usbmodemGY0052534",baudrate = dataBaudRate , timeout = 0.5)   # Data port
            portCFG = serial.Serial("/dev/tty.usbmodemGY0052531",baudrate = configBaudRate , timeout = 0.5) # config port
            
  ### raspberry pi 3 use ttyS0
    port = serial.Serial("/dev/ttyS0",baudrate = 921600, timeout = 0.5)

  ### raspberry pi 2 use ttyAMA0
    port = serial.Serial("/dev/ttyAMA0",baudrate = 921600, timeout = 0.5)
    
  ### Jetson Nano use ttyTHS1
	port = serial.Serial("/dev/ttyTHS1",baudrate = 921600, timeout = 0.5)
	 
  ### windows use COMxxx
	port = serial.Serial("COMxxx",baudrate = 921600, timeout = 0.5)
	COMxxx : please modify COM

  ### MacOS use tty.usbmodemxxx
	port = serial.Serial("/dev/tty.usbmodemGY0052534",baudrate = 921600, timeout = 0.5)
	please use $ls /dev/tty* to check file for example "/dev/tty.usbmodemGY0052534"
  
## data structure
	TRS Data Format: [subHeader][objPoint],[objPoint]...]

## Header:
    class header:
        version = 'v0.1.1'
        frameNumber = 0
        
    hdr = trs.getHeader() 
    fn = hdr.frameNumber #get frame number
    
## v21 data:
    
    Detected Object dataFrame : ['flow','fn','indexMax','index','x','y','range','doppler','area','ptsNum','cid']
    flow: flow data
    fn: frame number
    indexMax: indexMax = 0 means not object detected the x,y are equal 0,0
    index: detected object index
    x,y : object position
    range: range = sqrt(x*x + y*y)
    doppler: m/sec
    ptsNum: point cloud form a cluster(object)
    cid: cluster/object ID
    
## define 
    trs = roadwayTMD_kv.roadwayTmdISK_kv(port)

## get kv Data

    (dck,v21)=trs.trsRead(False)
    dck: data check true: Data is avaliable, false: Data invalid
    v21: is a detected object dataFrame  
     
## read record data file(csv) and get a record data based on frame number:
 	
	(1) read record data from file (for playback)
	
	v21 = trs.readFile(fileName)
	
	v21 data fields from file = ['fn','indexMax','index','x','y','range','doppler','area','ptsNum','NotObject','MAN','MotorCycle','car','CAR']
	usage:
	v21Read = trs.readFile("Roadwaytmd_2021-04-28-10-56-07.csv")

	--------------v21Read----------------
        fn  indexMax  index         x  ...  MAN  MotorCycle  car  CAR
	0   8526.0       2.0    0.0  1.012783  ...    0           0    0    1
	1   8526.0       2.0    1.0  1.007694  ...    0           0    0    1
	2   8527.0       3.0    0.0 -0.091609  ...    0           0    0    1
	3   8527.0       3.0    1.0  1.183277  ...    0           0    0    1
	4   8527.0       3.0    2.0  0.471129  ...    0           0    0    1
	..     ...       ...    ...       ...  ...  ...         ...  ...  ...
	93  8576.0       2.0    0.0  1.870340  ...    0           0    0    1
	94  8576.0       2.0    1.0  1.192607  ...    0           0    0    1
	95  8577.0       2.0    0.0  1.334430  ...    0           0    0    1
	96  8577.0       2.0    1.0  1.893243  ...    0           0    0    1
	97  8578.0       1.0    0.0  1.290153  ...    0           0    0    1

	[98 rows x 14 columns]
	
	(2) get a record data based on frame number (for playback)
	
	(chk,cur_rec) = trs.getRecordData(frameNum)
	
	chk: data check true: Data is avaliable, false: Data invalid
	cur_rec: Obtain v21 objects data according to the frame number
	
	usage:
	(chk,cur_rec) = trs.getRecordData(int(8526))
	
	-----------frameNum:(sim_startFN:fn)=(8526.0:0)--------------:8526.0
	       fn  indexMax  index         x  ...  MAN  MotorCycle  car  CAR
	0  8526.0       2.0    0.0  1.012783  ...    0           0    0    1
	1  8526.0       2.0    1.0  1.007694  ...    0           0    0    1

	[2 rows x 14 columns]



## Zone parameter configuration:
	
    Command Syntax:
    jb_zoneCfg <flag> <min_x> <max_x> <min_y> <max_y> <min_d> <max_d> 
    for example:
        "jb_zoneCfg 1.0 -0.5 8.0 0.0 70.0 -150.0 -0.01 \x0d\x0a"
    zone parameter:
        flag := 1.0     //enable using new parameters
        min_x := -0.5   //unit: m
        max_x := 8.0    //unit: m
        min_y := 10.0   //unit: m
        max_y := 70     //unit: m 
        min_d := -150   //unit: km/Hr  
        max_d := -0.01  //unit: km/Hr
    
## Record TRS data:
![MainMenu 1](https://github.com/bigheadG/imageDir/blob/master/trs-record_ex2.png)

## Record data Playback: (work with TRS-ToolKit hardware)
![MainMenu 1](https://github.com/bigheadG/imageDir/blob/master/trs-ex3.png)

## Reference:

1. LabGuide: https://github.com/bigheadG/mmWaveDocs/blob/master/V20_TMD_18xx_68xx_traffic_monitoring_users_guide.pdf
2. KeyDataProtocol: https://github.com/bigheadG/mmWaveDocs/blob/master/V20_TMD_Protocol_v20_10_pdf.pdf

