class Coordinates:
    def __init__(self, layer, instance):
        self._layer = layer
        self._instance = instance
        self._crs_error = False
        self._crs_message = "\nThe routes uploaded to MyGeotab must use the WGS 84 - EPSG: 4326 coordinate reference system. Other versions of WGS 84 will not work nor will a local CRS. On QGIS or another GIS software, use a Reproject Layer or Assign Projection tool to change the shapefile from an existing coordinate reference system to a new coordinate reference system.\n"
        self._coord_error = False
        self._coord_message = "\nThe shapefile coordinates are formatted incorrectly. This may have resulted if the shapefile was exported to WGS 84 - EPSG: 4326 without being appropriately re-projected or re-assigned from the original CRS. To resolve this issue, reassign the shapefile’s original CRS to it, and then run a ’Reproject Layer CRS’ or ‘Assign Coordinate System to Layer’ tool in the GIS software to properly convert to the correct CRS. Once complete, the GIS team can export the shapefile, and attempt the file upload again.\n"

    def run(self):
        crs_id = self._instance.crs().authid()
        if crs_id !=  "EPSG:4326":
            self._crs_error = True
        
        extents = self._layer.extent()    
        if (extents.xMinimum() < -180 or extents.xMaximum() > 180 or
            extents.yMinimum() < -90 or extents.yMaximum() > 90):
            self._coord_error = True

    def getFeedback(self):
        feedback_message = ""
        if self._crs_error:
            feedback_message += self._crs_message
        if self._coord_error:
            feedback_message += self._coord_message

        if feedback_message:
            return True, feedback_message

        return False, None