# 3D People Counting-ISK/AOP 3D Raw Data for 360°(pc3_360)
# ver:0.0.1
# 2020/06/19
# 
# parsing People Counting 3D fusion for 360° data
# hardware:(Batman-201)ISK IWR6843 ES2.0 / AOP(BM-501/BM601)
# company: Joybien Technologies: www.joybien.com
# author: Zach Chen
#===========================================
# output: V6,V7,V8 Raw data
# v1.0.1 : 2022/16/08 release
#          (1)Output list data
#          (2)Output dataframe data
#
# v1.0.2 : 2025/02/11 add zOffset
#          
#  
import serial
import time
import struct
import pandas as pd
import numpy as np

# new
#######################################################
import time
JB_tOld = time.time()
import pandas as pd
pd.options.display.float_format = "{:,.1f}".format
pd.set_option('display.width', 300)
pd.set_option('display.max_columns', 60)
pd.set_option('display.max_rows', 5) # 5 # can see two upper lines and two lower lines and dot line in the middle
def jb(title='.', value=0):
	if 1: # tmp comment out 	
		print('\nJB_({})>'.format(title), end="")
		#print('\nJB_({})>'.format(title)) # ALERT: tmp comment out. due to 'end' 
		if isinstance(value, list):
			print('type= list, len= {}'.format(len(value)))
			print('{}'.format(value))
		elif isinstance(value, tuple):
			print('type = tuple, len= {}'.format(len(value)))
			print('{}'.format(value))
		elif isinstance(value, type(np.array([]))):
			print('type= ndarray, shape= {}'.format(value.shape))
			#print('type= array, len= {}'.format(len(value)))
			print('{}'.format(value))
		elif isinstance(value, type(pd.DataFrame(pd.DataFrame([1.0,2.0])))):
			print('type= dataframe, shape= {}'.format(value.shape))
			print('{}'.format(value))
		elif isinstance(value, type(pd.Series([1.0, 2]))):
			print('type= series, shape= {}'.format(value.shape))
			print('{}'.format(value))
		else:
			print('type={}'.format(type(value)))
			print('JB> value= {}'.format(value))
		print('-----------------------------------------------------------------\n')
####################################################################


class header:
	version = 0
	totalPackLen = 0
	platform = 0
	frameNumber = 0
	subframeNumber = 0
	chirpMargin = 0
	frameMargin = 0 
	trackProcessTime = 0
	uartSendTime = 0
	numTLVs = 0
	checksum = 0

class unitS:
	elevationUnit:float = 0.0
	azimuthUnit : float = 0.0
	dopplerUnit :float = 0.0
	rangeUnit :float = 0.0
	snrUnit :float = 0.0

