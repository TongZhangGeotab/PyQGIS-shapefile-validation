"""
Utility script to add a line segment.
"""

import os

file_path = os.path.expanduser("~/Downloads/Mississauga_Demo_Data/Halton_roads.shp")
layer = QgsVectorLayer(file_path, "", "ogr")

feature = QgsFeature(layer.fields())
feature.setAttributes(["0", "TEST_ROUTE", "600", "Test Group", "2", "10", "425", "test"])
geometry = QgsGeometry.fromPolyline([QgsPoint(-79.1719, 43.57), QgsPoint(-79.1719, 43.903)])
feature.setGeometry(geometry)
layer.dataProvider().addFeatures([feature])
