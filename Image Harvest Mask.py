from PIL import Image, ImageDraw
import glob
import os

'''
This function will get the satellite image, put sugarcane first sugarcane first layer mask on it
the dark green color will be masked as blue color which mean plant already mature
the light green color will be masked as green color which mean plant on growing stage
the brown color will be masked as red color which mean plant already harvested
the white color will be masked as yellow color which mean its cloud
Image will be saved as new masked images
'''
def getharvestmask(tile_x, tile_y):
    mask = Image.open(f"./masks/mask-x{tile_x}-y{tile_y}.png")
    arr = os.listdir(f"./sugarcanetiles/{tile_x}-{tile_y}")
    for k in arr:
        if "TCI" in k:
            tile = Image.open(f"./sugarcanetiles/{tile_x}-{tile_y}/" + k)
            date = k[13:24]
            pixels = tile.load()
            overlay = mask.load()
            for y in range(512):
                for x in range(512):
                    if overlay[y, x] == (0, 0, 0, 255):
                        red = pixels[y, x][0]
                        green = pixels[y, x][1]
                        blue = pixels[y, x][2]
                        channelPortion = (green / (green + red + blue))
                        channelWhite = (green + red + blue)
                        if channelPortion < 0.32:  # harvest
                            pixels[y, x] = (255, 0, 0)
                        elif channelPortion > 0.35 and channelPortion < 0.37:  # mature
                            pixels[y, x] = (0, 0, 200)
                        elif channelPortion > 0.38:  # grow
                            pixels[y, x] = (3, 194, 3)
                        elif channelWhite == 765:
                            pixels[y, x] = (255, 250, 0)

            tile.save(f"data/harvested-{tile_x}-{tile_y}/{tile_x}-{tile_y}" + date + ".png")


