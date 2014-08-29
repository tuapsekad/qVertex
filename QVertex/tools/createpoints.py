# -*- coding: utf-8 -*-
__author__ = 'filippov'

from PyQt4.QtGui import *
from qgis.core import *

numLayer = 0


class CreatePoints():
    def __init__(self, iface):
        self.iface = iface
        self.numPoint = 0

        if (self.iface.mapCanvas().currentLayer() is not None) \
                and (self.iface.mapCanvas().currentLayer().selectedFeatures() is not None):
            self.selection = self.iface.mapCanvas().currentLayer().selectedFeatures()
            self.workLayer = self.iface.activeLayer()
            self.CrsSelectLayer = self.iface.mapCanvas().currentLayer().crs().authid()
            self.UriLayer = "Point?crs=%s&field=name:string(8)&index=yes" % self.CrsSelectLayer
            self.targetLayer = self.createNewLayer()
        else:
            QMessageBox.warning(self.iface.mainWindow(), u"Внимание", u"Нет выбранных объектов", QMessageBox.Ok)
            return False


    def Create(self):
        if (self.selection is None):
            return False
        self.targetLayer.startEditing()

        for every in self.selection:
            geom = every.geometry()
            self.createP(geom)
            for f in self.workLayer.getFeatures():
                if geom.contains(f.geometry()):
                    if f.geometry().exportToWkt() != geom.exportToWkt():
                        self.createP(f.geometry())

        self.targetLayer.commitChanges()
        self.removeDuplicate(self.targetLayer)


    def removeDuplicate(self, layer):
        layer.startEditing()

        geometries = []
        for feature in layer.getFeatures():
            geometries.append(feature.geometry().exportToWkt())

        for x in range(0, len(geometries) - 1):
            if geometries[x] != None:
                for y in range(x + 1, len(geometries)):
                    if geometries[x] == geometries[y]:
                        geometries[y] = None

        for index, feature in enumerate(layer.getFeatures()):
            layer.deleteFeature(feature.id())
            if geometries[index] != None:
                layer.addFeature(feature)

        for index, feature in enumerate(layer.getFeatures()):
            layer.changeAttributeValue(feature.id(), 0, u'н' + str(index + 1))

        layer.commitChanges()


    def createP(self, geom):
        if geom.isMultipart():
            polygons = geom.asMultiPolygon()
            for polygone in polygons:
                self.numberRing = 0
                for ring in polygone:
                    iter = 0
                    self.numberRing += 1
                    for i in ring:
                        if iter < len(ring) - 1:
                            self.numPoint += 1
                            self.createPointOnLayer(i, self.numPoint)
                        iter += 1

        else:
            self.numberRing = 0
            rings = geom.asPolygon()
            for ring in rings:
                iter = 0
                self.numberRing += 1
                for i in ring:
                    if iter < len(ring) - 1:
                        self.numPoint += 1
                        self.createPointOnLayer(i, self.numPoint)
                    iter += 1


    def createPointOnLayer(self, point, name):
        feature = QgsFeature()
        feature.initAttributes(len(self.targetLayer.dataProvider().attributeIndexes()))
        feature.setGeometry(QgsGeometry.fromPoint(point))
        feature.setAttribute(self.targetLayer.fieldNameIndex(u'name'), u'н' + str(name))
        self.targetLayer.dataProvider().addFeatures([feature])
        del feature
        return True


    def createNewLayer(self):
        layer = QgsVectorLayer(self.UriLayer, u'.Точки' + str(self.getNumLayers()), "memory")

        layer.startEditing()
        layer.setCustomProperty("labeling", "pal")
        layer.setCustomProperty("labeling/enabled", "true")
        layer.setCustomProperty("labeling/fontSize", "9")
        layer.setCustomProperty("labeling/fieldName", "name")
        layer.commitChanges()

        QgsMapLayerRegistry.instance().addMapLayers([layer])
        return layer


    def getNumLayers(self):
        global numLayer
        numLayer += 1
        return numLayer
