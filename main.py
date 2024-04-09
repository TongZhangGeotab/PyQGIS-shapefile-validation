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

# Constant for coordinates
CRS = "EPSG:4326"

# Constants for min and max segment lengths
MIN_BOUND = 20
MAX_BOUND = 1000

def main():
    iface.addVectorLayer(FILE_PATH, "", "ogr")
    QCoreApplication.processEvents()
    instance = QgsProject.instance()
    layer = QgsVectorLayer(FILE_PATH, "", "ogr")
    crs_object = QgsCoordinateReferenceSystem(CRS)

    # Configure a logger
    configure_logger.configure_logger(
        os.path.dirname(os.path.realpath(__file__)),
        datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S"),
    )
    logger = logging.getLogger("QGIS_logger")

    feedback_message = ""
    null_geoms = set()

    # Check the attribute table
    fieldCheck = fields.Fields(layer=layer)
    fieldCheck.run()

    result, message = fieldCheck.getFeedback()
    if result:
        feedback_message += message

    # Check the coordinate system
    coordinateCheck = coordinates.Coordinates(
        layer=layer,
        correct_crs=crs_object,
        instance=instance,
    )
    coordinateCheck.run()

    result, message = coordinateCheck.getFeedback()
    if result:
        feedback_message += message

    # Check for intersections
    index = QgsSpatialIndex()
    
    intersectionCheck = intersections.Intersections(
        layer=layer,
        index=index,
    )
    intersection_nulls = intersectionCheck.run()
    null_geoms.update(intersection_nulls)

    result, message = intersectionCheck.getFeedback()
    if result:
        feedback_message += message

    # Check the lengths
    distance_area_object = QgsDistanceArea()
    distance_area_object.setEllipsoid("WGS84")
    distance_area_object.setSourceCrs(crs_object, instance.transformContext())

    lengthCheck = lengths.Lengths(
        layer=layer,
        min_bound=MIN_BOUND,
        max_bound=MAX_BOUND,
        distance_area=distance_area_object,
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
