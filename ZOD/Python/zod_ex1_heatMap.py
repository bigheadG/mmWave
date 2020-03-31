#
# ZOD: Zone Occupant Detection
# ZOD: Y: Range 0~3m [0..64]
#     X: Range: (-60deg ~ +60deg) [0..48]
#
# UART Baud Rate: 921600
# 
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import time

import serial
from mmWave import vehicleOD
import sys
from threading import Thread
#UART initial
#Jetson nano
port = serial.Serial("/dev/ttyTHS1",baudrate = 921600, timeout = 0.5)
#raspberry pi 4
#port = serial.Serial("/dev/ttyS0",baudrate = 921600, timeout = 0.5)

pm = vehicleOD.VehicleOD(port)

heatA = np.zeros((64,48))

def animate(xdata, im):
	global heatA
	im.set_data(heatA)


def uartThread(name):
	global heatA
	cnt = 0
	port.flushInput()
	#pm.useDebug(False)
	#pm.stateMachine(True)
	#pm.checkTLV(True)
	while True:
		(dck,v8,v9,v10,v11) = pm.tlvRead(False)
		if dck:
			cnt += 1
			xa = np.amax(v8) 
			maxa = 1.0 if xa == 0 else xa 		
			heatA = np.array(v8).reshape((64,48)) / maxa

			NUM = sum(sum(heatA))
			print('\nJB> sum={}\n'.format( NUM ))
			
			#print(heatA.shape)
			#print("v8:len={:d}  v9={:d}  v10={:d}  v11={:d}".format(len(v8),len(v9),len(v10),len(v11)))
			#print(v11)
			#print(v9)
			#print(v11)
			#pm.headerShow()
			port.flushInput()
    

fig, ax = plt.subplots()
im = ax.imshow(np.random.rand(64, 48), interpolation= 'nearest' ) #'bilinear') #interpolation='nearest')

thread1 = Thread(target = uartThread, args =("UART",))
thread1.setDaemon(True)
thread1.start()

ani = animation.FuncAnimation(
    fig, animate, interval=200, repeat=True, fargs=(im, ))
plt.show()

