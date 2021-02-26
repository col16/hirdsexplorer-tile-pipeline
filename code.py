import numpy as np
import rasterio

# Convert tiff with 1 channel of 32-bit floats to a file with 3 channels of
# 8-bit integers
with rasterio.open('hirds_rainfalldepth_duration24.0_ARI100.0.tif') as src:
    floats = src.read(1)
    floats[floats==src.nodata]=0 # replace 'nodata' value with zero, as all
        # depths will be greater than zero
    print("Max",floats.max())
    print("Min",np.min(floats[np.nonzero(floats)]))

    #Taken from https://gis.stackexchange.com/a/272805
    zeros = np.zeros(floats.shape)
    mask = floats != 0
    r = np.where(mask, np.floor_divide((100000 + floats * 10), 65536), zeros)
    g = np.where(mask, np.floor_divide((100000 + floats * 10), 256) - r * 256, zeros)
    b = np.where(mask, np.floor(100000 + floats * 10) - r * 65536 - g * 256, zeros)

    """
    treated_as_ints = np.zeros((3, floats.shape[1], floats.shape[2]))
    for channel in floats:
        for i, row in enumerate(channel):
            for j, cell in enumerate(row):
                if cell == 0:
                    v = 0
                else:
                    v = int(round(cell*100,0))
                    v += 10000
                a,b,c = np.frombuffer(
                    v.to_bytes(3, byteorder="big", signed=False),
                    dtype=np.uint8)
                treated_as_ints[0][i][j] = a
                treated_as_ints[1][i][j] = b
                treated_as_ints[2][i][j] = c """

    # Write to a new 3-channel 8-bit file.
    profile = src.profile
    profile.update(dtype=rasterio.uint8, count=3, compress='lzw', nodata=0)
    with rasterio.open('example.tif', 'w', **profile) as dst:
        #dst.write(treated_as_ints.astype(rasterio.uint8))
        dst.write_band(1, r.astype(rasterio.uint8))
        dst.write_band(2, g.astype(rasterio.uint8))
        dst.write_band(3, b.astype(rasterio.uint8))
