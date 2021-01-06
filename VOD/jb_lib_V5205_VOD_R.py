# Vehicle Occupant Detection
# for only
# ver:0.0.1
# 2020/02/10
# parsing Vehicle Occupant Detection 3D data 
# hardware:(Batman-201 ISK)VOD IWR6843
# company: Joybien Technologies: www.joybien.com
# author: Zach Chen
#===========================================
# output: V8,V9,V10 Raw data
# v0.0.1 : 2020/09/15 release

import serial
import time
import struct
#import numpy as np

class header:
	version = 0
	totalPackLen = 0
	platform = 0
	frameNumber = 0
	timeCpuCycles = 0
	numDetectedObj = 0
	numTLVs = 0
	subFrameIndex = 0
	
class vitalSign:
	unwrapped = 0.0
	heart = 0.0
	breathing  = 0.0
	heart_rate = 0.0
	breathing_rate = 0.0

class VehicleOD:
	magicWord =  [b'\x01',b'\x02',b'\x03',b'\x04',b'\x05',b'\x06',b'\x07',b'\x08',b'\0x99']
	port = ""
	hdr = header
	vs  = vitalSign
	dck = 0
	# add for VOD interal use
	tlvLength = 0
	
	# for debug use 
	dbg = False #Packet unpacket Check: True show message 
	sm = False #Observed StateMachine: True Show message
	check = False # Observe numTLV and v length
	
	def __init__(self,port):
		self.port = port
		print("(jb)Vehicle Occupant Detection")
		print("(jb)For Hardware:IWR6843")
		print("(jb)SW:0.0.1: HW:IWR-6843")
		print("(jb)Firmware: V5205_VOD")
		print("(jb)UART Baud Rate:921600")
		print("(jb)==================================")
		print("(jb)Output: V8,V9,V10 data:(RAW)")
		print("(jb)V8 :Range Azimuth Heatmap TLV")
		print("(jb)V9 :Feature Vector TLV")
		print("(jb)V10:Decision Vector TLV")
		
		
	def checkTLV(self,ft):
		self.check = ft
		
	def useDebug(self,ft):
		self.dbg = ft
		
	def stateMachine(self,ft):
		self.sm = ft
		
	def getVitalSign(self):
		return self.vs
	
	def getHeader(self):
		return self.hdr
		
	def headerShow(self):
		print("***header***********") 
		print("Version:     \t%x "%(self.hdr.version))
		print("Platform:    \t%X "%(self.hdr.platform))
		print("TotalPackLen:\t%d "%(self.hdr.totalPackLen))
		print("PID(frame#): \t%d "%(self.hdr.frameNumber))
		print("timeCpuCycles: \t%d "%(self.hdr.timeCpuCycles))
		print("numDetectedObj: \t%d "%(self.hdr.numDetectedObj))
		print("numTLVs: \t%d "%(self.hdr.numTLVs))
		print("subFrameIndex: \t%d "%(self.hdr.subFrameIndex))
		print("***End Of Header***") 
		
	def tlvTypeInfo(self,dtype,count,dShow):
		
		dataByte = 0
		lenCount = count
		pString = ""
		stateString = "V8"
		if dtype == 8:
			dataByte= 2    #HeatMap Value Int
			pString = "Range-Azimuth Heat Map"
			lenCount = count
			stateString = 'V8'
		elif dtype == 9:
			lenCount = count
			dataByte = 20  #target struct 20 bytes:(avgPower1,avgPower2,powerRatio1,powerRatio2,crossCorr)  
			pString = "Feature Vector TLV"
			stateString = "V9"
		elif dtype == 10:
			lenCount = count
			dataByte = 12 #zone = 1 byte
			pString = "Decision Vector TLV"
			stateString = "V10"
			
		else:
			pString = "*** Type Error ***"
			stateString = 'idle'

		if dShow == True:
			print("-----[{:}] ----".format(pString))
			print("tlv Type :  \t{:d}".format(dtype))
			print("tlv length:      \t{:d}".format(lenCount)) 
			#print("{:}      \t{:d}".format(nString,int(nPoint)))
			#print("value length:    \t{:d}".format(retCnt))  
		
		return stateString,dataByte,lenCount,pString
		
