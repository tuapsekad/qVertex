# -*- coding: utf-8 -*-
__author__ = 'filippov'

#from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *


class CreatePoints():
    def __init__(self, iface):
        self.iface = iface
        self.layermap = QgsMapLayerRegistry.instance().mapLayers()
        for name, layer in self.layermap.iteritems():
            #QMessageBox.information(self.iface.mainWindow(), layer.name(), str())
            if layer.type() == QgsMapLayer.VectorLayer and layer.name() == u"Точки":
                if layer.isValid():
                    self.selection = layer.electedFeatures()
                else:
                    self.selection = None

    def Create(self):
        listPonts = []
        for every in self.selection:
            geom = every.geometry()
            if geom.isMultipart():
                polygons = geom.asMultiPolygon()
                for polygone in polygons:
                    self.numberRing = 0
                    for ring in polygone:
                        listPonts = []
                        self.numberRing += 1
                        for i in ring:
                            x = round(i.x(), 2)
                            y = round(i.y(), 2)
                            listPonts.append([x, y])

                        self.doAppend(listPonts)

            else:
                self.numberRing = 0
                rings = geom.asPolygon()
                for ring in rings:
                    listPonts = []
                    self.numberRing += 1
                    for i in ring:
                        x = round(i.x(), 2)
                        y = round(i.y(), 2)
                        listPonts.append([x, y])

                    self.doAppend(listPonts)