import datetime
import logging
import os

from modules import fields
from modules import intersections
from modules import lengths
from utilities import configure_logger

FILE_PATH = os.path.expanduser("~/Downloads/Mississauga_Demo_Data/Halton_roads.shp")
LAYER = QgsVectorLayer(FILE_PATH, "", "ogr")
# iface.addVectorLayer(FILE_PATH, '', 'ogr')

INDEX = QgsSpatialIndex()

MIN_BOUND = 20
MAX_BOUND = 1000

DISTANCE_AREA = QgsDistanceArea()
DISTANCE_AREA.setEllipsoid("WGS84")
CRS = QgsCoordinateReferenceSystem("EPSG:4326")
DISTANCE_AREA.setSourceCrs(CRS, QgsProject.instance().transformContext())

configure_logger.configure_logger(
    os.path.dirname(os.path.realpath(__file__)),
    datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
)


def main():
    logger = logging.getLogger("QGIS_logger")

    feedback_message = ""

    fieldCheck = fields.Fields(LAYER)
    fieldCheck.run()

    intersectionCheck = intersections.Intersections(
        layer=LAYER,
        index=INDEX,
    )
    intersectionCheck.run()

    lengthCheck = lengths.Lengths(
        layer=LAYER,
        min_bound=MIN_BOUND,
        max_bound=MAX_BOUND,
        distance_area=DISTANCE_AREA,
    )
    lengthCheck.run()

    result, message = fieldCheck.getFeedback()
    if result:
        feedback_message += message

    result, message = intersectionCheck.getFeedback()
    if result:
        feedback_message += message

    result, message = lengthCheck.getFeedback()
    if result:
        feedback_message += message

    return feedback_message


feedback_message = main()
if feedback_message:
    print(feedback_message)
