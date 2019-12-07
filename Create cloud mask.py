# This will generate cloud masks using the s2cloudless package.

import sentile
import matplotlib.pyplot as plt
import numpy as np
import pickle
from s2cloudless import S2PixelCloudDetector

cloud_detector = S2PixelCloudDetector(threshold=0.97, average_over=4, dilation_size=2)

#Create tiles list
tiles = [[5120, 3584],
         [5120, 4096],
         [5632, 4096],
         [6144, 4096],
         [6656, 4096],
         [7168, 4096],
         [4608, 4608],
         [5120, 4608],
         [5632, 4608],
         [6144, 4608],
         [6656, 4608],
         [7168, 4608],
         [7680, 5632],
         [4608, 5120],
         [5120, 5120],
         [5632, 5120],
         [6144, 5120],
         [6656, 5120],
         [7168, 5120],
         [7680, 5120],
         [4608, 5632],
         [5120, 5632],
         [5632, 5632],
         [6144, 5632],
         [6656, 5632],
         [7168, 5632],
         [4608, 6144],
         [5120, 6144],
         [5632, 6144],
         [6144, 6144],
         [6656, 6144],
         [5120, 6656],
         [5632, 6656],
         [6144, 6656],
         [6656, 6656],
         [7168, 6656],
         [5120, 7168],
         [5632, 7168],
         [6144, 7168],
         [6656, 7168],
         [7168, 7168],
         [5632, 7680],
         [6144, 7680],
         [6656, 7680],
         [5632, 8192],
         [6144, 8192],
         [6656, 8192],
         [5632, 8704],
         [6144, 8704],
         [6656, 8704],
         [6144, 9216],
         [6656, 9216],
         [6144, 9728],
         [6656, 9728],
         [6656, 10240]]

i = 0

dates_master = 0
ndvi_master = list()

for tile in tiles:
    tile_x = tile[0]
    tile_y = tile[1]
    my_sentile = sentile.SenTile(tile_x, tile_y)

    dates = my_sentile.get_timeseries_image_dates()
    dates_master = dates
    i = i + 1
    print(f"Processing tile: {tile_x},{tile_y} - {i} of {len(tiles)}")
    print(dates)
    #print(my_sentile.get_mean_ndvi_timeseries())
    ndvi_master.append(my_sentile.get_mean_ndvi_timeseries())

    #Create cloud masks images and save it in cloudmasks folder
    # for date in dates:
    #     image_arr = my_sentile.get_image_as_array(date)
    #     myts_list = list()
    #     myts_list.append(image_arr)
    #     cloud_masks = cloud_detector.get_cloud_masks(np.array(myts_list))
    #     plt.imsave(f"datap2/cloudmasks/cloudmask-x{tile_x}-y{tile_y}-{date}.png", cloud_masks[0], vmin=0, vmax=1, cmap=plt.get_cmap("binary"))


    for date in dates:
        with open('ndvi_master.data', 'wb') as filehandle:
            #store the data as binary data stream
            pickle.dump(ndvi_master, filehandle)

        with open('tiles.data', 'wb') as filehandle:
            # store the data as binary data stream
            pickle.dump(tiles, filehandle)

        with open('dates.data', 'wb') as filehandle:
            # store the data as binary data stream
            pickle.dump(dates_master, filehandle)