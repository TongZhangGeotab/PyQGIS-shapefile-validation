import os

# file_path = os.path.expanduser('~/Downloads/Mississauga_Demo_Data/Halton_Roads.shp')
file_path = os.path.expanduser('~/Downloads/LasVegas_Demo_Data/LasVegas_Route.shp')
layer = QgsVectorLayer(file_path, '', 'ogr')

# intersections = []

error_message = ''

def get_endpoints(geometry):
    # If multipart, get the first point of the first part and the last point of the last part
    if geometry.isMultipart():
        lines = geometry.asMultiPolyline()
        p1 = lines[0][0]
        p2 = lines[-1][-1]
    else:
        line = geometry.asPolyline()
        p1 = line[0]
        p2 = line[-1]
    return p1, p2

features = list(layer.getFeatures())

for i, f1 in enumerate(features):
    g1 = f1.geometry()
    p11, p12 = get_endpoints(g1)
    for f2 in features[i+1:]:
        g2 = f2.geometry()
        if g1.intersects(g2):
            p21, p22 = get_endpoints(g2)
            if p11 != p21 and p11 != p22 and p12 != p21 and p12 != p22:
                error_message += f'intersection between feature {f1.id()} and feature {f2.id()}\n'
