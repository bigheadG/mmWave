''' 
Vehicle Occupancy Detection(VOD) and Child Presence Detection(CPD)
ex0:
Display Object TLV data

(1)Download lib:

install:
~#sudo pip3 intall mmWave
update:
~#sudo pip3 install mmWave -U
'''

import serial

from mmWave import vehicleODHeatMap

#UART initial
#
# Notes: if permission not ALLOWED, please run > sudo chmod 777 /dev/tty* 
#
#############################       UART     ##################################
#
#use USB-UART
#port = serial.Serial("/dev/ttyUSB0",baudrate = 921600, timeout = 0.5)
#
#for Jetson nano UART port
#port = serial.Serial("/dev/ttyTHS1",baudrate = 921600, timeout = 0.5) 
#
#for pi 4 UART port
#port = serial.Serial("/dev/ttyS0",baudrate = 921600, timeout = 0.5)
#
#for Mac
#port = serial.Serial("/dev/tty.usbmodemGY0052854",baudrate = 921600, timeout = 0.5)
port = serial.Serial("/dev/tty.usbmodemGY0052534",baudrate = 921600, timeout = 0.5)
#for NUC ubuntu 
#port = serial.Serial("/dev/ttyACM1",baudrate = 921600, timeout = 0.5)
#
###############################################################################

zd = vehicleODHeatMap.VehicleODHeatMap(port)

def uartGetTLVdata(name):
	print("===================================================================")
	print("mmWave:Vehicle Occupancy Detection and Child Presence Detection {:} example:".format(name))
	print("===================================================================")
	
	port.flushInput()
	#zd.useDebug(False)
	#zd.stateMachine(True)
	#zd.checkTLV(False)

	while True:
		(dck,v8,v9,v10) = zd.tlvRead(False) 
		if dck:
			print("+++++++frame:{:d} v8:len={:d}  v9:len={:d}  v10:len={:d} +++++++++".format(zd.hdr.frameNumber,len(v8),len(v9),len(v10)))
			print("----V9------")
			print(v9)
			print("----V10------")
			print(v10)
			#print(v8)
			print("++++++++++++++++++++++++")
			#zd.headerShow()

uartGetTLVdata("VOD_CPD")






