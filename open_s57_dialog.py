# -*- coding: utf-8 -*-

import os

from qgis.PyQt import uic
from qgis.PyQt import QtWidgets
from PyQt5.QtWidgets import QFileDialog, QMessageBox
from PyQt5.QtGui import QColor

from qgis.core import (QgsVectorLayer, QgsProject, QgsMapLayer, QgsLayoutItemLegend,  QgsLegendRenderer,
                       QgsLegendStyle, QgsLayerTreeNode,  QgsWkbTypes, QgsPalLayerSettings,
                       QgsSimpleMarkerSymbolLayerBase, QgsVectorLayerSimpleLabeling)
from qgis.utils import iface


FORM_CLASS, _ = uic.loadUiType(os.path.join(
    os.path.dirname(__file__), 'dlg_open_s57.ui'))


class ImportS57Dialog(QtWidgets.QDialog, FORM_CLASS):
    def __init__(self, parent=None):
        super(ImportS57Dialog, self).__init__(parent)
        self.setupUi(self)
        self.path = None
        self.layer = None

        self.btn_file.clicked.connect(self.choose_file)
        self.btn_import.clicked.connect(self.load_map)

    def choose_file(self):
        self.path = QFileDialog.getOpenFileName(self, 'Выберите файл', "", "Карта (*.000*)")[0]
        self.le_path.setText(self.path)

    def load_map(self):
        if not self.path:
            QMessageBox.warning(self, "Ошибка!", "Выберите файл", QMessageBox.Ok)
        else:
            if os.path.exists(self.path):
                self.layer = iface.addVectorLayer(self.path, "", "")
                self.hide_layers()
                self.change_order()
                self.change_style()
                self.add_labels()
            else:
                QMessageBox.warning(self, "Ошибка!", "Такого пути не существует", QMessageBox.Ok)
        self.le_path.setText("")

    def hide_layers(self):
        keep_layers = ("LNDARE", "RESARE", "DEPARE", "COALNE", "DEPCNT", "LIGHTS", "BOYLAT",  "BOYSPP", "LNDMRK")
        invis_layers = [layer for layer in QgsProject.instance().mapLayers().values()
                        if layer.name().split(" — ")[-1] not in keep_layers or
                        layer.name().split(" — ")[-1] == "LNDARE" and layer.geometryType() == QgsWkbTypes.PointGeometry]
        self.vis_layers =  {layer.name().split(" — ")[-1]: layer for layer in QgsProject.instance().mapLayers().values()
                            if layer not in invis_layers}

        for layer in invis_layers:
            # QgsProject.instance().removeMapLayer(layer)
            QgsProject.instance().layerTreeRoot().findLayer(layer).setItemVisibilityChecked(False)
    def change_order(self):
        order = iface.layerTreeCanvasBridge().rootGroup().customLayerOrder()
        order = sorted((sorted(order, key=lambda y: y.name())), key=lambda x: x.geometryType())
        QgsProject.instance().layerTreeRoot().setHasCustomLayerOrder(True)
        QgsProject.instance().layerTreeRoot().setCustomLayerOrder(order)
        for layer in order:
            layer.triggerRepaint()
            iface.layerTreeView().refreshLayerSymbology(layer.id())

    def change_style(self):
        styles = {"LNDARE": {"color": (229, 182, 55)},
                  "RESARE": {"color": (52, 166, 176)},
                  "DEPARE": {"color": (173, 202, 205)},
                  "COALNE": {"color": (140, 90, 28), "width": 1.4},
                  "DEPCNT": {"color": (0, 58, 155)},
                  "LIGHTS": {"color": (255, 144, 53), "style": QgsSimpleMarkerSymbolLayerBase.Star, "size": 5.5},
                  "BOYLAT": {"color": (230, 245, 255)},
                  "BOYSPP": {"color": (247, 228,72)},
                  "LNDMRK": {"color":(0,0,0), "style":QgsSimpleMarkerSymbolLayerBase.Triangle}
                  }
        for name in self.vis_layers:
            layer = self.vis_layers[name]
            layer.renderer().symbol().setColor(QColor.fromRgb(*styles[name]["color"]))
            if "style" in styles[name]:
                layer.renderer().symbol().symbolLayer(0).setShape(styles[name]["style"])
            if "size" in styles[name]:
                layer.renderer().symbol().setSize(styles[name]["size"])
            if "width" in styles[name]:
                layer.renderer().symbol().symbolLayer(0).setWidth(styles[name]["width"])
            layer.triggerRepaint()
            iface.layerTreeView().refreshLayerSymbology(layer.id())

    def add_labels(self):
        fields = {"DEPCNT" : "VALDCO", "BOYSPP": "INFORM", "LNDMRK": "OBJNAM"}
        for name in self.vis_layers:
            if name in fields:
                layer = self.vis_layers[name]
                settings = QgsPalLayerSettings()
                settings.fieldName = fields[name]
                if layer.geometryType() == QgsWkbTypes.LineGeometry:
                    settings.placement = QgsPalLayerSettings.Line

                labels = QgsVectorLayerSimpleLabeling(settings)
                layer.setLabelsEnabled(True)
                layer.setLabeling(labels)
                layer.triggerRepaint()
