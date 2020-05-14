# mmWave
mmWave SDK examples based on Batman Kit mmWave Sensor module
This App works with Raspberry Pi 3, Pi 2 , Pi 4 and Jetson Nano
,Windows and MacOS.
Run this repository example needs install mmWave lib.
Those examples are VSD,HAM,PMB,SRR,PC3D,TMD examples: 
VSD stands for Vital Signs Detection, 
HAM stands for High Accuracy Measurement,
PMB stands for People Moving Behavior,
SRR stands for Short Range Radar,
LPD stands for Long range People Detect,
PC3D stands for People Overhead Counting 3D,
TMD stands for Traffic Monitor Detection,
ZOD stand for Zone Occupancy Detection,
SVD stand for Surface Velocity Detection
DRN stand for Drone Radar Navigation

# Youtube Demo

	[![Watch the video](https://github.com/bigheadG/mmWave/blob/master/people160.png)](https://www.youtube.com/watch?v=MmQOeToe7vE&feature=youtu.be "Watch the video")
	
	
# Hardware requirements:
      
       VSD: Batman kit 101: IWR1642-VSD
       HAM: Batman kit 101: IWR1642-HAM
       PMB: Batman kit 101: IWR1642-PMB
       SRR: Batman kit 101: IWR1642-SRR
       
       LPD: Batman kit 201: IWR6843-LPD
       PC3D: Batman kit 301: IWR6843-PC3D
       TMD: Batman kit 201: IWR6843-TMD
       ZOD: Batman kit 201(ISK) :IWR6843-ZOD
       SVD: Batman Kit 201(ISK) :IWR6843-SVD
       DRN: Batman Kit 201(ISK) :IWR6843-DRN


# Install Library:
      mmWave Library
      $sudo pip3 install mmWave
      
      tkinter Library
      $sudo pip3 install tkinter
      or
      $sudo apt-get install python3-tk python-tk
      
      numpy Library
      $sudo pip3 install numpy
      or
      $sudo apt-get install python3-numpy python-numpy
      
      NOOBS_V3 is installed already
      pySerial Library
      $sudo pip3 install pySerial
      
      RPi.GPIO library please reference:
      https://www.raspberrypi-spy.co.uk/2012/05/install-rpi-gpio-python-library/
      
 ## Some install problem the following information for reference:
      (1)-------libf77blas.so.3-----------------------------------------
      from scipy.linalg import _fblas
      ImportError: libf77blas.so.3: cannot open shared object file: No such file or directory

      problem solved:
      First of all, for libf77blas.so.3, you have to install ATLAS, something like sudo apt-get install libatlas-base-dev

      $sudo apt-get install libatlas-base-dev
      (2)-----------------------------------------
      Traceback (most recent call last):
      File "/usr/lib/python3/dist-packages/serial/serialposix.py", line 265, in open
      self.fd = os.open(self.portstr, os.O_RDWR | os.O_NOCTTY | os.O_NONBLOCK)
      FileNotFoundError: [Errno 2] No such file or directory: '/dev/ttyS0'

      problem solved:

      (1)menu->perference->Raspberry pi Configuration->Serial Port(Enable)
      (2)reboot:
      (3)$ls -l /dev/ttyS0
            crw--w---- 1 root tty       4, 64 Nov  1 04:21 /dev/ttyS0
      (4)$sudo chmod +666 /dev/ttyS0
      (5)pi@raspberrypi:~ $ ls -l /dev/ttyS0
	      crw-rw-rw- 1 root tty 4, 64 Nov  1 04:21 /dev/ttyS0


# How to Enable RPi UART port:
Enable UART:

      1:[MainMenu] -> [Preferences] -> [Raspberry Pi Configuration]
      
![MainMenu 1](https://github.com/bigheadG/imageDir/blob/master/UART0.jpeg)         


      2:Select [Interface Tab] in Raspberry Pi Configuration
      
      3:Enable Serial Port: Check radio RadioButton

![MainMenu 1](https://github.com/bigheadG/imageDir/blob/master/UART1.jpeg) 

      4:List tty Device
      
      $ls /dev/tty*
      $sudo chmod +666 /dev/ttyS0
      or 
      $sudo chmod +666 /dev/ttyAMA0
      
      Reboot
      
![MainMenu 1](https://github.com/bigheadG/imageDir/blob/master/UART3.jpeg)  

# UART Still can not work, Please check cmdline.txt
	$cat /boot/cmdline.txt
	
	if you find the console=serial0,115200 in cmdline.txt. please use raspi-config to remove it.
	
	$sudo raspi-config 
	then reboot
	
	Detailed information please reference:
	
	https://www.raspberrypi.org/documentation/configuration/uart.md

# Video Demo(Press ICON to watch the Video)

## Vital Signs Detection:
[![Watch the Video](https://github.com/bigheadG/mmWave/blob/master/heart160.png)](https://youtu.be/4MSrxUmm69M "Watch the Video")
## High Accuracy Measurement:
[![Watch the video](https://github.com/bigheadG/mmWave/blob/master/measure160.png)](https://youtu.be/IEmM7JIqtTc "Watch the Video")
## People Moving Behavior:
[![Watch the video](https://github.com/bigheadG/mmWave/blob/master/people160.png)](https://youtu.be/KuTrT1_m29k "Watch the Video")
## Short Range Radar:
[![Watch the video](https://github.com/bigheadG/mmWave/blob/master/people160.png)](https://youtu.be/KuTrT1_m29k "Watch the Video")
## People Overhead Counting 3D:
[![Watch the video](https://github.com/bigheadG/mmWave/blob/master/people160.png)](https://youtu.be/KuTrT1_m29k "Watch the Video")