class Pc3_360:
	gdata = b''
	playback = False
	magicWord =  [b'\x02',b'\x01',b'\x04',b'\x03',b'\x06',b'\x05',b'\x08',b'\x07',b'\0x99']
	port = ""
	hdr = header
	u = unitS
	frameNumber = 0
	# provide csv file dataframe
	# real-time 
    #v6_col_names_rt = ['time','fN','type','elv','azimuth','range' ,'doppler','snr','sx', 'sy', 'sz'] # original
	v6_col_names_rt = ['fN','type','elv','azimuth','doppler','range' ,'snr',  'sx', 'sy', 'sz' ]  #v0.1.4
	v7_col_names_rt = ['fN','type','posX','posY','posZ','velX','velY','velZ','accX','accY','accZ','ec0','ec1','ec2','ec3','ec4','ec5','ec6','ec7','ec8','ec9','ec10','ec11','ec12','ec13','ec14','ec15','g','confi','tid']
	                     
	v8_col_names_rt = ['fN','type','targetID']
	zOffset = 0.0 
	
	# read from file for trace point clouds
	fileName = ''
	v6_col_names = ['time','fN','degree','type','elv','azimuth','doppler','range','snr','sx', 'sy', 'sz']
	v7_col_names = ['time','fN','degree','type','tid','posX','posY','posZ','velX','velY','velZ','accX','accY','accZ','ec0','ec1','ec2','ec3','ec4','ec5','ec6','ec7','ec8','ec9','ec10','ec11','ec12','ec13','ec14','ec15','g','confi'] #v0.1.2
	v8_col_names = ['time','fN','degree','type','targetID']
	
	v6simo = []
	v7simo = []
	v8simo = []
	
	sim_startFN = 0
	sim_stopFN  = 0 
	JB_t0 = 0
	version_keep = '3050004'
	
	# add for interal use
	tlvLength = 0
	numOfPoints = 0
	# for debug use 
	dbg = False #Packet unpacket Check: True show message 
	sm = False #Observed StateMachine: True Show message
	plen = 16 
	
	def __init__(self,port, azi_degree = None, bufSize = None, zOffset = None):
		
		port.reset_input_buffer()
		port.ReadBufferSize = bufSize
		self.degree = azi_degree
		self.port = port
		self.zOffset = 0.0 if zOffset == None else zOffset
		self.azi_offset = 0.0 if azi_degree == None else azi_degree * np.pi/180.0
		print("(jb)People Counting 3D initial")
		print("(jb)vsersion:v0.1.0")
		print("(jb)For Hardware:Batman-201(ISK)/AOP(501/601)")
		print("(jb)Firmware: PC3")
		print("(jb)UART Baud Rate:921600")
		print("Output: V6,V7,V8 data:(RAW)\n##########################################\n\n\n")
		
	def useDebug(self,ft):
		self.dbg = ft
		
	def stateMachine(self,ft):
		self.sm = ft
		
	def getHeader(self):
		return self.hdr
		
	def headerShow(self):
		print("***header***********") 
		print("Version:     \t%x "%(self.hdr.version))
		print("Platform:    \t%X "%(self.hdr.platform))
		print("TotalPackLen:\t%d "%(self.hdr.totalPackLen))
		print("PID(frame#): \t%d "%(self.hdr.frameNumber))
		print("subframe#  : \t%d "%(self.hdr.subframeNumber))
		print("Inter-frame Processing Time:\t{:d} us".format(self.hdr.trackProcessTime))
		print("UART Send Time:\t{:d} us".format(self.hdr.uartSendTime))
		print("Inter-chirp Processing Margin:\t{:d} us".format(self.hdr.chirpMargin))
		print("Inter-frame Processing Margin:\t{:d} us".format(self.hdr.frameMargin))
		print("numTLVs:     \t%d "%(self.hdr.numTLVs))
		print("Check Sum   :\t{:x}".format(self.hdr.checksum))
		print("***End Of Header***") 
			
	
		
	def list2df(self,dck,l6,l7,l8):
		ll6 = pd.DataFrame(l6,columns=self.v6_col_names_rt)
		ll7 = pd.DataFrame(l7,columns=self.v7_col_names_rt)
		ll8 = pd.DataFrame(l8,columns=self.v8_col_names_rt)
		return (dck,ll6,ll7,ll8)

