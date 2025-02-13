#=============================================
# File Name: pc3_ex3_xyz_playback.py
#
# Requirement:
# Hardware: BM201-ISK or BM501-AOP
#  
# lib: pc3
# plot tools: pyqtgraph
# Plot point cloud(V6) in 2D/3D figure 
# type: Raw data
#  
#	Baud Rate: 115200 for playback
# 
''' 3D plot tools version 
PyOpenGL                     3.1.5
PyQt5                        5.14.1
PyQt5-Qt5                    5.15.2
PyQt5-sip                    12.9.0
PyQt6                        6.5.0
PyQt6-Qt6                    6.5.0
PyQt6-sip                    13.5.1
pyqtgraph                    0.13.3
'''
#=============================================
#import pyqtgraph as pg
#import pyqtgraph.opengl as gl
from pyqtgraph.Qt import QtGui, QtCore, QtWidgets
import numpy as np
import sys
import serial
import threading

# lib file 
from mmWave import pc3_v2 # mmWave lib
from jb_tools import Plot2D, Plot3D
#

class RadarReader:
	def __init__(self, port, baud_rate=115200,zOffset = None):
		"""Initialize radar connection."""
		self.zOffset = 0.0 if zOffset == None else zOffset
		self.port = serial.Serial(port, baudrate=baud_rate, timeout=0.5)
		
		self.radar = pc3_v2.Pc3_v2(self.port)

		self.data_2d = np.empty((0, 2))  # Placeholder for 2D data
		self.data_3d = np.empty((0, 3))  # Placeholder for 3D data

		self.running = True  # Control flag for the reading loop
		self.data_ready = threading.Event()  # Event to signal new data
		
		self.thread = threading.Thread(target=self.read_radar_data, daemon=True)
		self.thread.start()
		self.fn = 0
		self.fn_prev = 0
		(v6smu,v7smu,v8smu) = self.radar.readFile("pc3_2025-02-12-16-03-27.csv")

	def read_radar_data(self):
		"""Continuously reads data from the radar in a separate thread without sleep."""
		while self.running:
			dck, v6, v7, v8 = self.radar.tlvRead(False)
			#hdr = radar.getHeader()
			self.fn = self.radar.frameNumber
			print("JB> fn:{:}    start:{:}   stop:{:}".format(self.fn,self.radar.sim_startFN,self.radar.sim_stopFN))
			hdr = self.radar.getHeader()
			fn = hdr.frameNumber
			(dck,v6,v7,v8) = self.radar.getRecordData(fn)
			
			if self.fn != self.fn_prev :
				print(f'fn = {self.fn}  v6: {v6}')
				v6op = v6    #v6Temp[(v6Temp.sx > -0.5) & (v6Temp.sx < 0.5) & (v6Temp.sy < 1.0) & (v6Temp.doppler != 0) ]
				d3 = v6op.loc[:,['sx','sy','sz']] .copy()
				d3['sz'] += self.zOffset
				d2 = v6op.loc[:,['sx','sy']] 
				#dd = v6op.loc[:,['sx','sy','sz','doppler']] 
				print(f'fn = {self.fn}  \n{d2} \n{d3}')
				
				
				# Data for plot 
				if not v6.empty:
					self.data_2d = d2.to_numpy()
					self.data_3d = d3.to_numpy() 
				else:
					self.data_2d = np.empty((0, 2))
					self.data_3d = np.empty((0, 3))
					
				self.fn_prev = self.fn
				
			self.port.flushInput()  # Clear input buffer
			self.data_ready.set()  # Signal that new data is available
			

	def get_data(self):
		"""Return the latest radar data."""
		self.data_ready.wait()  # Wait until new data is available
		self.data_ready.clear()  # Reset event flag
		return self.data_2d, self.data_3d

	def stop(self):
		"""Stop the radar reading thread."""
		self.running = False
		self.thread.join()


JB_RADAR_INSTALL_HEIGHT = 1.0
UART_PORT = '/dev/ttyACM1'

if __name__ == '__main__':
	app = QtWidgets.QApplication(sys.argv)
	
	# initialize the 2D and 3D plot
	plot2d = Plot2D()
	plot3d = Plot3D(zOffset = JB_RADAR_INSTALL_HEIGHT)
	
	# Initialize radar reader
	radar = RadarReader(UART_PORT, baud_rate=115200, zOffset =  JB_RADAR_INSTALL_HEIGHT)

	def update():
		"""Fetch latest radar data and update the plots."""
		data_2d, data_3d = radar.get_data()
		plot2d.update_plot(data_2d)
		plot3d.update_plot(data_3d)

	timer = QtCore.QTimer()
	timer.timeout.connect(update)
	timer.start(100)  # Update every 100ms

	try:
		sys.exit(app.exec())
	except KeyboardInterrupt:
		print("Stopping radar...")
		radar_reader.stop()

