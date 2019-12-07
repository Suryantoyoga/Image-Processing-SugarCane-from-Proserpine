# Improving Sugarcane Irrigation practices using Satellite Intelegence
This project was created for Datathon 2019 Data2App Challenge

## Problem Description
The changing climate increases the occurrence of droughts and flooding rains. Both have the potential impact of
decreasing sugarcane productivity. In a survey conducted by Sugar Research Australia (SRA), irrigation
was reported as one of the main constraints to productivity for sugarcane produces (Sugar Research
Australia, 2018). Additionally, water is one of the major aspects that needs to be considered in
supporting the industry’s sustainability programs. Irrigation infrastructure and water use efficiency is
a vital for the increase of productivity and profitability.

## Proposed Solution
The aim of the project is to improve the irrigation practices of sugarcane producers using satellite
intelligence. The irrigation scheduling tool devised uses a land parcel specific, water balance model that can enable
a farmer to time or schedule irrigation to fulfil their field’s needs. By tailoring the water needs and
watering times individually to that specific part of cultivated land, we can potentially maximise yield
while keeping irrigation costs to a minimum.

## Packages to import
1. Matplotlib
2. Numpy
3. Pandas
4. Scikit-learn
5. S2cloudlesspackage (need to import lightgbm and shapely first)
6. Pickle

## Methodology 
1. Get the data : satellite image data, daily rainfall, daily evapotranspiration Proserpine area from Bureau of Meteorology
2. Prepare the data : Remove cloud outliers, calculate sugarcane yield, and average NDVI value of the farm plots.
3. Explore and data modelling : Calculate crop evapotranspiration using NDVI value (Research from Sugarcane Australia, 2018), and combining with rainfall dataset to create water balance model
4. Make Front-End Application : Based on the water balance model, to create irrigation scheduling tools

## Code Explaination
1. ImageHarvestMask.py is to create masks for sugarcane images, this mask differentiate sugarcane cycle by 3 level, green = growth phase, blue = mature phase, and red = already harvested
2. HarvestTimeSeries is to calculate masked images and write it to csv files
3. Sentile.py is code where we store sentile object and helper function 
4. CreateMaskCalculateNDVI is to create cloud masks, calculate NDVI, and store in form of pickle
5. pickle2csv.py is to convert pickle file to csv files


