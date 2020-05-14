"""
****************************************
version: v1.0 2020/05/13 release
Drone Radar Navigtion API ex0
****************************************
This example will show the DRN radar detected object information.
the information will be V1,V2,V3,V6,V7. Such as object point cloud...

Hardware requirements:
 Batman Kit- 201 DRN mmWave Sensor SDK
 Jetson nano or pi 4
 
**************
Install Jetson nano: Please reference

https://makerpro.cc/2019/05/the-installation-and-test-of-nvida-jetson-nano/
it will teach you how to install
 
(1)install Jetson nano GPIO
    $sudo pip3 install Jetson.GPIO
    $sudo groupadd -f -r gpio
    
    #please change pi to your account
    $cd practice sudo usermod -a -G gpio pi
    
    $sudo cp /opt/nvidia/jetson-gpio/etc/99-gpio.rules /etc/udev/rules.d/
    
    reboot system and run
    
    $sudo udevadm control --reload-rules && sudo udevadm trigger
(2)install mmWave lib
$sudo pip3 install mmWave
(3) upgarde mmWave lib
$sudo pip3 install mmWave -U

************************************************
raspberry pi 4 UART setting issues reference:
https://www.raspberrypi.org/documentation/configuration/uart.md

************************************************

"""
import serial
import struct
import datetime

import numpy as np
from mmWave import droneRN

class globalV:
	count = 0
	def __init__(self, count):
		self.count = count


#use USB-UART
#port = serial.Serial("/dev/ttyUSB0",baudrate = 921600*2, timeout = 0.5)
#
#for Jetson nano UART port
port = serial.Serial("/dev/ttyTHS1",baudrate = 921600*2, timeout = 0.5) 

#for pi 4 UART port
#port = serial.Serial("/dev/ttyS0",baudrate = 921600*2, timeout = 0.5)

v1len = 0
v2len = 0
v3len = 0
v6len = 0
v7len = 0
#
#initial global value
#
gv = globalV(0)
#Drone Object Detect Radar initial 
drn = droneRN.DroneRN(port)
drn.sm = False 
# UART : 50 ms
def uartGetTLVdata(name):
	print("mmWave:Drone Radar Navigation: {:} example:".format(name))
	global v1len,v2len,v3len,v6len,v7len
	
	port.flushInput()
	#drn.stateMachine(True)
	while True:
		(dck,v1,v2,v3,v6,v7) = drn.tlvRead(False)
		#hdr = drn.getHeader()
		#drn.headerShow()
		if dck == 1:
			v1len = len(v1)
			v2len = len(v2)
			v3len = len(v3)
			v6len = len(v6)
			v7len = len(v7)
			#
			#you can use print to print all information
			#
			print("Sensor Data(Len): [v1,v2,v3,v6,v7]:[{:d},{:d},{:d},{:d},{:d}]".format(v1len,v2len,v3len,v6len,v7len))
			print(v1)
			
uartGetTLVdata("DRN")






