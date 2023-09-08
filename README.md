# mmWave based on AI (by request with purcahse of corresponding AI enabled mmWave EVM Kit)


https://user-images.githubusercontent.com/2010446/141447812-ecb79563-1f78-440d-9533-c14793f3fec2.mov

# mmWave based on PC3 360 degree application(BM501)

https://user-images.githubusercontent.com/2010446/176392496-6d01bb21-8c48-42b0-9875-4303d25188f1.MOV



# mmWave
mmWave SDK examples based on Batman Kit mmWave Sensor module
This App works with Raspberry Pi 3, Pi 2 , Pi 4, Jetson Nano ,Windows, MacOS or Intel NUC.
Run this repository example needs install mmWave lib. Those examples are<br/>

VSD,HAM,PMB,SRR,LPD,PC3D,TMD,ZOD,SVD,DRN,VOD,PC3,POS, PCR and VED examples:<br/><br/> 
VSD:	Vital Signs Detection.<br/> 
HAM:	High Accuracy Measurement.<br/>
PMB:	People Moving Behavior.<br/>
SRR:	Short Range Radar.<br/>
LPD:	Long range People Detection.<br/>
PC3D:	People Overhead Counting 3D.<br/>
TMD:	Traffic Monitor Detection.<br/>
ZOD:	Zone Occupancy Detection.<br/>
SVD:	Surface Velocity Detection.<br/>
DRN:	Drone Radar Navigation.<br/>
VOD:	Vehicle Occupancy Detection.<br/>
PC3:	People Counting Detection.<br/>
PC3_v2:	People Counting Detection 3D version:2.<br/>
TRS:    Traffic_monitoring_detection Roadway Sensing.<br/>
POS:	People counting Overhead Sensor.<br/>
PCR:    People Counting short Range sensing.<br/>
VED:    Vital Energy Detection.

# mmWave Data Sheet:
BM101: https://github.com/bigheadG/mmWaveDocs/blob/master/Datasheet_BM101_F_C.pdf (deprecated) <br/> 
BM201: https://github.com/bigheadG/mmWaveDocs/blob/master/Datasheet_BM201_I_C.pdf <br/> 
BM301: https://github.com/bigheadG/mmWaveDocs/blob/master/Datasheet_BM301FDS_D_C.pdf (deprecated) <br/> 
BM501-Module: https://github.com/bigheadG/mmWaveDocs/blob/master/Datasheet_BM501_M_A_C.pdf <br/> 
BM502-Module: https://github.com/bigheadG/mmWaveDocs/blob/master/Datasheet_BM502_M_A_C.pdf <br/> 
BM601-Module: https://github.com/bigheadG/mmWaveDocs/blob/master/Datasheet_BM601_M_A_C.pdf <br/> 
BM501-EVK: https://github.com/bigheadG/mmWaveDocs/blob/master/Datasheet_BM501_D_C.pdf <br/>



## Youtube Demo:

[![Watch the video](https://github.com/bigheadG/imageDir/blob/master/YouTube-icon-full_color.png)](https://www.youtube.com/playlist?list=PL4QD4eKmMP2WvnZ4I8-AomJjiYkygw3G2 "Watch the Video")
	
# Hardware requirements:
      
       VSD: Batman kit 101/201/501(AOP): IWR1642-VSD/IWR6843-VSD/IWR6843AOP-VSD
       HAM: Batman kit 101/201: IWR1642-HAM/IWR6843-HAM
       PMB: Batman kit 101/201: IWR1642-PMB/IWR6843-PMB
       SRR: Batman kit 101: IWR1642-SRR
       
       LPD: Batman kit 201: IWR6843-LPD
       PC3D: Batman kit 301: IWR6843-PC3D
       TMD: Batman kit 201: IWR6843-TMD
       ZOD: Batman kit 201(ISK) :IWR6843-ZOD
       SVD: Batman Kit 201(ISK) :IWR6843-SVD
       DRN: Batman Kit 201(ISK) :IWR6843-DRN
       VOD: Batman Kit 201(ISK) :IWR6843-VOD
       PC3: Batman Kit 201(ISK) :IWR6843-PC3 and BM501 AOP-PC3
       PC3_v2: Batman Kit 201(ISK)/501(AOP) :IWR6843-PC3 and BM501 AOP-PC3
       TRS: Batman Kit 201(ISK) :IWR6843-TRS
       POS: Batman Kit 201(ISK)/501(AOP) :IWR6843-POS and BM501 AOP-POS
       PCR: Batman Kit 201(ISK) :IWR6843-PCR and BM501 AOP-PCR
       VED: Batman Kit 201(ISK) :IWR6843-VED and BM501 AOP 


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
      
      pandas Library
      $sudo pip3 install pandas
      
      scikit-learn Library
      $sudo pip3 install scikit-learn
      
      pyqtgraph Library
      $sudo pip3 install pyqtgraph
      https://pyqtgraph.readthedocs.io/en/latest/installation.html
      
      
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


# For pyqtgraph v0.13.1 users need to replace the three parts of the code in the file. 
## Method 1:	
	############################################
	#(1) for pyqtgraph Version: 0.13.1
	import pyqtgraph as pg
	import pyqtgraph.opengl as gl
	from pyqtgraph.Qt import mkQApp ,QtCore ,QtGui

	''' # remove
	# before pyqtgraph Version: 0.13.1
	from pyqtgraph.Qt import QtCore, QtGui
	import pyqtgraph.opengl as gl
	import pyqtgraph as pg
	'''
	
	############################################
	#(2)
	app = mkQApp("PCT") #for pyqtgraph v0.13.1
	#app = QtGui.QApplication([]) #remove 
	
	############################################
	#(3)#for pyqtgraph v0.13.1
	if __name__ == '__main__':
   		 pg.exec()
  
	''' # remove
	#before pyqtgraph Version: 0.13.1 
	if __name__ == '__main__':
	    import sys
	    if (sys.flags.interactive != 1) or not hasattr(QtCore,'PYQT_VERSION'):
		QtGui.QApplication.instance().exec_()
	'''
	############################################
 	setDaemon() is deprecated, set the daemon attribute instead
 	remove thread1.setDaemon(True)
  	add    thread1.daemon = True
  	############################################
   
        for pyqtgraph V0.13.1 
	remove : circle = pg.QtGui.QGraphicsEllipseItem(-r, -r, r * 2, r * 2)
 	add new line : circle = pg.QtWidgets.QGraphicsEllipseItem(-r, -r, r * 2, r * 2)
  	example :
	for r in range(1, 10, 1):
        #circle = pg.QtGui.QGraphicsEllipseItem(-r, -r, r * 2, r * 2)
         circle = pg.QtWidgets.QGraphicsEllipseItem(-r, -r, r * 2, r * 2)
         circle.setPen(pg.mkPen(1.0))
         w0.addItem(circle)

## Method 2
	############################################
	#(1) for pyqtgraph Version: 0.13.1
	from PyQt5 import QtGui, QtWidgets, QtCore   
	#from PyQt5.QtGui import QPen, QColor
	import pyqtgraph as pg
	import pyqtgraph.opengl as gl
	from pyqtgraph.Qt import mkQApp, QtGui

	''' # remove
	# before pyqtgraph Version: 0.13.1
	from pyqtgraph.Qt import QtCore, QtGui
	import pyqtgraph.opengl as gl
	import pyqtgraph as pg
	'''
	
	############################################
	#(2)
 	app = QtWidgets.QApplication([])      
	
 	# remove 
	#app = QtGui.QApplication([]) #remove 
	
	############################################
	#(3.0)#for pyqtgraph v0.13.1
	if __name__ == '__main__':
		 pg.exec()
     	
        #(3.1) 
	if __name__ == '__main__':
		import sys
		if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'): 
			#QtGui.QApplication.instance().exec_()     # for windows
			QtWidgets.QApplication.instance().exec_()  # for linux
 
	# remove
 	'''
	#before pyqtgraph Version: 0.13.1 
	if __name__ == '__main__':
	    import sys
	    if (sys.flags.interactive != 1) or not hasattr(QtCore,'PYQT_VERSION'):
		QtGui.QApplication.instance().exec_()
	'''
 
 	circle for pyqtgraph V0.13.1 
	remove : circle = pg.QtGui.QGraphicsEllipseItem(-r, -r, r * 2, r * 2)
 	add new line : circle = pg.QtWidgets.QGraphicsEllipseItem(-r, -r, r * 2, r * 2)
  	example :
	for r in range(1, 10, 1):
        #circle = pg.QtGui.QGraphicsEllipseItem(-r, -r, r * 2, r * 2)
         circle = pg.QtWidgets.QGraphicsEllipseItem(-r, -r, r * 2, r * 2)
         circle.setPen(pg.mkPen(1.0))
         w0.addItem(circle)



## Please refer to https://github.com/bigheadG/pyqtgraph_3d_text when you find the following errors when executing the 3d program

	Error while drawing item <__main__.CustomTextItem object at 0x7f7950a9c4c0>.
	Error while drawing item <__main__.CustomTextItem object at 0x7f7950a9c550>.
	
	

	
