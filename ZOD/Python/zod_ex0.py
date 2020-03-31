''' 
Vehicle Occupant Detection and Driver Vital Sign
ex0:
Display Object TLV data

(1)Download lib:

install:
~#sudo pip3 intall mmWave
update:
~#sudo pip3 install mmWave -U
'''
import serial

from mmWave import vehicleOD
#import vehicleOD as vehicleOD

#UART initial
#ALERT: if permission not ALLOWED, please run > sudo chmod 777 /dev/ttyT* 
#Jetson nano
port = serial.Serial("/dev/ttyTHS1",baudrate = 921600, timeout = 0.5)
#raspberry pi 4
#port = serial.Serial("/dev/ttyS0",baudrate = 921600, timeout = 0.5)

pm = vehicleOD.VehicleOD(port)

def uartGetTLVdata(name):
	print("===================================================================")
	print("mmWave:Vehicle Occupant Detection and Driver Vital Sign {:} example:".format(name))
	print("===================================================================")
	
	port.flushInput()
	#pm.useDebug(False)
	#pm.stateMachine(True)
	pm.checkTLV(True)
	
	while True:
		(dck,v8,v9,v10,v11) = pm.tlvRead(False)
		if dck:
			#print("v8:len={:d}  v9={:d}  v10={:d}  v11={:d}".format(len(v8),len(v9),len(v10),len(v11)))
			print("V8:len={:d}, value={}".format(len(v8), v8[0:5]))
			#print(v8[0:5])
			#print(v11)
			#print(v10)
			#print(v9)
			#vs = pm.getVitalSign()
			#print(v11)
			#pm.headerShow()

			
uartGetTLVdata("VOD")






