# Download Instructions
# 1. Goto https://gadm.org/download_country.html#google_vignette
# 2. Select Philippines then download GeoJSON and select level2
# 3. Put it in your root folder `data/shapefiles/<file>`

# REMOVE CODE BELOW TEMP ONLY
# import os
# os.chdir("../")

import geopandas as gpd

filepath = "data/shapefile/gadm41_PHL_2.json.zip"
gadm = gpd.read_file(filepath)

# filter the town of interest
# let's use Taguig City for now
# change when you want to explore
town_keyword = "Taguig"
town_filter = gadm.NAME_2==town_keyword
gadm = gadm.loc[town_filter]

# save file to local disk
filepath = f"data/shapefile/gadm_{town_keyword.lower()}.gpkg"
gadm.reset_index(drop=True).to_file(filepath, driver="GPKG")

# ADD CODE HERE TO GENERATE FAKE CELLSITES
# 1. Make bounding box for town of interest
# 2. Add coords based on poisson distribution
# 3. Persist shapefile to local disk