import numpy as np
import rasterio
import re
import os
from pathlib import Path
import csv
import traceback

output_type = 'dem' #either 'dem' or 'float32'
# 'dem' output is run through gdal2tiles process to create tiles, but this is
# not done with 'float32' output as gdal2tiles ignores anything more than the
# first three channels

input_folder = 'Original data'

input_files = [
    'hirds_rainfalldepth_duration0.5_ARI1.58.tif',
    'hirds_rainfalldepth_duration0.5_ARI2.0.tif',
    'hirds_rainfalldepth_duration0.5_ARI5.0.tif',
    'hirds_rainfalldepth_duration0.5_ARI10.0.tif',
    'hirds_rainfalldepth_duration0.5_ARI20.0.tif',
    'hirds_rainfalldepth_duration0.5_ARI30.0.tif',
    'hirds_rainfalldepth_duration0.5_ARI40.0.tif',
    'hirds_rainfalldepth_duration0.5_ARI50.0.tif',
    'hirds_rainfalldepth_duration0.5_ARI60.0.tif',
    'hirds_rainfalldepth_duration0.5_ARI80.0.tif',
    'hirds_rainfalldepth_duration0.5_ARI100.0.tif',
    'hirds_rainfalldepth_duration0.5_ARI250.0.tif',
    'hirds_rainfalldepth_duration0.166667_ARI1.58.tif',
    'hirds_rainfalldepth_duration0.166667_ARI2.0.tif',
    'hirds_rainfalldepth_duration0.166667_ARI5.0.tif',
    'hirds_rainfalldepth_duration0.166667_ARI10.0.tif',
    'hirds_rainfalldepth_duration0.166667_ARI20.0.tif',
    'hirds_rainfalldepth_duration0.166667_ARI30.0.tif',
    'hirds_rainfalldepth_duration0.166667_ARI40.0.tif',
    'hirds_rainfalldepth_duration0.166667_ARI50.0.tif',
    'hirds_rainfalldepth_duration0.166667_ARI60.0.tif',
    'hirds_rainfalldepth_duration0.166667_ARI80.0.tif',
    'hirds_rainfalldepth_duration0.166667_ARI100.0.tif',
    'hirds_rainfalldepth_duration0.166667_ARI250.0.tif',
    'hirds_rainfalldepth_duration0.333333_ARI1.58.tif',
    'hirds_rainfalldepth_duration0.333333_ARI2.0.tif',
    'hirds_rainfalldepth_duration0.333333_ARI5.0.tif',
    'hirds_rainfalldepth_duration0.333333_ARI10.0.tif',
    'hirds_rainfalldepth_duration0.333333_ARI20.0.tif',
    'hirds_rainfalldepth_duration0.333333_ARI30.0.tif',
    'hirds_rainfalldepth_duration0.333333_ARI40.0.tif',
    'hirds_rainfalldepth_duration0.333333_ARI50.0.tif',
    'hirds_rainfalldepth_duration0.333333_ARI60.0.tif',
    'hirds_rainfalldepth_duration0.333333_ARI80.0.tif',
    'hirds_rainfalldepth_duration0.333333_ARI100.0.tif',
    'hirds_rainfalldepth_duration0.333333_ARI250.0.tif',
    'hirds_rainfalldepth_duration1.0_ARI1.58.tif',
    'hirds_rainfalldepth_duration1.0_ARI2.0.tif',
    'hirds_rainfalldepth_duration1.0_ARI5.0.tif',
    'hirds_rainfalldepth_duration1.0_ARI10.0.tif',
    'hirds_rainfalldepth_duration1.0_ARI20.0.tif',
    'hirds_rainfalldepth_duration1.0_ARI30.0.tif',
    'hirds_rainfalldepth_duration1.0_ARI40.0.tif',
    'hirds_rainfalldepth_duration1.0_ARI50.0.tif',
    'hirds_rainfalldepth_duration1.0_ARI60.0.tif',
    'hirds_rainfalldepth_duration1.0_ARI80.0.tif',
    'hirds_rainfalldepth_duration1.0_ARI100.0.tif',
    'hirds_rainfalldepth_duration1.0_ARI250.0.tif',
    'hirds_rainfalldepth_duration2.0_ARI1.58.tif',
    'hirds_rainfalldepth_duration2.0_ARI2.0.tif',
    'hirds_rainfalldepth_duration2.0_ARI5.0.tif',
    'hirds_rainfalldepth_duration2.0_ARI10.0.tif',
    'hirds_rainfalldepth_duration2.0_ARI20.0.tif',
    'hirds_rainfalldepth_duration2.0_ARI30.0.tif',
    'hirds_rainfalldepth_duration2.0_ARI40.0.tif',
    'hirds_rainfalldepth_duration2.0_ARI50.0.tif',
    'hirds_rainfalldepth_duration2.0_ARI60.0.tif',
    'hirds_rainfalldepth_duration2.0_ARI80.0.tif',
    'hirds_rainfalldepth_duration2.0_ARI100.0.tif',
    'hirds_rainfalldepth_duration2.0_ARI250.0.tif',
    'hirds_rainfalldepth_duration6.0_ARI1.58.tif',
    'hirds_rainfalldepth_duration6.0_ARI2.0.tif',
    'hirds_rainfalldepth_duration6.0_ARI5.0.tif',
    'hirds_rainfalldepth_duration6.0_ARI10.0.tif',
    'hirds_rainfalldepth_duration6.0_ARI20.0.tif',
    'hirds_rainfalldepth_duration6.0_ARI30.0.tif',
    'hirds_rainfalldepth_duration6.0_ARI40.0.tif',
    'hirds_rainfalldepth_duration6.0_ARI50.0.tif',
    'hirds_rainfalldepth_duration6.0_ARI60.0.tif',
    'hirds_rainfalldepth_duration6.0_ARI80.0.tif',
    'hirds_rainfalldepth_duration6.0_ARI100.0.tif',
    'hirds_rainfalldepth_duration6.0_ARI250.0.tif',
    'hirds_rainfalldepth_duration12.0_ARI1.58.tif',
    'hirds_rainfalldepth_duration12.0_ARI2.0.tif',
    'hirds_rainfalldepth_duration12.0_ARI5.0.tif',
    'hirds_rainfalldepth_duration12.0_ARI10.0.tif',
    'hirds_rainfalldepth_duration12.0_ARI20.0.tif',
    'hirds_rainfalldepth_duration12.0_ARI30.0.tif',
    'hirds_rainfalldepth_duration12.0_ARI40.0.tif',
    'hirds_rainfalldepth_duration12.0_ARI50.0.tif',
    'hirds_rainfalldepth_duration12.0_ARI60.0.tif',
    'hirds_rainfalldepth_duration12.0_ARI80.0.tif',
    'hirds_rainfalldepth_duration12.0_ARI100.0.tif',
    'hirds_rainfalldepth_duration12.0_ARI250.0.tif',
    'hirds_rainfalldepth_duration24.0_ARI1.58.tif',
    'hirds_rainfalldepth_duration24.0_ARI2.0.tif',
    'hirds_rainfalldepth_duration24.0_ARI5.0.tif',
    'hirds_rainfalldepth_duration24.0_ARI10.0.tif',
    'hirds_rainfalldepth_duration24.0_ARI20.0.tif',
    'hirds_rainfalldepth_duration24.0_ARI30.0.tif',
    'hirds_rainfalldepth_duration24.0_ARI40.0.tif',
    'hirds_rainfalldepth_duration24.0_ARI50.0.tif',
    'hirds_rainfalldepth_duration24.0_ARI60.0.tif',
    'hirds_rainfalldepth_duration24.0_ARI80.0.tif',
    'hirds_rainfalldepth_duration24.0_ARI100.0.tif',
    'hirds_rainfalldepth_duration24.0_ARI250.0.tif',
    'hirds_rainfalldepth_duration48.0_ARI1.58.tif',
    'hirds_rainfalldepth_duration48.0_ARI2.0.tif',
    'hirds_rainfalldepth_duration48.0_ARI5.0.tif',
    'hirds_rainfalldepth_duration48.0_ARI10.0.tif',
    'hirds_rainfalldepth_duration48.0_ARI20.0.tif',
    'hirds_rainfalldepth_duration48.0_ARI30.0.tif',
    'hirds_rainfalldepth_duration48.0_ARI40.0.tif',
    'hirds_rainfalldepth_duration48.0_ARI50.0.tif',
    'hirds_rainfalldepth_duration48.0_ARI60.0.tif',
    'hirds_rainfalldepth_duration48.0_ARI80.0.tif',
    'hirds_rainfalldepth_duration48.0_ARI100.0.tif',
    'hirds_rainfalldepth_duration48.0_ARI250.0.tif',
    'hirds_rainfalldepth_duration72.0_ARI1.58.tif',
    'hirds_rainfalldepth_duration72.0_ARI2.0.tif',
    'hirds_rainfalldepth_duration72.0_ARI5.0.tif',
    'hirds_rainfalldepth_duration72.0_ARI10.0.tif',
    'hirds_rainfalldepth_duration72.0_ARI20.0.tif',
    'hirds_rainfalldepth_duration72.0_ARI30.0.tif',
    'hirds_rainfalldepth_duration72.0_ARI40.0.tif',
    'hirds_rainfalldepth_duration72.0_ARI50.0.tif',
    'hirds_rainfalldepth_duration72.0_ARI60.0.tif',
    'hirds_rainfalldepth_duration72.0_ARI80.0.tif',
    'hirds_rainfalldepth_duration72.0_ARI100.0.tif',
    'hirds_rainfalldepth_duration72.0_ARI250.0.tif',
    'hirds_rainfalldepth_duration96.0_ARI1.58.tif',
    'hirds_rainfalldepth_duration96.0_ARI2.0.tif',
    'hirds_rainfalldepth_duration96.0_ARI5.0.tif',
    'hirds_rainfalldepth_duration96.0_ARI10.0.tif',
    'hirds_rainfalldepth_duration96.0_ARI20.0.tif',
    'hirds_rainfalldepth_duration96.0_ARI30.0.tif',
    'hirds_rainfalldepth_duration96.0_ARI40.0.tif',
    'hirds_rainfalldepth_duration96.0_ARI50.0.tif',
    'hirds_rainfalldepth_duration96.0_ARI60.0.tif',
    'hirds_rainfalldepth_duration96.0_ARI80.0.tif',
    'hirds_rainfalldepth_duration96.0_ARI100.0.tif',
    'hirds_rainfalldepth_duration96.0_ARI250.0.tif',
    'hirds_rainfalldepth_duration120.0_ARI1.58.tif',
    'hirds_rainfalldepth_duration120.0_ARI2.0.tif',
    'hirds_rainfalldepth_duration120.0_ARI5.0.tif',
    'hirds_rainfalldepth_duration120.0_ARI10.0.tif',
    'hirds_rainfalldepth_duration120.0_ARI20.0.tif',
    'hirds_rainfalldepth_duration120.0_ARI30.0.tif',
    'hirds_rainfalldepth_duration120.0_ARI40.0.tif',
    'hirds_rainfalldepth_duration120.0_ARI50.0.tif',
    'hirds_rainfalldepth_duration120.0_ARI60.0.tif',
    'hirds_rainfalldepth_duration120.0_ARI80.0.tif',
    'hirds_rainfalldepth_duration120.0_ARI100.0.tif',
    'hirds_rainfalldepth_duration120.0_ARI250.0.tif',
]

