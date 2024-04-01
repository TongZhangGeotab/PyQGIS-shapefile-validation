class Lengths:
    def __init__(self, layer, transform, min_bound, max_bound):
        self._layer = layer
        self._error_message = ''
        self._transform = transform
        self._min_bound = min_bound
        self._max_bound = max_bound

    def run(self):
        # Calculate length in meters for each feature in the layer
        for f in self._layer.getFeatures():
            geom = f.geometry()
            geom.transform(self._transform)  # Reproject the geometry
            length_meters = geom.length()  # Get the length in meters
            if length_meters > self._max_bound:
                self._error_message += f'warning: feature {f.id()} exceeds {self._max_bound} m\n'
            if length_meters < self._min_bound:
                self._error_message += f'warning: feature {f.id()} less than {self._min_bound} m\n'

    def getErrorMessage(self):
        return self._error_message
