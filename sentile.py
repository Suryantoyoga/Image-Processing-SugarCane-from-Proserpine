from PIL import Image
import glob
import os
import numpy as np

os.getcwd()

# The expected value of a Pixel in a mask file indicating that the pixel is
# within that region.  Tuple value, (Red, Green, Blue, Alpha)
IS_IN_MASK_PIXEL_VALUE = (0, 0, 0, 255)
IS_IN_CLOUD_MASK_PIXEL_VALUE = (0, 0, 0, 255)

# Tile width / height in pixels
TILE_WIDTH_PX = 512
TILE_HEIGHT_PX = 512

# Path to the data folder
DATA_PATH = "./datap2"


# Open an image file and get all the pixels
def get_tile_pixels(tile_path):
    img = Image.open(tile_path)
    pixels = img.load()
    return pixels

# mask  color validation
def is_in_mask(mask_pixels, pixel_x, pixel_y):
    if mask_pixels[pixel_y, pixel_x] == IS_IN_MASK_PIXEL_VALUE:
        return True
    else:
        return False

# cloud mask validation
def is_in_cloud_mask(cloud_mask_pixels, pixel_x, pixel_y):
    if cloud_mask_pixels[pixel_y, pixel_x] == IS_IN_CLOUD_MASK_PIXEL_VALUE:
        return True
    else:
        return False


def mask_tile(mask_pixels, tile_pixels):
    for y in range(TILE_HEIGHT_PX):
        for x in range(TILE_WIDTH_PX):
            in_mask = is_in_mask(mask_pixels, x, y)
            if not in_mask:
                tile_pixels[y, x] = IS_IN_MASK_PIXEL_VALUE
    return tile_pixels


