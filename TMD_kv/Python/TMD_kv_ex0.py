''' 
Target Monitor Detect (ISK) for BM-201" : 2020/03/09
ex0:
Hardware: Batman-201 ISK


(1)Download lib:
install:
~#sudo pip intall mmWave
update:
~#sudo pip install mmWave -U
'''

import serial
import numpy as np
from mmWave import trafficMD_kv
#import trafficMD as TrafficMD

port = serial.Serial("COM189",baudrate = 921600, timeout = 0.5)
pm = trafficMD_kv.tmdISK_kv(port)

def uartGetdata(name):
	print("mmWave: {:} example:".format(name))
	port.flushInput()
	while True:
		(dck,v0,v1)=pm.tmdRead(False) 
		if dck:
			print("=====v0 info.=====")
			print(v0)
			print("=======v1=====")
			print(v1)
			
			
uartGetdata("Traffic Monitor Detect (TMD) for BM-201")
