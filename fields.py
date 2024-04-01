import os

file_path = os.path.expanduser('~/Downloads/LasVegas_Demo_Data/LasVegas_Route.shp')
layer = QgsVectorLayer(file_path, '', 'ogr')

fields = [field.name() for field in layer.fields()]
print(len(fields))
print(fields)

error_message = ''

mandatory_fields = {
    'group': False,
    'route': False,
    'segment': False,
    'roadwidth': False,
    'passcount': False,
}

for field in fields:
    if field.lower() in mandatory_fields:
        mandatory_fields[field.lower()] = field

if not mandatory_fields['group']:
    error_message += 'group column is missing\n'
else:
    groups = [(feature[mandatory_fields['group']], feature.id()) for feature in layer.getFeatures()]
    for group, id in groups:
        if group is None:
            error_message += f'feature {id} has NULL group value\n'
if not mandatory_fields['route']:
    error_message += 'route column is missing\n'
else:
    routes = [(feature[mandatory_fields['route']], feature.id()) for feature in layer.getFeatures()]
    for route, id in routes:
        if route is None:
            error_message += f'feature {id} has NULL route value\n'

if not mandatory_fields['segment']:
    error_message += 'segment column is missing\n'
else:
    segments = [(feature[mandatory_fields['segment']], feature.id()) for feature in layer.getFeatures()]
    segment_set = set()
    duplicate_segments = set()
    for segment in segments:
        if segment is None:
            error_message += f'feature {id} has NULL segment value\n'
        elif segment in segment_set:
            duplicate_segments.add(segment)
        else:
            segment_set.add(segment)
    
    for duplicate in duplicate_segments:
        error_message += f'duplicated segment: {duplicate}\n'

if mandatory_fields['roadwidth']:
    roadwidth_type = layer.fields().field(mandatory_fields['roadwidth']).typeName()
    if 'int' not in roadwidth_type.lower():
        error_message += f'roadwidth datatype is {roadwidth_type} not integer\n'

    roadwidths = [(feature[mandatory_fields['roadwidth']], feature.id()) for feature in layer.getFeatures()]
    for roadwidth, id in roadwidths:
        if roadwidth <= 0:
            error_message += f'feature {id} has non positive roadwidth value\n'

if mandatory_fields['passcount']:
    passcount_type = layer.fields().field(mandatory_fields['passcount']).typeName()
    if 'int' not in passcount_type.lower():
        error_message += f'passcount datatype is {passcount_type} not integer\n'

    passcounts = [(feature[mandatory_fields['passcount']], feature.id()) for feature in layer.getFeatures()]
    for passcount, id in passcounts:
        if passcount <= 0:
            error_message += f'feature {id} has non positive passcount value\n'

if error_message:
    print(f'Errors:\n{error_message}')