import os

file_path = os.path.expanduser('~/Downloads/LasVegas_Demo_Data/LasVegas_Route.shp')
layer = QgsVectorLayer(file_path, '', 'ogr')

feature = QgsFeature(layer.fields())
feature.setAttributes(['test_route', 'TEST', '600', '2', '10', 'test_segment'])
geometry = QgsGeometry.fromPolyline([QgsPoint(-115.209, 36.214025), QgsPoint(-115.209, 36.213103)])
feature.setGeometry(geometry)
layer.dataProvider().addFeatures([feature])
