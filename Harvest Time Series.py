from PIL import Image, ImageDraw
import glob
import os

'''
This function will count the masked images pixel based on the color and write it in new csv files
it will compare two images, if the latter image have cloud on it, it will use previous image pixel
this will reduce outlier created by the cloud 
'''

# Open an image file and get all the pixels
def get_tile_pixels(tile_path):
    img = Image.open(tile_path)
    pixels = img.load()
    return pixels

def get_cloudless_timeseries(tile_x, tile_y):
    f = open(f"data/cloudlesscsvharvested/timeseries-{tile_x}-{tile_y}.csv", "w+")
    f.write(f"Date,HarvestedPixelCountRed,HarvestedPixelCountBlue,HarvestedPixelCountGreen,Cloud,\n")
    arr = os.listdir(f"./data/harvested-{tile_x}-{tile_y}")
    for k in range(1, len(arr)):
        tile2 = Image.open(f"./data/harvested-{tile_x}-{tile_y}/" + arr[k])
        tile1 = Image.open(f"./data/harvested-{tile_x}-{tile_y}/" + arr[k - 1])
        date = os.path.basename(f"./data/harvested-{tile_x}-{tile_y}" + arr[k])[29:39]
        pixels2 = tile2.load()
        pixels1 = tile1.load()
        totalr = 0
        totalb = 0
        totalg = 0
        totaly = 0
        for y in range(512):
            for x in range(512):
                if pixels2[y, x] == (255,0,0):
                    totalr += 1
                elif pixels2[y,x] == (0, 0, 200):
                    totalb += 1
                elif pixels2[y,x] == (3,194,3):
                    totalg += 1
                elif pixels2[y,x] == (255,250,0):
                    pixels2[y,x] = pixels1 [y,x]
                    if pixels2[y, x] == (255, 0, 0):
                        totalr += 1
                    elif pixels2[y, x] == (0, 0, 200):
                        totalb += 1
                    elif pixels2[y, x] == (3, 194, 3):
                        totalg += 1
        f.write(f"{date},{totalr},{totalb},{totalg},{totaly}\n")
    f.close()

def get_real_cloudless_timeseries(tile_x, tile_y):
    f = open(f"data/cloudlesscsvrealharvested/realharvested-{tile_x}-{tile_y}.csv", "w+")
    f.write(f"Date,HarvestedPixelCount \n")
    arr = os.listdir(f"./data/harvested-{tile_x}-{tile_y}")
    for k in range (1, len(arr)):
        tile2 = Image.open(f"./data/harvested-{tile_x}-{tile_y}/" + arr[k])
        tile1 = Image.open(f"./data/harvested-{tile_x}-{tile_y}/" + arr[k - 1])
        date = os.path.basename(f"./data/harvested-{tile_x}-{tile_y}" + arr[k])[29:39]
        pixels2 = tile2.load()
        pixels1 = tile1.load()
        totalr = 0

        for y in range(512):
            for x in range(512):
                if pixels2[y,x] == (255, 250, 0):
                    pixels2[y,x] = pixels1 [y,x]
                    if pixels1 [y,x] == (255,0,0):
                        totalr += 1

                if pixels2[y, x] == (255,0,0) and pixels1[y,x] != (255,0,0):
                    totalr += 1

        f.write(f"{date},{totalr}\n")
    f.close()
