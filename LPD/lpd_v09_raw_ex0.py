''' 
Long range People Detect (ISK) for BM-201" : 2019/12/04 
ex0:
Hardware: Batman-201 ISK

V6: Point Cloud Spherical
	v6 structure: [(range,azimuth,elevation,doppler),......]
	
V7: Target Object List
	V7 structure: [(tid,posX,posY,velX,velY,accX,accY,posZ,velZ,accZ),....]
	
V8: Target Index
	V8 structure: [id1,id2....]
	
V9:Point Cloud Side Info
	v9 structure: [(snr,noise'),....]

(1)Download lib:
install:
~#sudo pip intall mmWave
update:
~#sudo pip install mmWave -U
'''

import serial
import numpy as np
from mmWave import lpdISK

#UART initial


port = serial.Serial("/dev/tty.usbmodemGY0043864",baudrate = 921600, timeout = 0.5)

radar = lpdISK.LpdISK(port)

 
prev_fn = 0
fn = 0 
def uartGetdata(name):
	global prev_fn,fn
	print("mmWave: {:} example:".format(name))
	port.flushInput()
	while True:
		
		(dck,v6,v7,v8,v9)=radar.tlvRead(False) 
		hdr = radar.getHeader()
		fn = hdr.frameNumber
		
		if fn != prev_fn:
			prev_fn = fn
			print(f"\n\n ==================  frameNumber:{fn} ==========================")
		#if dck:
			print("V6:V7:V8:V9 = length([{:d},{:d},{:d},{:d}])".format(len(v6),len(v7),len(v8),len(v9)))
			if len(v6) != 0:
				print("\nV6: Point Cloud Spherical v6:len({:d})-----------------".format(len(v6)))
				#[(range,azimuth,elevation,doppler),......]
				print(v6)
			if len(v7) != 0:
				print("\nV7: Target Object List----v7:len({:d})-----------------".format(len(v7)))
				#[(tid,posX,posY,velX,velY,accX,accY,posZ,velZ,accZ),....]
				print(v7)
			if len(v8) != 0:
				print("\nV8: Target Index----------v8:len({:d})-----------------".format(len(v8)))
				#[id1,id2....]
				print(v8)
			if len(v9) != 0:
				print("\nV9:Point Cloud Side Info--v9:len({:d})-----------------".format(len(v9)))
				#[(snr,noise'),....]
				print(v9)
			
uartGetdata("Long range People Detect (LPD) for BM-201")






