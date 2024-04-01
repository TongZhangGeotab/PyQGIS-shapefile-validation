import os

file_path = os.path.expanduser('~/Downloads/LasVegas_Demo_Data/LasVegas_Route.shp')
layer = QgsVectorLayer(file_path, '', 'ogr')

source_crs = QgsCoordinateReferenceSystem(4326)  # WGS 84
dest_crs = QgsCoordinateReferenceSystem(3395)    # WGS 84 to UTM
transform = QgsCoordinateTransform(source_crs, dest_crs, QgsProject.instance())

distances = []

# Calculate length in meters for each feature in the layer
for feature in layer.getFeatures():
    geom = feature.geometry()
    geom.transform(transform)  # Reproject the geometry
    length_meters = geom.length()  # Get the length in meters
    distances.append((length_meters, feature.id(), feature.attributes()))

print(max(distances, key=lambda d:d[0]), min(distances, key=lambda d:d[0]), sum([d[0] for d in distances])/len(distances))