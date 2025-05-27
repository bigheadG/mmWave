# mmWave_zyyx
This repository contains the mmWave-PC3 People Counting & Detection mmWave Sensor SDK for using Batman BM201-PC3 mmWave Kit solution. The sample codes in this GitHub Folder consist of instruction for using the mmWave lib. The Python Programs in this Folder work with a Raspberry Pi 4 & NVIDIA Jetson Nano attached via Kit’s HAT Board, or work with Windows/Linux computer or MAC computer via EM110 Emulator attached to the Kit; for People Sensing, People Counting, or People Occupancy Density Estimation in approx. 10m x 10m area (Azimuth FOV with radius of 10m) without privacy invasion; and where the Python Programs would have multiple people detection in a 3-Dimentional Area with ID tag, posX, posY, posZ, velx, vely, velz, accX, accY, accZ parameters, along with Point Clouds with Elevation, Azimuth, Doppler, Range, and SNR parameters.

# Hardware:
    Batman kit-201 (ISK)
data sheet:
https://github.com/bigheadG/mmWaveDocs/blob/master/Datasheet_BM201_K_C.pdf

# installing:
    pySerial Library
    $sudo pip3 install pySerial
    
    pandas Library
    $sudo pip3 install pandas
   
# import 
    from mmWave import pc3_v1884R     
    
# UART Setting:

### PC Windows use COM12 (for example)
    port = serial.Serial("COM12",baudrate = 921600, timeout = 0.5)

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


# define
    
    radar =  pc3_v1884R.pc3_v1884R(port) 
    
    (dck,v1010,v1011,v1012,v1020,v1021) = radar.tlvRead(False)
    fn = radar.frameNumber
    
    notes:
        dck: data valid chcek
        v1010: target
        v1011: target index
        v1012: target height
        v1020: point cloud [(sx,sy,sz,ran,elv,azi,dop,snr,fn).....]
        v1021: Prescence Indication
    
    
    
# Data structure (RAW data):
  V1020: Point Cloud<br/>
Each Point Cloud list consists of an array of points,Each point data structure is defined as following
   
    point Struct:
        sx :      float #point position x
        sy :      float #point position y
        sz :      float #point position z
        range:    float   #Range in meters
        elevation: float  #Elevation in radians
        azimuth:  float   #Azimuth in radians 
        doppler:  float   #Doppler in m/s
        snr:      float   #SNR, ratio
        fn:       Int     #Frame Number
        
V1020 data present:
<img width="1151" alt="image" src="https://user-images.githubusercontent.com/2010446/209495538-f6e25c9c-e1c5-454f-ab3f-8f1b6b5d1980.png">

        
V1010: Target Object<br/>
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
        
V1011: Target Index<br/> 
Each Target List consists of an array of target IDs, A targetID at index i is the target to which point i of the previous frame's point cloud was associated. Valid IDs range from 0-249
        
    TargetIndex Struct(V1011):
        tragetID: Int #Track ID
        {targetID0,targetID1,.....targetIDn}
        
        Other Target ID values:
        253:Point not associated, SNR to weak
        254:Point not associated, located outside boundary of interest
        255:Point not associated, considered as noise

V1012: Target Height<br/> 
        
        Target Height Structure:
        tid: Int  #tracking ID
        maxZ: float # Detected maximum Z coordinate, in m
        minZ: float # Detected maximum Z coordinate, in m

V1010 & V1012 data presents:
<img width="1249" alt="image" src="https://user-images.githubusercontent.com/2010446/209494942-6656c0b0-8141-4b2c-9322-523a28289777.png">

 

V1021: Prescence Indication<br/> 
        
        presenceInd:  Int #Prescence Indication
    
    
Based on IWR6843 3D(r,az,el) -> (x,y,z)
    el: elevation φ <Theta bottom -> Obj    
    az: azimuth   θ <Theta Obj ->Y Axis 
    
    z = r * sin(φ)
    x = r * cos(φ) * sin(θ)
    y = r * cos(φ) * cos(θ)
    
 ![MainMenu 1](https://github.com/bigheadG/imageDir/blob/master/objGeoSmall.png)  
    

    
    

# Getting Started: (run following examples)
    
    (Step 1) Verifying system integration 
    The first python program can be used as Hardware (Batman kit-201) Veirification purpose
    run on mmWave_pc3_1884r_ex0.py      #display radar information (raw data)
    
    (Step 2) Easy reading format
    This python program is the same as above which dataFrame format is more easier for reading 
    run on mmWave_pc3_1884r_ex1.py      #display radar information by pandas (dataFrame type)

    (Step 3) Running Algorithm
    Please change the folder to /mmap_run/linux 
    then reading README first for Getting Started 

# (1) mmWave_pc3_1884r_ex0.py
    
Report as following, 
    
![image](https://user-images.githubusercontent.com/2010446/209753686-8374914a-0e82-4ef9-a967-c266cf8222e1.png)



# recording data (type:v1020):
<img width="1374" alt="image" src="https://user-images.githubusercontent.com/2010446/209308792-27eefd33-535f-488f-83c2-44e71e43e755.png">


 


## Reference:

1. Data Structure: [jb_V1884R_PC3_10m_55ms_V03.pdf](https://github.com/bigheadG/mmWave_zyyx/files/10292192/jb_V1884R_PC3_10m_55ms_V03.pdf)

2. Block Diagram 1: [Block Diagram1-20221229001.pdf](https://github.com/bigheadG/mmWave_zyyx/files/10317558/Block.Diagram1-20221229001.pdf)

3. Block Diagram 2: [Block Diagram2-20221229001.pdf](https://github.com/bigheadG/mmWave_zyyx/files/10317560/Block.Diagram2-20221229001.pdf)
