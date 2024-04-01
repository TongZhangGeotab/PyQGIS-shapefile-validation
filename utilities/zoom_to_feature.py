import os

file_path = os.path.expanduser('~/Downloads/LasVegas_Demo_Data/LasVegas_Route.shp')
layer = QgsVectorLayer(file_path, '', 'ogr')

canvas = iface.mapCanvas()  # Get the map canvas
feature_id = 510  # Replace with the ID of the feature you want to zoom to

# Assuming 'line_layer' is your QgsVectorLayer instance
feature = layer.getFeature(feature_id)  # Get the feature by its ID

# Check if the feature exists and has geometry
if feature and feature.hasGeometry():
    # Zoom to the bounding box (extent) of the feature
    canvas.setExtent(feature.geometry().boundingBox())
    canvas.refresh()  # Refresh the map canvas to apply the changes