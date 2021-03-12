This code generates the tiles plotted on the [hirdsexplorer.nz](https://hirdsexplorer.nz/) website (see repo at [https://github.com/col16/hirdsexplorer](https://github.com/col16/hirdsexplorer)).

Dependancies are Python 3, [gdal2tiles](https://gdal.org/programs/gdal2tiles.html) and those listed in [requirements.txt](requirements.txt).

To use, download geotiff files from [the NIWA website](https://data-niwa.opendata.arcgis.com/datasets/edcbe0a99d7f4df59501ba55973648f5) using ArcGIS Pro or ArcMap, and save these files to a folder called 'Original data'.

Then run `python convert_2km_geotiffs_to_tiles.py`