#
# TLV: Type-Length-Value
# read TLV data
# input:
#     disp: True:print message
#			False: hide printing message
#     df: 
# output:(return parameter)
# (pass_fail, v6, v7, v8)
#  pass_fail: True: Data available    False: Data not available
#  v6: point cloud infomation
#  v7: Target Object information
#  v8: Target Index information
#  
# 
#

	#################################################################
	JB_syncFlag = 0
	def jb_getUartBuf(self):
		idx = 0
		buf = b""
		self.gdata = b''
		while True:
			if self.JB_syncFlag == 0:
				ch = self.port.read() # here ch type is byte
				if ch == self.magicWord[idx]: # 0..7
					buf += ch
					idx += 1 # 1..8
					if idx == 8:
						idx = 8
						self.JB_syncFlag = 1
						self.JB_t0 = time.time()
						
			else:
				self.JB_syncFlag = 0 # magic word ch mismatch loop back again
				idx = 0 # init
				buf = b""
				self.gdata = b''
			

			if self.JB_syncFlag == 1:
				# read next 16 bytes for v, l, p, f
				for i in range(16):
					ch = self.port.read()
					
					buf += ch
					self.gdata = buf
					
				if len(buf) == (8 + 16): # version + totalLen
					magic=struct.unpack('8B', buf[0:8])
					version = struct.unpack('I', buf[8:12])[0]   # get tuple [0]
					verString = "{:X}".format(version)
					totalLen = struct.unpack('I', buf[12:16])[0] # get tuple [0]
					fn = struct.unpack('I', buf[20:24])[0]
					
					self.frameNumber = fn
					if self.playback == True:
						return False
					
					if verString != self.version_keep or totalLen > 100000:
						print("ver: {:}   version_keep:{:}".format(verString,self.version_keep ))
						return False
					
					
				else:
					self.JB_syncFlag = 0 # len mismatch loop back again
					idx = 0
					buf = b''
					self.gdata = b''

			if self.JB_syncFlag == 1:
				r = self.port.read(totalLen - 24) # read rest of bytes
				#xx = self.port.inWaiting()
				#print("is Wating= {:}  :len:{:}".format(0,len(r)))
				#buf += r
				self.gdata += r
				dt = time.time()- self.JB_t0
				#self.port.flushInput()
				self.port.reset_input_buffer()
				#print('JB_getUartBuf> fn={}, magic={}, version={:X}, totalLen={}, bufLen={}, dt={:.0f} ms'.format(fn, magic, version, totalLen, len(buf), dt * 1000))
				if totalLen == len(self.gdata):
					return True
				else:
					self.JB_syncFlag = 0 # len mismatch loop back again
					idx = 0
					buf = b""
					self.gdata = b''
					

