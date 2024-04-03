import datetime
import logging
import os


def configure_logger(root_directory_path):
    CURRENT_TIME = datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
    LOG_FILE_NAME = os.path.join(root_directory_path, 'logs', f"{CURRENT_TIME}.log")
    LOGGING_LEVEL = logging.DEBUG

    file_handler = logging.FileHandler(filename=LOG_FILE_NAME, mode="w")
    stream_handler = logging.StreamHandler()
    formatter = logging.Formatter(
        fmt="%(asctime)s: [%(levelname)s] %(message)s",
        datefmt="%I:%M:%S"
    )
    file_handler.setFormatter(formatter)
    stream_handler.setFormatter(formatter)

    logger = logging.getLogger("QGIS_logger")
    logger.setLevel(LOGGING_LEVEL)
    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
