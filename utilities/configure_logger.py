"""
Utility script to set up the logger.
"""

import datetime
import logging
import os


LOGGING_LEVEL = logging.DEBUG
LOGGING_LEVEL_STREAM = logging.WARNING


def configure_logger(root_directory_path, time):
    log_file_name = os.path.join(root_directory_path, "logs", f"{time}.log")

    logger = logging.getLogger("QGIS_logger")
    logger.setLevel(LOGGING_LEVEL)

    formatter = logging.Formatter(
        fmt="%(asctime)s: [%(levelname)s] %(message)s", datefmt="%I:%M:%S"
    )

    file_handler = logging.FileHandler(filename=log_file_name, mode="w")
    file_handler.setLevel(LOGGING_LEVEL)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(LOGGING_LEVEL_STREAM)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
