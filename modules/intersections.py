class Intersections:
    def __init__(self, layer, index):
        self._layer = layer
        self._error_message = ''
        self._index = index
        self._intersections = {}
    
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

        feature_dict = {}
        for feature in features:
            self._index.insertFeature(feature)
            feature_dict[feature.id()] = feature

        for f1 in features:
            g1 = f1.geometry()
            p11, p12 = self.get_endpoints(g1)

            candidate_ids = self._index.intersects(g1.boundingBox())
            for candidate_id in candidate_ids:
                if candidate_id == f1.id():
                    continue

                f2 = feature_dict[candidate_id]
                g2 = f2.geometry()

                if g1.intersects(g2):
                    p21, p22 = self.get_endpoints(g2)
                    if p11 != p21 and p11 != p22 and p12 != p21 and p12 != p22:
                        if f2.id() not in self._intersections or self._intersections[f2.id()] != f1.id():
                            self._intersections[f1.id()] = f2.id()
                            self._error_message += f'error: intersection between feature {f1.id()} and feature {f2.id()}\n'

    def getErrorMessage(self):
        return self._error_message




