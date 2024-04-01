class Intersections:
    def __init__(self, layer):
        self._layer = layer
        self._error_message = ''
    
    @staticmethod
    def get_endpoints(geometry):
        # If multipart, get the first point of the first part and the last point of the last part
        if geometry.isMultipart():
            lines = geometry.asMultiPolyline()
            p1 = lines[0][0]
            p2 = lines[-1][-1]
        else:
            line = geometry.asPolyline()
            p1 = line[0]
            p2 = line[-1]
        return p1, p2
    
    def run(self):
        features = list(self._layer.getFeatures())

        for i, f1 in enumerate(features):
            g1 = f1.geometry()
            p11, p12 = self.get_endpoints(g1)
            for f2 in features[i+1:]:
                g2 = f2.geometry()
                if g1.intersects(g2):
                    p21, p22 = self.get_endpoints(g2)
                    if p11 != p21 and p11 != p22 and p12 != p21 and p12 != p22:
                        self._error_message += f'error: intersection between feature {f1.id()} and feature {f2.id()}\n'

    def getErrorMessage(self):
        return self._error_message