#
# TLV: Type-Length-Value
# read TLV data
# input:
#     disp: True:print message
#			False: hide printing message
# output:(return parameter)
# (pass_fail, v8, v9, v10)
#  pass_fail: True: Data available    False: Data not available
#
#	Output: V8,V9,V10 data:(RAW)")
#	V8 :Range Azimuth Heatmap TLV 
#	V9 :Feature Vector TLV 
#	V10:Decision Vector TLV 
#

	def tlvRead(self,disp):
		#print("---tlvRead---")
		#ds = dos
		typeList = [8,9,10]
		idx = 0
		lstate = 'idle'
		sbuf = b""
		lenCount = 0
		unitByteCount = 0
		dataBytes = 0
		
		tlvCount = 0
		pbyte = 16
		v8 = []
		v9 = ([])
		v10 = ([])
		
		zone = 0
	
		while True:
			try:
				ch = self.port.read()
			except:
				return (False,v8,v9,v10)
			#print(str(ch))
			if lstate == 'idle':
				#print(self.magicWord)
				if ch == self.magicWord[idx]:
					#print("*** magicWord:"+ "{:02x}".format(ord(ch)) + ":" + str(idx))
					idx += 1
					if idx == 8:
						#print(self.magicWord)
						idx = 0
						lstate = 'header'
						rangeProfile = b""
						sbuf = b""
				else:
					#print("not: magicWord state:")
					idx = 0
					rangeProfile = b""
					return (False,v8,v9,v10)
		
			elif lstate == 'header':
				sbuf += ch
				idx += 1
				if idx == 24: 
					#print("------header-----")
					#print(":".join("{:02x}".format(c) for c in sbuf)) 	 
					#print("len:{:d}".format(len(sbuf))) 
					# [header - Magicword]
					try: 
						#(self.hdr.version,self.hdr.totalPackLen,self.hdr.platform,
						#self.hdr.frameNumber,self.hdr.timeCpuCycles,self.hdr.numDetectedObj,
						#self.hdr.numTLVs,self.hdr.subFrameIndex) = struct.unpack('8I', sbuf)
						(self.hdr.totalPackLen,self.hdr.platform,
						self.hdr.frameNumber,self.hdr.timeCpuCycles,self.hdr.numDetectedObj,
						self.hdr.numTLVs) = struct.unpack('6I', sbuf)
						 
					except:
						if self.dbg == True:
							print("(Header)Improper TLV structure found: ")
						return (False,v8,v9,v10)
					
					if disp == True:  
						self.headerShow()
					
					tlvCount = self.hdr.numTLVs
					if self.hdr.numTLVs == 0:
						return (False,v8,v9,v10)
						
					if self.sm == True:
						print("(Header)")
						
					sbuf = b""
					idx = 0
					lstate = 'TL'
					dck = 0
					  
				elif idx > 40:
					idx = 0
					lstate = 'idle'
					return (False,v8,v9,v10)
					
			elif lstate == 'TL': #TLV Header type/length
				sbuf += ch
				idx += 1
				if idx == 8:
					#print(":".join("{:02x}".format(c) for c in sbuf))
					try:
						ttype,self.tlvLength = struct.unpack('2I', sbuf)
						if self.check:
							print("(check) numTLVs({:d}): tlvCount({:d})-------ttype:tlvLength:{:d}:{:d}".format(self.hdr.numTLVs,tlvCount,ttype,self.tlvLength))
						if ttype not in typeList or self.tlvLength > 10000:
							if self.dbg == True:
								print("(TL)Improper TL Length(hex):(T){:d} (L){:x} numTLVs:{:d}".format(ttype,self.tlvLength,self.hdr.numTLVs))
							sbuf = b""
							idx = 0
							lstate = 'idle'
							self.port.flushInput()
							return (False,v8,v9,v10)
							
					except:
						if self.dbg == True:
							print("TL unpack Improper Data Found:")
						self.port.flushInput()
						return (False,v8,v9,v10)
					
					lstate,dataBytes,lenCount,pString = self.tlvTypeInfo(ttype,self.tlvLength,disp)
					if lstate == 'V10':
						self.zone = self.tlvLength
					 
					if self.sm == True:
						print("(TL:{:d})=>({:})".format(tlvCount,lstate))
						
					tlvCount -= 1
					idx = 0  
					sbuf = b""
			
					
			elif lstate == 'V8': # count = Total Lentgh - 8
				sbuf += ch
				idx += 1
				if (idx%dataBytes == 0):
					try:
						#print(":".join("{:02x}".format(c) for c in sbuf))
						v8s = struct.unpack('h', sbuf)						
						v8.append(v8s[0])
						sbuf = b""
					except:
						if self.dbg == True:
							print("(6.1)Improper Type V8 structure found: ")
						return (False,v8,v9,v10)
					
				if idx == lenCount:
					if disp == True:
						print("v8[{:d}]".format(len(v8)))
					idx = 0
					sbuf = b""
					if tlvCount <= 0: # Back to idle
						lstate = 'idle'
						dck += 1
						if self.sm == True:
							print("(V8:{:d})=>(idle) :true".format(tlvCount))
						return (True,v8,v9,v10)
						
					else: # Go to TL to get others type value
						lstate = 'TL' 
						dck += 1
						idx = 0
						sbuf = b""
						#print("---------v8 ok ---------{:d}".format(len(v8)))
						if self.sm == True:
							print("(V8:{:d})=>(TL)".format(tlvCount))
					
				elif idx > 7000: #lenCount:
					print("V8 data over:10")
					idx = 0
					sbuf = b""
					lstate = 'idle'
					return (False,v8,v9,v10)
					
			elif lstate == 'V9':
				idx += 1
				sbuf += ch
				if  (idx%dataBytes == 0):
					#print("*************v9******:{:}   tlvCount={:}".format(lenCount,tlvCount))
					#(avgPower1,avgPower2,powerRatio1,powerRatio1,crossCorr) = struct.unpack('5f',sbuf)
					#v9.append((avgPower1,avgPower2,powerRatio1,powerRatio1,crossCorr)) # =  struct.unpack('5f',sbuf)
					#(avgPower1,avgPower2,powerRatio1,powerRatio1,crossCorr) = struct.unpack('5f',sbuf)
					v9.append(struct.unpack('5f',sbuf)) 
					
					
					sbuf = b""
					if disp == True:
						print("v9[{:d}]".format(len(v9))) 
							
				if idx == lenCount:
					if disp == True:
						print("v9[{:d}]".format(len(v9)))
					idx = 0
					sbuf = b""
					if tlvCount <= 0: # Back to idle
						lstate = 'idle'
						if self.sm == True:
							print("(V9:{:d})=>(idle) :true".format(tlvCount))
						return (True,v8,v9,v10)
						
					else: # Go to TL to get others type value
						lstate = 'TL' 
						if self.sm == True:
							print("(V9:{:d})=>(TL)".format(tlvCount))
						
				if idx > lenCount :
					print("V9 data over:80")
					idx = 0 
					lstate = 'idle'
					sbuf = b""
					if self.sm == True:
						print("(V9)=>(idle)")
					return (False,v8,v9,v10)
				
			elif lstate == 'V10':
				idx += 1
				sbuf += ch
				#print(idx) 
				if  (idx%dataBytes == 0):
					#print("V10:dataBytes({:d}) lenCount({:d}) index:{:d}".format(dataBytes,lenCount,idx))
					(percent,power,rangeIdx,azimuthIdx) =  struct.unpack('2f2h',sbuf)
					v10.append((percent,power,rangeIdx,azimuthIdx))
					
					if disp == True:
						print("v10[{:d}]".format(len(v10))) 
					sbuf = b""
							
				if idx == lenCount:
					if disp == True:
						print("v10[{:d}]".format(len(v10)))
					idx = 0
					sbuf = b""
					if tlvCount <= 0: # Back to idle
						lstate = 'idle'
						if self.sm == True:
							print("(V10:{:d})=>(idle) :true".format(tlvCount))
						return (True,v8,v9,v10)
						
					else: # Go to TL to get others type value
						lstate = 'TL' 
						if self.sm == True:
							print("(V10:{:d})=>(TL)".format(tlvCount))
						
				if idx > lenCount :
					print("V10 data over:96")
					idx = 0 
					lstate = 'idle'
					sbuf = b""
					if self.sm == True:
						print("(V10)=>(idle)")
					return (False,v8,v9,v10)