#################################################################
#
# TLV: Type-Length-Value
# read TLV data
# input:
#     disp: True:print message
#			False: hide printing message
#     df: 
# output:(return parameter)
# (pass_fail, v6, v7, v8)
#  pass_fail: True: Data available    False: Data not available
#  v6: point cloud infomation
#  v7: Target Object information
#  v8: Target Index information
#  
#================================================================
	JB_i = 0
	def tlvRead(self,disp,df = None):
		global JB_tOld, JB_i
		 
		#print("---tlvRead---")
		#ds = dos
		typeList = [6,7,8]
		idx = 0
		lstate = 'idle'
		sbuf = b''
		lenCount = 0
		unitByteCount = 0
		dataBytes = 0
		numOfPoints = 0
		tlvCount = 0
		pbyte = 16
		v6 = ([])
		v7 = ([])
		v8 = ([])
		v6df = ([])
		v7df = ([])
		v8df = ([])
		ch = b'\x00' # init
		idxTo = 0
		uartBuf = b''
		while True:
			###############################
			# on {idle} getUartBuf() else parsing from uartBuf[]
			if lstate == 'idle':
				chk = self.jb_getUartBuf()
				if chk == True:
					uartBuf = self.gdata
				else:
					#print("===========================tlvRead=========================buf empty" )
					return self.list2df(False,v6df,v7df,v8df) if (df == 'DataFrame') else (False,v6,v7,v8)
		
				self.JB_i = 8 # init, read start from 8, after magic word		 
				lstate = 'header'
				sbuf = b"" # init
				idxFrom = 0
				idxTo = 8
			else:
				dumy = 0
				
				# read ch from uartBuf[]
				#ch1 = uartBuf[self.JB_i] # read start after magic word (8 bytes)
				#self.JB_i += 1 		
				# MUST int -> bytes			
				#ch = bytes(ch1) # ALERT: failed
				#ch = ch1.to_bytes(1, 'little')
			################################

			if lstate == 'header': # 40B := index 8:48
				idxFrom = idxTo
				idxTo += 40
				#print("JB> header : idxTo:{:}".format(idxTo))
				try: 
					(self.hdr.version,self.hdr.totalPackLen,self.hdr.platform,
					self.hdr.frameNumber,self.hdr.subframeNumber,
					self.hdr.chirpMargin,self.hdr.frameMargin,self.hdr.trackProcessTime,self.hdr.uartSendTime,self.hdr.numTLVs,self.hdr.checksum
					) = struct.unpack('9I2H', uartBuf[idxFrom : idxTo]) 
					self.frameNumber = self.hdr.frameNumber
					
					#self.headerShow()
					#print('JB> fn={}, len={}, platform={}, tlv={}'.format(self.frameNumber, self.hdr.totalPackLen, self.hdr.platform, self.hdr.numTLVs))
					if self.playback == True:
						lstate = 'idle'
					else:
						lstate = 'TL'
				except:
					if self.dbg == True:
						print("(Header)Improper TLV structure found: ")
					return self.list2df(False,v6df,v7df,v8df) if (df == 'DataFrame') else (False,v6,v7,v8)
				
				tlvCount = self.hdr.numTLVs
					
			elif lstate == 'TL': #TLV Header type/length
				idxFrom = idxTo
				idxTo += 8
				
				#print("JB> (TL) indexFrom = {:}   idxTo = {:}".format(idxFrom,idxTo))
				#print("JB> (TL) {:}".format(uartBuf[idxFrom : idxTo]))
				ttype, self.tlvLength = struct.unpack('2I', uartBuf[idxFrom : idxTo])
				
				if ttype == 6 or ttype == 7:
					#print('JB> (TL) type=V{}, len={}'.format(ttype, self.tlvLength))
					if ttype  == 6: #'V6'
						lstate = 'V6-unit' #'V6'
						if self.sm == True:
							print("JB>..(TL:len={:d})=>({:})".format(self.tlvLength,lstate))
							
					if ttype == 7:
						return self.list2df(False,v6df,v7df,v8df) if (df == 'DataFrame') else (False,v6,v7,v8)
						lstate = 'idle'
						#lstate = 'V7'
						if self.sm == True:
							print("JB>..(TL:len={:d})=>({:})".format(self.tlvLength,lstate))
				else:
					print("(TL) -v6/v7 failed  type: {:}".format(ttype))
					return self.list2df(False,v6df,v7df,v8df) if (df == 'DataFrame') else (False,v6,v7,v8)
			
			elif lstate == 'V6-unit':
				idxFrom = idxTo
				idxTo +=  (5 * 4)    #(self.tlvLength - 8) # uints := 5 x u32
				#print(len(uartBuf[idxFrom  : idxTo]))
				try: 
					self.u.elevationUnit,self.u.azimuthUnit,self.u.dopplerUnit,self.u.rangeUnit,self.u.snrUnit = struct.unpack('5f', uartBuf[idxFrom : idxTo])
					#print("JB> (V6-unit)  ==> elv:{:.4f} azimuth:{:.4f} doppler:{:.4f} range:{:.4f} snr:{:.4f}".format(self.u.elevationUnit,self.u.azimuthUnit,self.u.dopplerUnit,self.u.rangeUnit,self.u.snrUnit))
				except:
					if self.dbg == True:
						print("(V6-unit)Improper Type/Value structure found: ")
					return self.list2df(False,v6df,v7df,v8df) if (df == 'DataFrame') else (False,v6,v7,v8)
					
				lstate = 'V6'
				if self.sm == True:
					print("JB>..(V6-Unit)=>(V6)")
					
			elif lstate == 'V6': # count = Total Lentgh - 8   # eadrs: 8 bytes
				dataBytes = 8
				datalen = self.tlvLength - 8 - 20
				points = int(datalen/dataBytes)
				#print("JB> (V6) points: {:}    datalen:{:}  idxTo:{:}".format(points,datalen,idxTo))
				idxFrom = idxTo
				idxTo += datalen 
				#print("JB> (V6) idxFrom:{:} idxTo= {:}  diff:{:} + 28 = {:}    self.tlvLength= {:}".format(idxFrom,idxTo,idxTo-idxFrom,idxTo-idxFrom + 28,self.tlvLength))
				
				#sbuf = uartBuf[idxFrom : idxTo]
				for i in range(points):
					try: 
						(e,a,d,r,s) = struct.unpack('2bh2H', uartBuf[idxFrom + i*dataBytes : idxFrom + (i + 1)*dataBytes]) #8bytes
						elv = e * self.u.elevationUnit
						azi = a * self.u.azimuthUnit  + self.azi_offset
						dop = d * self.u.dopplerUnit
						ran = r * self.u.rangeUnit
						snr = s * self.u.snrUnit
						sz  = ran * np.sin(elv)  + self.zOffset
						sx  = ran * np.cos(elv) * np.sin(azi) 
						sy  = ran * np.cos(elv) * np.cos(azi) 
						
						#print("({:}:{:4d})(idx:({:4d}) elv:{:.4f} azimuth:{:.4f} doppler:{:.4f} range:{:.4f} snr:{:.4f}".format(points,lenCount,idx,elv,azi,dop,ran,snr))
						if (df == 'DataFrame'):
							v6df.append((self.hdr.frameNumber,'v6',elv,azi,dop,ran,snr,sx,sy,sz))
							#jb('tlvRead()_v6df', v6df)
						else:
							v6.append((elv,azi,dop,ran,snr,sx,sy,sz))
					except:
						if self.dbg == True:
							print("(7)Improper Type 6 Value structure found: ")
						return self.list2df(False,v6df,v7df,v8df) if (df == 'DataFrame') else (False,v6,v7,v8)
				
				tlvCount -= 1
				if tlvCount == 0:
					lstate = 'idle'
					if self.sm == True:
						print("JB>..(V6)->(idle)   tlvCount:{:}".format(tlvCount))
					return self.list2df(True,v6df,v7df,v8df) if (df == 'DataFrame') else (True,v6,v7,v8)
				else:
					lstate = 'TL'
					if self.sm == True:
						print("JB>..(V6)->(TL)  tlvCount:{:}".format(tlvCount))
						
			elif lstate == 'V7': # count = Total Lentgh - 8
				dataBytes = 112 # 4 + 9 * 4 + 18 *4 = 112
				datalen = self.tlvLength - 8
				points = int(datalen / dataBytes)
				idxFrom = idxTo
				idxTo += datalen
				#print("JB> (V7) points: {:}    datalen:{:}  idxTo:{:}".format(points,datalen,idxTo))
				#print("JB> (V7) idxFrom: {:}  idxTo:{:}".format(idxFrom,idxTo))
				
				for i in range(points):
					try:
						(tid,pX,pY,posZ,velX,velY,velZ,accX,accY,accZ,ec0,ec1,ec2,
						ec3,ec4,ec5,ec6,ec7,ec8,ec9,ec10,ec11,ec12,ec13,ec14,ec15,g,confi) = struct.unpack('I9f18f', uartBuf[idxFrom + i*dataBytes : idxFrom + (i + 1)*dataBytes])
						posX, posY = rotate_matrix(pX, pY, self.azi_offset  , x_shift=0, y_shift=0, units="RADIAN")  
						
						if (df == 'DataFrame'):
							v7df.append((self.hdr.frameNumber,'v7',posX,posY,posZ,velX,velY,velZ,accX,accY,accZ,ec0,ec1,ec2,
							ec3,ec4,ec5,ec6,ec7,ec8,ec9,ec10,ec11,ec12,ec13,ec14,ec15,g,confi,tid)) 
						else: 
							v7.append((tid,posX,posY,posZ,velX,velY,velZ,accX,accY,accZ,ec0,ec1,ec2,ec3,ec4,ec5,ec6,ec7,ec8,ec9,ec10,ec11,ec12,ec13,ec14,ec15,g,confi))
							
					except:
						if self.dbg == True:
							print("(7)Improper Type 7 Value structure found: ")
						return self.list2df(False,v6df,v7df,v8df) if (df == 'DataFrame') else (False,v6,v7,v8)
				
				tlvCount -= 1
				if tlvCount == 0:
					lstate = 'idle'
					if self.sm == True:
						print("JB> (V7)->(idle)   tlvCount:{:}".format(tlvCount))
					return self.list2df(True,v6df,v7df,v8df) if (df == 'DataFrame') else (True,v6,v7,v8)
				else:
					lstate = 'TL'
					if self.sm == True:
						print("JB> (V7)->(TL)  tlvCount:{:}".format(tlvCount))
						
			elif lstate == 'V8':
				idx += 1
				v8.append(ord(ch))
				
				if idx == lenCount:
					if disp == True:
						print("=====V8 End====")
					sbuf = b""
					idx = 0
					lstate = 'idle'
					if self.sm == True:
						print("(V8:{:d})=>(idle)".format(tlvCount))
						
					if (df == 'DataFrame'):
						v8o = [self.hdr.frameNumber,'v8']
						v8df = v8o.extend(v8)
					return self.list2df(True,v6df,v7df,v8df) if (df == 'DataFrame') else (True,v6,v7,v8)
				
				if idx > lenCount:
					sbuf = b""
					idx = 0
					lstate = 'idle'
					return self.list2df(False,v6df,v7df,v8df) if (df == 'DataFrame') else (False,v6,v7,v8)

	def rotate_matrix(x, y, angle, x_shift=0, y_shift=0, units="DEGREES"):
		# Shift to origin (0,0)
		x = x - x_shift
		y = y - y_shift
		
		# Convert degrees to radians
		if units == "DEGREES":
			angle = np.radians(angle)

		# Rotation matrix multiplication to get rotated x & y
		xr = (x * np.cos(angle)) - (y * np.sin(angle)) + x_shift
		yr = (x * np.sin(angle)) + (y * np.cos(angle)) + y_shift
		return xr, yr


					

	def v67Simlog(frameNum):
		global sim_startFN,sim_stopFN
		s_fn = frameNum + sim_startFN
		#print("frame number:{:}".format(s_fn))
		v6d = v6sim[v6sim['fN'] == s_fn]
		#v6d =  v6dd[v6dd['doppler'] < 0.0]
		#print(v6d)
		v7d = v7sim[v7sim['fN'] == s_fn]
		chk = 0
		if v6d.count != 0:
			chk = 1
		return (chk,v6d,v7d)
		
	def getRecordData(self,frameNum):
		s_fn = frameNum + self.sim_startFN
		#print("frame number:{:}".format(s_fn))
		v6d = self.v6simo[self.v6simo['fN'] == s_fn]
		#v6d =  v6dd[v6dd['doppler'] < 0.0]
		#print(v6d)
		v7d = self.v7simo[self.v7simo['fN'] == s_fn]
		v8d = self.v8simo[self.v8simo['fN'] == s_fn]
		chk = 0
		if v6d.count != 0:
			chk = 1
		return (chk,v6d,v7d,v8d)
		
	
		
	def readFile(self,fileName):
		#fileName = "pc32021-03-19-10-02-17.csv"  
		#df = pd.read_csv(fileName, error_bad_lines=False, warn_bad_lines=False) 
		self.fileName = fileName 
		#          ['time','fN','type','elv','azimuth','range' ,'doppler','snr','sx', 'sy', 'sz']
		df = pd.read_csv(self.fileName, names = self.v6_col_names, skiprows = [0,11,12]) 
		df.dropna()
		#print("------------------- df --------------------shape:{:}".format(df.shape))
		print(df.info())
		print(df.info(memory_usage="deep")) 
		
		v6simOri = df[(df.type == 'v6')]
		#print("-------------------v6sim------------:{:}".format(v6simOri.shape))
		
		self.v6simo = v6simOri.loc[:,['fN','type','elv','azimuth','doppler','range' ,'snr','sx', 'sy', 'sz']] # in this case
		self.v6simo['elv'] = self.v6simo['elv'].astype(float, errors = 'raise') 
		
		df7 = pd.read_csv(self.fileName, names = self.v7_col_names, skiprows = [0])  
		
		#------------- v7 sim ---------------
		v7simc = df7[df7['type'] == 'v7']
		self.v7simo  = v7simc.loc[:,['fN','type','posX','posY','posZ','velX','velY','velZ','accX','accY','accZ','tid']]
		self.v7simo['posX'] = self.v7simo['posX'].astype(float, errors = 'raise') 
		self.sim_startFN = df['fN'].values[0]
		self.sim_stopFN  = df['fN'].values[-1]
		
		#------------- v8 sim ---------------
		v8simc = df[df['type'] == 'v8']
		self.v8simo  = v8simc.loc[:,['fN','type','elv']]
		self.v8simo.columns = ['fN','type','targetID']
		
		#print(self.v8simo)
		return (self.v6simo,self.v7simo,self.v8simo)
		