class SenTile:
    def __init__(self, tile_x, tile_y):
        self.tile_x = tile_x
        self.tile_y = tile_y

    # Get the physical path to the PNG image containing the current sugarcane area mask file
    def get_mask_path(self):
        path = f"{DATA_PATH}/masks/mask-x{self.tile_x}-y{self.tile_y}.png"
        return path

    # Get the physical path to the PNG image containing the cloud mask file
    def get_cloud_mask_path(self, date):
        path = f"{DATA_PATH}/cloudmasks/cloudmask-x{self.tile_x}-y{self.tile_y}-{date}.png"
        return path

    # Get the pixels for the current sugarcane area mask image file
    def get_mask_pixels(self):
        mask_path = self.get_mask_path()
        return get_tile_pixels(mask_path)

    # Get the pixels for the cloud mask image file
    def get_cloud_mask_pixels(self, date):
        cloud_mask_path = self.get_cloud_mask_path(date)
        return get_tile_pixels(cloud_mask_path)

    # Get a binary ndarray for the current sugarcane area mask image file
    def get_binary_mask(self):
        binary_mask = np.zeros((TILE_HEIGHT_PX, TILE_WIDTH_PX))
        mask_pixels = self.get_mask_pixels()
        for x in range(TILE_WIDTH_PX):
            for y in range(TILE_HEIGHT_PX):
                in_mask = is_in_mask(mask_pixels, x, y)
                if in_mask:
                    binary_mask[x, y] = 1
        return binary_mask

    # Get a binary ndarray for the cloud mask image file
    def get_binary_cloud_mask(self, date):
        binary_mask = np.zeros((TILE_HEIGHT_PX, TILE_WIDTH_PX))
        mask_pixels = self.get_cloud_mask_pixels(date)
        for x in range(TILE_WIDTH_PX):
            for y in range(TILE_HEIGHT_PX):
                in_mask = not is_in_cloud_mask(mask_pixels, x, y)
                if in_mask:
                    binary_mask[x, y] = 1
        return binary_mask

    # Get a list of all the image tiles for the specified band
    def get_timeseries_image_paths(self, band):
        path = f"{DATA_PATH}/sugarcanetiles/{self.tile_x}-{self.tile_y}-{band}*.png"
        images = glob.glob(path)
        return images

    # Get the path of the image tile for the specified band and date
    def get_timeseries_image_path(self, band, date):
        path = f"{DATA_PATH}/sugarcanetiles/{self.tile_x}-{self.tile_y}-{band}-{date}.png"
        return path

    # Get a list of all dates in the time series
    def get_timeseries_image_dates(self):
        dates = list()
        paths = self.get_timeseries_image_paths("B01")
        for p in paths:
            # date = os.path.basename(p)[15:25]
            file_name = os.path.basename(p)
            file_name_length = len(file_name)
            date = file_name[(file_name_length - 14):file_name_length - 4]
            dates.append(date)
        return dates

    # Get a matrix with the NDVI for a specific date
    def get_ndvi_matrix(self, date):
        nir = self.get_timeseries_image_path("B08", date)
        red = self.get_timeseries_image_path("B04", date)

        nir_pixels = get_tile_pixels(nir)
        red_pixels = get_tile_pixels(red)

        ndvi_matrix = np.zeros((TILE_WIDTH_PX, TILE_HEIGHT_PX))

        for y in range(TILE_HEIGHT_PX):
            for x in range(TILE_WIDTH_PX):
                # NDVI = (NIR - RED) / (NIR + RED)
                ndvi_matrix[x][y] = (nir_pixels[y, x] - red_pixels[y, x]) / (nir_pixels[y, x] + red_pixels[y, x])
        return ndvi_matrix

    # Get a list of matrices with the NDVI for the time series
    def get_ndvi_matrices(self):
        dates = self.get_timeseries_image_dates()
        ndvi_matrix_list = list()
        for date in dates:
            ndvi_matrix = self.get_ndvi_matrix(date)
            ndvi_matrix_list.append(ndvi_matrix)
        return ndvi_matrix_list

    def get_mean_ndvi_timeseries(self):
        # This is not very efficient...
        dates = self.get_timeseries_image_dates()

        # result[0] is the date
        # result[1] is the mean ndvi
        # result[3] is the number of unmasked pixels
        result = list()
        mask_pixels = self.get_mask_pixels()
        for date in dates:
            cloud_mask_pixels = self.get_cloud_mask_pixels(date)
            unmasked_pixel_value = list()
            ndvi_matrix = self.get_ndvi_matrix(date)
            for y in range(TILE_HEIGHT_PX):
                for x in range(TILE_WIDTH_PX):
                    in_mask = is_in_mask(mask_pixels, x, y)
                    in_cloud_mask = is_in_cloud_mask(cloud_mask_pixels, x, y)
                    if (not in_mask) & (not in_cloud_mask):
                        unmasked_pixel_value.append(ndvi_matrix[x, y])
            if len(unmasked_pixel_value) > 0:
                row = [date, np.mean(unmasked_pixel_value), len(unmasked_pixel_value)]
            else:
                row = [date, -99, 0]
            result.append(row)
        return result

    # Choose the image band and organize as array
    def get_image_as_array(self, date):
        layers = ["B01", "B02", "B04", "B05", "B08", "B8A", "B09", "B10", "B11", "B12"]
        images = np.empty([512, 512, 10])
        for idx in range(10):
            path = self.get_timeseries_image_path(layers[idx], date)
            img = Image.open(path)
            images[:, :, idx] = (np.array(img) / 10000)
        return images

    def get_timeseries_as_array(self):
        dates = self.get_timeseries_image_dates()
        image_list = list()
        for date in dates:
            image = self.get_image_as_array(date)
            image_list.append(image)
        return np.array(image_list)

    # Returns whether the tile overlaps a current sugarcane growing area
    # based on the provided mask.
    # TRUE : the tile overlaps a current sugarcane growing area
    # FALSE : the tiles does not overlap a current sugarcane growing area
    def get_sugarcane_growing_status(self):
        # Check the mask exists
        does_exist = os.path.exists(self.get_mask_path())
        if not does_exist:
            return False

        mask_pixels = self.get_mask_pixels()
        for y in range(TILE_HEIGHT_PX):
            for x in range(TILE_WIDTH_PX):
                in_mask = is_in_mask(mask_pixels, x, y)
                if in_mask:
                    return True
        return False