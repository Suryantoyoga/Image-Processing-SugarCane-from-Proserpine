import pickle

# Load the saved data
ndvi_master = pickle.load(open("ndvi_master.data", "rb"))
dates = pickle.load(open("dates.data", "rb"))
tiles = pickle.load(open("tiles.data", "rb"))

# Create summary of average NDVI
summary = list()
for date in range(0, len(dates)):
    ndvi_weighted = 0
    pixel_total = 0
    for tile in range(0, len(tiles)):
        current_slice = ndvi_master[tile][date]
        ndvi_weighted = ndvi_weighted + current_slice[1] * current_slice[2]
        pixel_total = pixel_total + current_slice[2]
    summary.append([dates[date], ndvi_weighted, pixel_total, ndvi_weighted / pixel_total])

# Write summary to a CSV file
f = open(f"average_NDVI.csv", "w+")
f.write(f"Date,Weighted_NDVI,Total_Pixels,Average_NDVI\n")
for row in range(0,len(summary)):
    f.write(f"{summary[row][0]},{summary[row][1]},{summary[row][2]},{summary[row][3]}\n")
f.close()