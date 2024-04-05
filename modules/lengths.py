"""
Class for checking the lenght of line segments.
"""

import logging


class Lengths:
    """
    Checks line segment lengths.
    """

    def __init__(self, layer, min_bound, max_bound, distance_area):
        """
        Constructor.
        """
        self._layer = layer
        self._logger = logging.getLogger("QGIS_logger")

        # Bounds constants
        self._min_bound = min_bound
        self._max_bound = max_bound

        # QgsDistanceArea class instance
        self._distance_area = distance_area

        # Track if an error exists and the feedback message
        self._warn = True
        self._feedback_message = "\nTo obtain an efficient and accurate Route Completion Report, road segment lengths should be approximately 100 meters to 300 meters in length, and should start or end the intersections, but not overlap at intersections. If the segments are too small, the report will be overly detailed. If the segments are too long, the report will lack detail. Reconsider and adjust the segment lengths according to the scale that the report will be viewed in, and how much detail is necessary.\n"

    def run(self):
        """
        Determine all warnings caused by line segment lengths.
        """
        short_lines = []
        long_lines = []

        # Calculate length in meters for each feature in the layer
        null_geoms = set()
        for f in self._layer.getFeatures():
            geom = f.geometry()
            if not geom:
                null_geoms.add(f.id())
                continue
            length_meters = self._distance_area.measureLength(geom)

            # If line is too long or too short, add to list
            if length_meters > self._max_bound:
                long_lines.append(f.id())
            if length_meters < self._min_bound:
                short_lines.append(f.id())

        if not short_lines and not long_lines:
            self._warn = False

        # Log a warning for all lines that are too short
        if short_lines:
            self._logger.warning(f"{len(short_lines)} features are less than {self._min_bound} m")
            self._logger.info(f"features less than {self._min_bound} m: {short_lines}")
        # Log a warning for all lines that are too long
        if long_lines:
            self._logger.warning(f"{len(long_lines)} features are greater than {self._max_bound} m")
            self._logger.info(f"features greater than {self._max_bound} m: {long_lines}")

        return null_geoms

    def getFeedback(self):
        """
        Returns the feedback message.
        """
        if self._warn:
            return True, self._feedback_message
        return False, None
