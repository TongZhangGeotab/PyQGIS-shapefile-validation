"""
Utility script to zoom to a feature by id.
"""

import os

feature_id = 1

with open(f"{os.path.dirname(__file__)}/config.txt", 'r') as file:
    FILE_PATH = file.read()
layer = QgsVectorLayer(FILE_PATH, "", "ogr")

canvas = iface.mapCanvas()
feature = layer.getFeature(feature_id)

if feature and feature.hasGeometry():
    canvas.setExtent(feature.geometry().boundingBox())
    canvas.refresh()
else:
    print(f"feature {feature_id} does not exist")
