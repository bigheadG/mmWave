''' 
High Accuracy Measurement(HAM)  : 2019/2/13 15:47
ex0:
Display object distance

(1)Download lib:

install:
~#sudo pip intall mmWave
update:
~#sudo pip install mmWave -U

'''
import serial
import struct
import datetime
import numpy as np
from mmWave import highAccuracy

class globalV:
	count = 0
	rangeValue = 0.0
	br = 0.0
	def __init__(self, count):
		self.count = count
		
#UART initial
try:    #pi 3
	port = serial.Serial("/dev/ttyS0",baudrate = 921600, timeout = 0.5)
except: #pi 2
	port = serial.Serial("/dev/ttyAMA0",baudrate = 921600, timeout = 0.5)
	
#
#initial global value
#
gv = globalV(0)
ham = highAccuracy.HighAccuracy(port)

# UART : 50 ms
def uartGetTLVdata(name):
	print("mmWave:High Accuracy Measuremnet {:} example:".format(name))
	pt = datetime.datetime.now()
	ct = datetime.datetime.now()
	port.flushInput()
	while True:
		#print(datetime.datetime.now().time())
		(dck , hd, rangeBuf) = ham.tlvRead(False)
		
		'''
		h = ham.getHeader()
		d = ham.getDetectedObject()
		s = ham.getStatsInfo()
		print("Version:{:}".format(h.version))
		print("Q Value:{:d}".format(d.descriptor_q))
		print("Structure Tag:{:d}".format(s.stt))
		'''
		
		if dck:
			ct = datetime.datetime.now()
			gv.rangeValue = hd.rangeValue 
			print("Range:{:.4f} m".format(gv.rangeValue))
			pt = ct
			rp = ham.getRangeProfileInfo()
			print("Struct Tag Type:{:d}  Length Of Structure:{:d} (Real for 4bytes + Image for 4Bytes) 512 * 8 bytes".format(rp.structureTag, rp.lengthOfStruct))
			print("Rangebuf length [r0,i0...r511,i511]:" + str(len(rangeBuf)))
			print("*********** end ***************")
			port.flushInput()

uartGetTLVdata("HAM")






