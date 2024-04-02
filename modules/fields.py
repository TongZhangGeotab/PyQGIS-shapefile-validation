class Fields:
    def __init__(self, layer):
        self._layer = layer
        self._fields = []
        self._error_message = ''
        self._mandatory_fields = {
            'group': False,
            'route': False,
            'segment': False,
        }
        self._optional_fields = {
            'roadwidth': False,
            'passcount': False,
        }
    
    def parseFieldNames(self):
        self._fields = [field.name() for field in self._layer.fields()]
        for field in self._fields:
            if field.lower() in self._mandatory_fields:
                self._mandatory_fields[field.lower()] = field
            if field.lower() in self._optional_fields:
                self._optional_fields[field.lower()] = field

    def checkMandatoryColumn(self, fieldName):
        if not self._mandatory_fields[fieldName]:
            self._error_message += f'error: {fieldName} column is missing\n'
        else:
            entries = [(feature[self._mandatory_fields[fieldName]], feature.id()) for feature in self._layer.getFeatures()]
            for entry, id in entries:
                if entry is None:
                    self._error_message += f'error: feature {id} has Null {fieldName} value\n'
            return True, entries
        return False, None

    def checkOptionalColumn(self, fieldName, type):
        if not self._optional_fields[fieldName]:
            self._error_message += f'warning: {fieldName} column is unpopulated, using defaults\n'
        else:
            data_type = self._layer.fields().field(self._optional_fields[fieldName]).typeName()
            if type not in data_type.lower():
                self._error_message += f'error: {fieldName} datatype is {data_type} not {type}\n'

            entries = [(feature[self._optional_fields[fieldName]], feature.id()) for feature in self._layer.getFeatures()]
            for entry, id in entries:
                if entry <= 0:
                    self._error_message += f'error: feature {id} has non positive {fieldName} value\n'

    def run(self):
        self.parseFieldNames()
        self.checkMandatoryColumn('group')
        self.checkMandatoryColumn('route')

        result, segments = self.checkMandatoryColumn('segment')
        if result:
            segment_set = {}
            for segment, id in segments:
                if segment in segment_set:
                    segment_set[segment].append(id)
                else:
                    segment_set[segment] = [id]

        for segment in segment_set:
            if len(segment_set[segment]) > 1:
                    self._error_message += f'error: duplicated segment name {segment} for features {segment_set[segment]}\n'


        self.checkOptionalColumn('roadwidth', 'int')
        self.checkOptionalColumn('passcount', 'int')

    def getErrorMessage(self):
        return self._error_message