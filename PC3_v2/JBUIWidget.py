#=============================================
# File Name: JBUIWidget.py
#
# usuage please reference: POS_pc3OVH_pyqtgraph_v7_gate_class_json.py 
#
# Requirement:
# Hardware: BM201-ISK or BM501-AOP
# Firmware: PC3-I471
#
#
# JBWidget.py is a liberay file 
#
#=============================================


import numpy as np
import math
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import pandas as pd
from sklearn.cluster import DBSCAN
from sklearn.preprocessing import StandardScaler
import time
from datetime import date,datetime,time

import tkinter as tk

################### Class #######################################
class CustomTextItem(gl.GLGraphicsItem.GLGraphicsItem):
	def __init__(self, X, Y, Z, text):
		gl.GLGraphicsItem.GLGraphicsItem.__init__(self)
		self.text = text
		self.X = X
		self.Y = Y
		self.Z = Z

	def setGLViewWidget(self, GLViewWidget):
		self.GLViewWidget = GLViewWidget

	def setText(self, text):
		self.text = text
		self.update()

	def setX(self, X):
		self.X = X
		self.update()

	def setY(self, Y):
		self.Y = Y
		self.update()

	def setZ(self, Z):
		self.Z = Z
		self.update()

	def paint(self):
		a = 0
		#self.GLViewWidget.qglColor(QtCore.Qt.cyan)
		#self.GLViewWidget.renderText(round(self.X), round(self.Y), round(self.Z), self.text)

class Custom3DAxis(gl.GLAxisItem):
	#Class defined to extend 'gl.GLAxisItem'
	def __init__(self, parent, color=(0,0,0,.6)):
		gl.GLAxisItem.__init__(self)
		self.parent = parent
		self.c = color
		
	def add_labels(self):
		#Adds axes labels. 
		x,y,z = self.size()
		#X label
		self.xLabel = CustomTextItem(X=x/2, Y=-y/20, Z=-z/20, text="X")
		self.xLabel.setGLViewWidget(self.parent)
		self.parent.addItem(self.xLabel)
		#Y label
		self.yLabel = CustomTextItem(X=-x/20, Y=y/2, Z=-z/20, text="Y")
		self.yLabel.setGLViewWidget(self.parent)
		self.parent.addItem(self.yLabel)
		#Z label
		self.zLabel = CustomTextItem(X=-x/20, Y=-y/20, Z=z/2, text="Z")
		self.zLabel.setGLViewWidget(self.parent)
		self.parent.addItem(self.zLabel)
		
	def add_tick_values(self, xticks=[], yticks=[], zticks=[]):
		#Adds ticks values. 
		x,y,z = self.size()
		xtpos = np.linspace(0, x, len(xticks))
		ytpos = np.linspace(0, y, len(yticks))
		ztpos = np.linspace(0, z, len(zticks))
		#X label
		for i, xt in enumerate(xticks):
			val = CustomTextItem(X=xtpos[i], Y=0, Z=0, text='{}'.format(xt))
			val.setGLViewWidget(self.parent)
			self.parent.addItem(val)
		#Y label
		for i, yt in enumerate(yticks):
			val = CustomTextItem(X=0, Y=ytpos[i], Z=0, text='{}'.format(yt))
			val.setGLViewWidget(self.parent)
			self.parent.addItem(val)
		#Z label
		for i, zt in enumerate(zticks):
			val = CustomTextItem(X=0, Y=0, Z=ztpos[i], text='{}'.format(zt))
			val.setGLViewWidget(self.parent)
			self.parent.addItem(val)



class radar_utility:
	def __init__(self,x= 0.0625  ,y= 0.05 ,z= 0.125 , offset= 1.0):
		self.verX = x
		self.verY = y
		self.verZ = z
		self.zOffSet = offset
		
	def obj(self):
		self.verts = np.empty((2,3,3))
		self.verts[0,0,:] = [-self.verX, 0, self.verZ + self.zOffSet]
		self.verts[0,1,:] = [-self.verX, 0,-self.verZ + self.zOffSet]
		self.verts[0,2,:] = [self.verX,  0,-self.verZ + self.zOffSet]
		self.verts[1,0,:] = [-self.verX, 0, self.verZ + self.zOffSet]
		self.verts[1,1,:] = [self.verX,  0, self.verZ + self.zOffSet]
		self.verts[1,2,:] = [self.verX,  0, -self.verZ + self.zOffSet]
		return(self.verts)
		
	def getFileName(self):
		tt = datetime.now()
		dt = tt.strftime("%Y-%m-%d-%H-%M-%S") 
		return  "uDoppler_{:}.csv".format(dt)
		
	def recording_uD(self,writer = None, uD = None ,ts = None, fN = None , label = None, action_id = None):
		if writer is not None:
			if uD is not None:
				#uDf = ['{:.4f}'.format(elem) for elem in uD]
				writer.writerow((fN,label,action_id,uD))
					
					
		
		
	def recording(self,writer = None,v6 = None, v7= None ,v8 = None):
		if writer is not None:
			ts = datetime.now()
			if v6 is not None:
				if len(v6) > 0:
					v6l = v6.values.tolist()
					for i in v6l: 
						i.insert(0,ts)
						writer.writerow(i)
			if v7 is not None:
				if len(v7) > 0:
					v7l = v7.values.tolist()
					for i in v7l:
						i.insert(0,ts) 
						writer.writerow(i)
			if v8 is not None:
				if len(v8) > 0:
					v8 = v8.values.tolist()
					for i in v8l: 
						i.insert(0,ts)
						writer.writerow(i)
		

