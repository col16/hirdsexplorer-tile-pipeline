import numpy as np
import rasterio

# Convert tiff with 1 channel of 32-bit floats to a file with 4 channels of
# 8-bit integers
with rasterio.open('hirds_rainfalldepth_duration24.0_ARI100.0.tif') as src:
    floats = src.read()
    floats[floats==src.nodata]=0 # replace 'nodata' value with zero, as all
        # depths will be greater than zero

    treated_as_ints = np.zeros((4, floats.shape[1], floats.shape[2]))
    for channel in floats:
        for i, row in enumerate(channel):
            for j, cell in enumerate(row):
                #cell.tobytes()
                a,b,c,d = np.frombuffer(cell, dtype=np.uint8)
                treated_as_ints[0][i][j] = a
                treated_as_ints[1][i][j] = b
                treated_as_ints[2][i][j] = c
                treated_as_ints[3][i][j] = d

    # Write to a new 4-channel 8-bit file.
    profile = src.profile
    profile.update(dtype=rasterio.uint8, count=4, compress='lzw', nodata=0)
    with rasterio.open('example.tif', 'w', **profile) as dst:
        dst.write(treated_as_ints.astype(rasterio.uint8))
