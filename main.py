"""
Main script that runs in the QGIS environment
"""

import datetime
import logging
import os

from modules import fields
from modules import coordinates
from modules import intersections
from modules import lengths
from utilities import configure_logger

# Upload layer and update project instance
with open(f"{os.path.dirname(__file__)}/config.txt", 'r') as file:
    FILE_PATH = file.read()
LAYER = QgsVectorLayer(FILE_PATH, "", "ogr")
iface.addVectorLayer(FILE_PATH, "", "ogr")
QCoreApplication.processEvents()

# Constants for coordinates
CRS = "EPSG:4326"
INSTANCE = QgsProject.instance()

# Spatial index for checking intersections
INDEX = QgsSpatialIndex()

# Constants for min and max segment lengths
MIN_BOUND = 20
MAX_BOUND = 1000

# Setup for distance measuring object
DISTANCE_AREA = QgsDistanceArea()
DISTANCE_AREA.setEllipsoid("WGS84")
CRS = QgsCoordinateReferenceSystem(CRS)
DISTANCE_AREA.setSourceCrs(CRS, QgsProject.instance().transformContext())

# Configure a logger
configure_logger.configure_logger(
    os.path.dirname(os.path.realpath(__file__)),
    datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
)
logger = logging.getLogger("QGIS_logger")


def main():
    feedback_message = ""
    null_geoms = set()

    # Check the attribute table
    fieldCheck = fields.Fields(layer=LAYER)
    fieldCheck.run()

    result, message = fieldCheck.getFeedback()
    if result:
        feedback_message += message

    # Check the coordinate system
    coordinateCheck = coordinates.Coordinates(
        layer=LAYER,
        correct_crs=CRS,
        instance=INSTANCE,
    )
    coordinateCheck.run()

    result, message = coordinateCheck.getFeedback()
    if result:
        feedback_message += message

    # Check for intersections
    intersectionCheck = intersections.Intersections(
        layer=LAYER,
        index=INDEX,
    )
    intersection_nulls = intersectionCheck.run()
    null_geoms.update(intersection_nulls)

    result, message = intersectionCheck.getFeedback()
    if result:
        feedback_message += message

    # Check the lengths
    lengthCheck = lengths.Lengths(
        layer=LAYER,
        min_bound=MIN_BOUND,
        max_bound=MAX_BOUND,
        distance_area=DISTANCE_AREA,
    )
    length_nulls = lengthCheck.run()
    null_geoms.update(length_nulls)

    result, message = lengthCheck.getFeedback()
    if result:
        feedback_message += message

    # Log geometries with Null values
    if null_geoms:
        logger.error(f"{len(null_geoms)} features have Null geometry")
        logger.info(f"features with Null geometry: {null_geoms}")

    return feedback_message


feedback_message = main()
if feedback_message:
    print(feedback_message)
