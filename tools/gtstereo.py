"""
/***************************************************************************
GeoTools
A geosciences toolkit for QGIS.
Copyright (C) 2014  Lachlan Grose

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA. 
***************************************************************************/
"""
import os.path,  sys
currentPath = os.path.dirname( __file__ )
sys.path.append(os.path.abspath(os.path.dirname(__file__) + '/../'))
from geo_tools_dialog import GeoToolsDialog

from PyQt4 import QtGui

from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
import matplotlib.pyplot as plt
import mplstereonet
import random

class Window(QtGui.QDialog):
    def __init__(self, canvas, iface, parent=None):
        super(Window, self).__init__(parent)
        self.canvas = canvas
        self.iface = iface
        self.layer = self.iface.mapCanvas().currentLayer()
        fields = self.layer.pendingFields()
        #self.strike_combo = QtGui.QComboBox()
        #self.dip_combo = QtGui.QComboBox()

        #for f in fields:
        #    self.strike_combo.addItem(f.name())
        #    self.dip_combo.addItem(f.name())
            # a figure instance to plot on
        #self.figure = plt.figure()
        self.figure, self.ax = mplstereonet.subplots()
        # this is the Canvas Widget that displays the `figure`
        # it takes the `figure` instance as a parameter to __init__
        self.canvas = FigureCanvas(self.figure)

        # this is the Navigation widget
        # it takes the Canvas widget and a parent
        self.toolbar = NavigationToolbar(self.canvas, self)

        # Just some button connected to `plot` method
        self.polesbutton = QtGui.QPushButton('Plot Poles')
        self.polesbutton.clicked.connect(self.plotpoles)
        self.circlebutton = QtGui.QPushButton('Plot Circle')
        self.circlebutton.clicked.connect(self.plotcircles)
        self.densitybutton = QtGui.QPushButton('Plot Density')
        self.densitybutton.clicked.connect(self.plotdensity)
        # set the layout
        layout = QtGui.QVBoxLayout()
        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        #layout.addWidget(self.strike_combo)
        #layout.addWidget(self.dip_combo)
        layout.addWidget(self.polesbutton)
        layout.addWidget(self.circlebutton)
        layout.addWidget(self.densitybutton)
        self.setLayout(layout)

    def plotpoles(self):
        strike = []
        dip = []
        for f in self.layer.selectedFeatures():
            dip.append(f['dip']) #self.dip_combo.currentText()])
            strike.append(f['strike'])#self.strike_combo.currentText()]) 
        self.ax.hold(False)
        self.ax.pole(strike, dip)
        self.ax.grid()
        self.canvas.draw()

    def plotdensity(self):
        strike = []
        dip = []
        for f in self.layer.selectedFeatures():
            dip.append(f['dip']) #self.dip_combo.currentText()])
            strike.append(f['strike'])#self.strike_combo.currentText()]) 
        # discards the old graph
        self.ax.hold(False)
        self.ax.hold(True)

        self.ax.density_contourf(strike,dip,measurement='poles')
        self.ax.pole(strike, dip)
        self.ax.grid(True)
        # refresh canvas
        self.canvas.draw()

    def plotcircles(self):
        strike = []
        dip = []
        for f in self.layer.selectedFeatures():
            dip.append(f['dip']) #self.dip_combo.currentText()])
            strike.append(f['strike'])#self.strike_combo.currentText()]) 
        self.ax.hold(False)
        self.ax.plane(strike, dip)
        self.ax.grid()

        # refresh canvas
        self.canvas.draw()


class GtStereo():
  def __init__(self, canvas,iface):
      self.canvas = canvas
      self.iface = iface

        
  def run(self):
        """Run method that performs all the real work"""

        self.main = Window(self.canvas,self.iface)
        # show the dialog
        self.main.show()
        # Run the dialog event loop
        #result = self.dlg.exec_()
        # See if OK was pressed
        #if result:
            # Do something useful here - delete the line containing pass and
            # substitute with your code.
         #   pass      
