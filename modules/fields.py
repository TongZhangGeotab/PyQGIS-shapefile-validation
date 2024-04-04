"""
Class for checking attribute table
"""

import logging


class Fields:
    """
    Checks attribute table fields
    """

    def __init__(self, layer):
        """
        Constructor
        """
        self._layer = layer
        self._logger = logging.getLogger("QGIS_logger")

        # Track if errors exist and the feedback message for each error
        self._header_syntax_error = False
        self._header_syntax_message = "\nThe attribute column heading does not match the required formatting. The column header syntax is character-sensitive. If the characters do not match the required format, the upload to MyGeotab will fail. Please adjust the data columns to match the formatting guidelines outlined in the Adding Required Route Completion Attributes section of the Route Completion configuration with a Shapefile [PUBLIC] document.\n"
        self._null_error = False
        self._null_message = "\nPlease ensure there is no missing or incomplete data for the group, route, or segment column. If a feature contains a NULL value or the record is missing, the file upload to MyGeotab will fail. Ensure that every feature has a valid attribute for each column header.\n"
        self._duplicate_segment_error = False
        self._duplicate_segment_message = "\nRoutes are made up of segments and must have a unique attribute to upload the file to MyGeotab. Please adjust the values to align with this requirement. There are many segment-naming options. The most common option is combining the street name with a unique identifier (an object ID or row number). For example, the segment name for the field calculator expression may be written as “Street Name + Object ID” to create a unique attribute.\n"
        self._type_or_value_error = False
        self._type_or_value_message = "\nAll values for the roadWidth and passCount field categories must be inputted in meters as integers without any decimals. If you are converting from feet to meters, round up or down to the nearest whole number. The value must be greater than 0 to be valid.\n"

        # Track the names of fields based with lowercase name as key
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
        fields = [field.name() for field in self._layer.fields()]
        for field in fields:
            # If lowercase name matches a key, assign that key's value to be the name
            lower_case_name = field.lower()

            if lower_case_name in self._mandatory_fields:
                self._mandatory_fields[lower_case_name] = field

            if lower_case_name in self._optional_fields:
                self._optional_fields[lower_case_name] = field

    def checkMandatoryColumn(self, fieldName):
        """
        Check a mandatory column for missing values and returns list of entries in that column
        """
        # Log an error if a mandatory field does not exist
        if not self._mandatory_fields[fieldName]:
            self._header_syntax_error = True
            self._logger.error(f"{fieldName} column is missing")
            return False, None

        entries = [
            (feature[self._mandatory_fields[fieldName]], feature.id())
            for feature in self._layer.getFeatures()
        ]

        # Log an error if a value is Null
        for entry, id in entries:
            if entry is None:
                self._null_error = True
                self._logger.error(f"feature {id} has Null {fieldName} value")

        return True, entries

    def checkOptionalColumn(self, column, type):
        """
        Check an optional column for data type and invalid values
        """
        # Log an info statement if the optional field does not exist
        if not self._optional_fields[column]:
            self._logger.info(f"{column} is unpopulated, using defaults")
            return False, None

        data_type = self._layer.fields().field(self._optional_fields[column]).typeName()

        # Check if data type name contains type we want - for cases like int8, int16, etc. names
        if type not in data_type.lower():
            self._type_or_value_error = True
            self._logger.error(f"{column} datatype is {data_type} not {type}")

        # Check if any of the entires have invalid values
        entries = [
            (feature[self._optional_fields[column]], feature.id())
            for feature in self._layer.getFeatures()
        ]
        for entry, id in entries:
            if entry <= 0:
                self._type_or_value_error = True
                self._logger.error(f"feature {id} has non positive {column} value")

        return True, entries

    def check_segment_names(self, segments):
        """
        Checks if there are any segments that have the same name
        """
        # Make dict of segment names and associated id(s)
        segment_set = {}
        for segment, id in segments:
            if segment in segment_set:
                segment_set[segment].append(id)
            else:
                segment_set[segment] = [id]

        # Loop through segments and log an error for all segments with multiple associated ids
        for segment in segment_set:
            if len(segment_set[segment]) > 1:
                self._duplicate_segment_error = True
                self._logger.error(f"features {segment_set[segment]} share segment name {segment}")

    def run(self):
        """
        Determine all errors and warnings in the attribute table
        """
        self.parseFieldNames()

        # Check existance of mandatory fields
        self.checkMandatoryColumn("group")
        self.checkMandatoryColumn("route")

        result, segments = self.checkMandatoryColumn("segment")
        if result:
            # Check for duplicate segment names
            self.check_segment_names(segments)

        self.checkOptionalColumn("roadwidth", "int")
        self.checkOptionalColumn("passcount", "int")

    def getFeedback(self):
        """
        Generate and return the feedback message
        """
        feedback_message = ""
        if self._header_syntax_error:
            feedback_message += self._header_syntax_message
        if self._null_error:
            feedback_message += self._null_message
        if self._duplicate_segment_error:
            feedback_message += self._duplicate_segment_message
        if self._type_or_value_error:
            feedback_message += self._type_or_value_message
        if feedback_message:
            return True, feedback_message

        return False, None
