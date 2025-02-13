import pyqtgraph as pg
import pyqtgraph.opengl as gl
from pyqtgraph.Qt import QtGui, QtCore, QtWidgets
import numpy as np


class Plot2D:
	def __init__(self):
		self.win = pg.GraphicsLayoutWidget(show=True)
		self.win.resize(900, 900)
		pg.setConfigOption('foreground', 'y')
		self.win.setWindowTitle('2D Scatter Plot')

		self.plot = self.win.addPlot()
		self.plot.setLabel('bottom', 'X Axis', 'meter')
		self.plot.setLabel('left', 'Y Axis', 'meter')
		self.plot.showGrid(x=True, y=True, alpha=0.7)
		self.plot.setAspectLocked()
		self.plot.addLine(x=0, pen=1.0)
		self.plot.addLine(y=0, pen=1.0)

		for r in range(1, 10, 1):
			circle = pg.QtWidgets.QGraphicsEllipseItem(-r, -r, r * 2, r * 2)
			circle.setPen(pg.mkPen(1.0))
			self.plot.addItem(circle)

		self.scatter = pg.ScatterPlotItem(size=2, pen=pg.mkPen('w'), pxMode=True)
		self.plot.addItem(self.scatter)

	def update_plot(self, data):
		"""Update 2D scatter plot with new data."""
		if data is not None and len(data) > 0:
			self.scatter.setData(pos=data[:, (0, 1)], pen='g', symbol='o')
		else:
			self.scatter.setData(pos=np.empty((0, 2)))  # Clear the plot if no data

class Plot3D:
	def __init__(self, zOffset = None):
		self.win = gl.GLViewWidget()
		self.win.show()
		self.zOffset = zOffset if zOffset != None else 0.0
		self.create_axes()
		self.create_radar_box()

		self.scatter = gl.GLScatterPlotItem()
		self.win.addItem(self.scatter)

	def create_axes(self):
		"""Create coordinate grid and labeled axes."""
		axis_length = 5

		# Grid Item
		griditem = gl.GLGridItem()
		griditem.setSize(10, 10)
		griditem.setSpacing(1, 1)
		self.win.addItem(griditem)

		# Coordinate Labels
		self.coordText(self.win, x=axis_length, y=axis_length, z=axis_length, fontSize=12)
	
	def create_radar_box(self):
		"""Create a box representation for the radar device."""
		
		verX = 0.0625
		verY = 0.05
		verZ = 0.125
		zOffSet = self.zOffset

		# Define vertices for the rectangle (2 triangles forming a square)
		verts = np.array([
			[-verX, 0, verZ + zOffSet],  # Bottom-left
			[verX, 0, verZ + zOffSet],   # Bottom-right
			[verX, 0, -verZ + zOffSet],  # Top-right
			[-verX, 0, -verZ + zOffSet]  # Top-left
		])

		# Define two triangles using indices
		faces = np.array([
			[0, 1, 2],  # First triangle
			[0, 2, 3]   # Second triangle
		])

		# Create mesh item
		evmBox = gl.GLMeshItem(vertexes=verts, faces=faces, smooth=False, drawEdges=True, edgeColor=pg.glColor('r'), drawFaces=False)
		self.win.addItem(evmBox)

	def coordText(self, gview, x=None, y=None, z=None, fontSize=None):
		"""Add labeled axes to the 3D plot."""
		axisitem = gl.GLAxisItem()
		axisitem.setSize(x=x, y=y, z=z)
		gview.addItem(axisitem)

		size = 5 if fontSize is None else fontSize
		font = QtGui.QFont('Helvetica', size)

		# Generate axis labels
		xo = np.linspace(-x, x, x * 2 + 1)
		yo = np.linspace(-y, y, y * 2 + 1)
		zo = np.linspace(0, z, z * 2 + 1)  # Updated zo range

		for i in range(len(xo)):
			axisX = gl.GLTextItem(pos=(xo[i], 0.0, 0.0), text=f'{xo[i]:.1f}', color=(255, 127, 127, 255), font=font)
			gview.addItem(axisX)

		for i in range(len(yo)):
			axisY = gl.GLTextItem(pos=(0.0, yo[i], 0.0), text=f'{yo[i]:.1f}', color=(127, 255, 127, 255), font=font)
			gview.addItem(axisY)

		for i in range(len(zo)):
			axisZ = gl.GLTextItem(pos=(0.0, 0.0, zo[i]), text=f'{zo[i]:.1f}', color=(127, 127, 255, 255), font=font)
			gview.addItem(axisZ)

	def update_plot(self, data):
		"""Update 3D scatter plot with new data."""
		if data is not None and len(data) > 0:
			colors = np.array([[0.0, 1.0, 0.0, 1.0]] * len(data))
			self.scatter.setData(pos=data, color=colors, size=3.0)
		else:
			self.scatter.setData(pos=np.empty((0, 3)))  # Clear the plot if no data
