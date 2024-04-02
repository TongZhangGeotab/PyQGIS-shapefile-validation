import os

from modules import fields
from modules import intersections
from modules import lengths

FILE_PATH = os.path.expanduser('~/Downloads/Mississauga_Demo_Data/Halton_roads.shp')
LAYER = QgsVectorLayer(FILE_PATH, '', 'ogr')

INDEX = QgsSpatialIndex()

SOURCE_CRS = QgsCoordinateReferenceSystem(4326)
DEST_CRS = QgsCoordinateReferenceSystem(3395)
TRANSFORM = QgsCoordinateTransform(SOURCE_CRS, DEST_CRS, QgsProject.instance())
MAX_BOUND = 300
MIN_BOUND = 100

def main():
    error_message = ''

    fieldCheck = fields.Fields(LAYER)
    fieldCheck.run()
    error_message += fieldCheck.getErrorMessage()

    intersectionCheck = intersections.Intersections(
        layer=LAYER,
        index=INDEX,
    )
    intersectionCheck.run()
    error_message += intersectionCheck.getErrorMessage()

    lengthCheck = lengths.Lengths(
        layer=LAYER,
        transform=TRANSFORM,
        min_bound=MIN_BOUND,
        max_bound=MAX_BOUND,
    )
    lengthCheck.run()
    error_message += lengthCheck.getErrorMessage()

    return error_message

error_message = main()
if error_message:
    print(error_message)