"""
Utility script to zoom to a feature by id.
"""

import os

feature_id = 510

file_path = os.path.expanduser("~/Downloads/LasVegas_Demo_Data/LasVegas_Route.shp")
layer = QgsVectorLayer(file_path, "", "ogr")

canvas = iface.mapCanvas()
feature = layer.getFeature(feature_id)

if feature and feature.hasGeometry():
    canvas.setExtent(feature.geometry().boundingBox())
    canvas.refresh()
else:
    print(f"feature {feature_id} does not exist")
