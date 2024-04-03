"""
Class for checking attribute table
"""

import itertools


class Fields:
    """
    Checks attribute table fields
    """

    def __init__(self, layer):
        """
        Constructor
        """
        self._layer = layer
        self._fields = []
        self._error_message = ""
        self._mandatory_fields = {
            "group": False,
            "route": False,
            "segment": False,
        }
        self._optional_fields = {
            "roadwidth": False,
            "passcount": False,
        }

    def parseFieldNames(self):
        """
        Finds and stores the name of mandatory and optional column headers
        """
        self._fields = [field.name() for field in self._layer.fields()]
        for field in self._fields:
            if field.lower() in self._mandatory_fields:
                self._mandatory_fields[field.lower()] = field
            if field.lower() in self._optional_fields:
                self._optional_fields[field.lower()] = field

    def checkMandatoryColumn(self, fieldName):
        """
        Check a mandatory column for missing values and returns list of entries in that column
        """
        if not self._mandatory_fields[fieldName]:
            self._error_message += f"error: {fieldName} column is missing\n"
        else:
            entries = [
                (feature[self._mandatory_fields[fieldName]], feature.id())
                for feature in self._layer.getFeatures()
            ]
            for entry, id in entries:
                if entry is None:
                    self._error_message += f"error: feature {id} has Null {fieldName} value\n"
            return True, entries
        return False, None

    def checkOptionalColumn(self, column, type):
        """
        Check an optional column for data type and invalid values
        """
        if not self._optional_fields[column]:
            self._error_message += f"warning: {column} column is unpopulated, using defaults\n"
        else:
            data_type = self._layer.fields().field(self._optional_fields[column]).typeName()
            # Check if data type name contains type we want - for cases like int8, int16, etc. names
            if type not in data_type.lower():
                self._error_message += f"error: {column} datatype is {data_type} not {type}\n"

            # Check if any of the entires have invalid values
            entries = [
                (feature[self._optional_fields[column]], feature.id())
                for feature in self._layer.getFeatures()
            ]
            for entry, id in entries:
                if entry <= 0:
                    self._error_message += f"error: feature {id} has non positive {column} value\n"

    def run(self):
        """
        Determine all errors and warnings in the attribute table
        """
        self.parseFieldNames()
        self.checkMandatoryColumn("group")
        self.checkMandatoryColumn("route")

        # Check for duplicate segment names
        result, segments = self.checkMandatoryColumn("segment")
        if result:
            segment_set = {}
            # Make dict of segment names and associate id(s)
            for segment, id in segments:
                if segment in segment_set:
                    segment_set[segment].append(id)
                else:
                    segment_set[segment] = [id]

            for segment in segment_set:
                # If any segment has 2 or more associated ids, check if they are duplicated names
                if len(segment_set[segment]) > 1:
                    self._error_message += f"error: features {segment_set[segment]} share segment name {segment}\n"

        self.checkOptionalColumn("roadwidth", "int")
        self.checkOptionalColumn("passcount", "int")

    def getErrorMessage(self):
        """
        Return the error message
        """
        return self._error_message
