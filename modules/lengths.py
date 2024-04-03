"""
Class for checking the lenght of line segments
"""


class Lengths:
    """
    Checks line segment lengths
    """

    def __init__(self, layer, transform, min_bound, max_bound):
        """
        Constructor
        """
        self._layer = layer
        self._error_message = ""
        self._transform = transform
        self._min_bound = min_bound
        self._max_bound = max_bound

    def run(self):
        """
        Determine all warnings caused by line segment lengths
        """
        # Calculate length in meters for each feature in the layer
        for f in self._layer.getFeatures():
            geom = f.geometry()
            geom.transform(self._transform)
            length_meters = geom.length()
            # If line is too long or too short, add warning
            if length_meters > self._max_bound:
                self._error_message += f"warning: feature {f.id()} exceeds {self._max_bound} m\n"
            if length_meters < self._min_bound:
                self._error_message += f"warning: feature {f.id()} less than {self._min_bound} m\n"

    def getErrorMessage(self):
        """
        Returns the error message
        """
        return self._error_message
