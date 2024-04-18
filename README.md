# PyQGIS shapefile validation

This is an automated shapefile validation tool made using PyQGIS. This script attempts to discover potential errors as outlined in the [Public Works: Route Shapefile Validation (Partner Guide) \[PUB\]](https://docs.google.com/document/d/1PRAwFHVcfzmP5Um6crQzm4FY151ZIkIZxw5yzwEOYb4/edit).

To use the tool, follow the instructions found here [Public Works: Automated Shapefile Validation Tool Guide \[INT\]](https://docs.google.com/document/d/1x0yHLW9mKt6qri7pfTKhIuaByhpvh5tnQLEn1H7roMA/edit).

## Development notes

### Architecture 

The `main.py` script imports and runs all the checkers in `modules` to get the appropriate feedback message.

Each checker is a class, it must contain the `run()` function and the `getFeedback()` function, both of which should take `self` as the only argument.

The logger is used to log issues and warnings with the shapefile to both the console and a log file (the name of the log file is always the timestamp of when the script is run). The logging convention currently used is to log the number of problematic feature at a `ERROR` or `WARNING` level, and log the actual feature IDs at a `INFO` level. The logger is configured to log only `WARNING` or `ERROR` to the console, and all messages to the log file. This effectively means the console output will be a summary while the log file contains all the details. Note that the feature IDs are all logged in 1 log message - logging them 1 at a time creates too many log messages and slows down the system (and potentially crashes QGIS).

### QGIS API

In the QGIS IDE, only the script being run can access the QGIS API - this means that all imported modules (the checkers) cannot use the QGIS API. The current workaround is to intialize all QGIS objects in `main.py` and pass them to the modules. The utility scripts are run in the environment, so may use the QGIS API.

It is possible to set up a PyQGIS environment outside of the QGIS IDE, though it has not been successfully tested yet.

PyQGIS has an official Docker image - this could be a better way of running the script if a GUI is not required, this is the link to the [GitHub repository](https://github.com/qgis/pyqgis/blob/master/Dockerfile). This method has not been tested yet.
