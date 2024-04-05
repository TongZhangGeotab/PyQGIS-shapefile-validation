"""
Class for checking intersections
"""

import logging


class Intersections:
    """
    Checks for intersections in the layet
    """

    def __init__(self, layer, index):
        """
        Constructor
        """
        self._layer = layer
        self._logger = logging.getLogger("QGIS_logger")

        # Spatial index
        self._index = index

        # Track if an error exists and the feedback message
        self._error = False
        self._feedback_message = "\nSegments must not overlap or intersect to reduce instances of vehicles accidentally entering neighboring segments. Overlapping segments may cause the Route Completion Report to inaccurately reflect vehicle passes on segments. If intersecting or overlapping segments exist, run a tool (for example, Split Lines) at intersections to produce a non-intersection line layer.\n"

    @staticmethod
    def get_endpoints(geometry):
        """
        Gets the endpoints (first and last point) for a line segment
        """
        # If multipart, get the first point of the first part and the last point of the last part
        if geometry.isMultipart():
            lines = geometry.asMultiPolyline()
            p1 = lines[0][0]
            p2 = lines[-1][-1]
        # If single line, get the first and last point
        else:
            line = geometry.asPolyline()
            p1 = line[0]
            p2 = line[-1]

        return p1, p2

    def run(self):
        """
        Determine all errors caused by intersections
        """
        features = list(self._layer.getFeatures())

        # Add all features to spatial index and create a reference key by id
        feature_dict = {}
        for feature in features:
            self._index.insertFeature(feature)
            feature_dict[feature.id()] = feature

        intersections = set()
        null_geoms = set()
        for f1 in features:
            g1 = f1.geometry()
            if not g1:
                null_geoms.add(f1.id())
                continue
            p11, p12 = self.get_endpoints(g1)

            # Find possible intersections by bounding box - cheaper than with true intersection
            candidate_ids = self._index.intersects(g1.boundingBox())
            for candidate_id in candidate_ids:
                # Do not test a segment against itself
                if candidate_id == f1.id():
                    continue

                f2 = feature_dict[candidate_id]
                g2 = f2.geometry()
                if not g2:
                    null_geoms.add(f2.id())
                    continue

                # Check if a candidate actually intersects
                if g1.intersects(g2):
                    # Check if the lines only touch at the ends - not a true intersection
                    p21, p22 = self.get_endpoints(g2)
                    if p11 != p21 and p11 != p22 and p12 != p21 and p12 != p22:
                        # Make sure we're not adding duplicates
                        id1 = min(f1.id(), f2.id())
                        id2 = max(f1.id(), f2.id())
                        intersections.add((id1, id2))

        # Log an error if there are intersections
        if intersections:
            self._error = True
            self._logger.error(f"{len(intersections)} intersections in the shapefile")
            self._logger.info(f"intersections: {intersections}")

        return null_geoms

    def getFeedback(self):
        """
        Return the feedback message
        """
        if self._error:
            return True, self._feedback_message
        return False, None