filename_regex = re.compile(
    r'hirds_rainfalldepth_duration(?P<duration>\d+.\d+)_ARI(?P<ari>\d+.\d+).tif')


def convert(filename, output_folder):
    # Convert tiff with 1 channel of 32-bit floats to a file with 3 channels of
    # 8-bit integers
    try:
        with rasterio.open(os.path.join(input_folder,filename)) as src:
            floats = src.read(1)
            floats[floats==src.nodata]=0 # replace 'nodata' value with zero, as all
                # depths will be greater than zero
            max = floats.max()
            min = np.min(floats[np.nonzero(floats)])
            output_file = os.path.join(output_folder, 'dem_source_data.tif')

            if output_type == 'dem':
                #Taken from https://gis.stackexchange.com/a/272805
                #floats = floats*10
                zeros = np.zeros(floats.shape)
                mask = floats != 0
                r = np.where(mask, np.floor_divide((100000 + floats * 10), 65536), zeros)
                g = np.where(mask, np.floor_divide((100000 + floats * 10), 256) - r * 256, zeros)
                b = np.where(mask, np.floor(100000 + floats * 10) - r * 65536 - g * 256, zeros)

                # Write to a new 3-channel 8-bit file.
                profile = src.profile
                profile.update(dtype=rasterio.uint8, count=3, compress='lzw',
                    nodata=0)
                with rasterio.open(output_file, 'w', **profile) as dst:
                    dst.write_band(1, r.astype(rasterio.uint8))
                    dst.write_band(2, g.astype(rasterio.uint8))
                    dst.write_band(3, b.astype(rasterio.uint8))

                os.system("/usr/local/Cellar/python@3.9/3.9.1_8/bin/python3 "+\
                    "/usr/local/bin/gdal2tiles.py --xyz --resampling='near' "+\
                    "--webviewer='leaflet' --zoom='6' "+\
                    "--s_srs='EPSG:27200' '"+output_file+"' '"+output_folder+"'")

            elif output_type == 'float32':
                floats = np.full(floats.shape, 3.14, dtype="float32")
                bytes = floats.tobytes()
                treated_as_ints = np.reshape(
                    np.frombuffer(bytes, dtype=np.uint8),
                    (floats.shape[0], floats.shape[1], 4)
                )
                output_array = np.array([
                    treated_as_ints[:,:,0],
                    treated_as_ints[:,:,1],
                    treated_as_ints[:,:,2],
                    treated_as_ints[:,:,3],
                ])
                
                # Write to a new 4-channel 8-bit file.
                profile = src.profile
                profile.update(dtype=rasterio.uint8, count=4, compress='lzw',
                    nodata=0)
                with rasterio.open(output_file, 'w', **profile) as dst:
                    dst.write(output_array.astype(rasterio.uint8))

        return min, max
    except Exception as e:
        print(traceback.format_exc())
        return None, None


with open('min_max.csv', 'w', newline='') as minmax_file:
    minmax_writer = csv.writer(minmax_file)
    minmax_writer.writerow(['ARI (years)','Duration (hours)', 'Min depth (mm)',
        'Max depth (mm)'])

    for filename in input_files:
        print(filename)
        d = filename_regex.match(filename).groupdict()
        ari_folder = d['ari']+'yr'
        duration_folder = d['duration']+'hr'
        combined_folder = os.path.join('tiles',ari_folder,duration_folder)
        Path(combined_folder).mkdir(parents=True, exist_ok=True)
        min, max = convert(filename, combined_folder)
        minmax_writer.writerow([d['ari'],d['duration'],min,max])        
