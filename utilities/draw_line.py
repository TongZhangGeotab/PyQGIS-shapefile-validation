"""
Utility script to add a line segment.
"""

import os

with open(f"{os.path.dirname(os.path.dirname(__file__))}/config.txt", 'r') as file:
    FILE_PATH = file.read()
layer = QgsVectorLayer(FILE_PATH, "", "ogr")

feature = QgsFeature(layer.fields())
feature.setAttributes(["0", "TEST_ROUTE", "0", "Test Group", "2", "10", "0", "test"])
geometry = QgsGeometry.fromPolyline([QgsPoint(0, 0), QgsPoint(0, 0)])
feature.setGeometry(geometry)
layer.dataProvider().addFeatures([feature])
