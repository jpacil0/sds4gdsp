"""This python script creates a fake cellsites dataset.
We'll be assuming here that the cellsites are built exclusively on road intersections
and is unique per location (node in the graph); this does not reflect the real-world.
OUTPUT: 'data/fake_cellsites.gpkg'
"""

import os
os.chdir("../")
curr_dir = os.getcwd()
print(f"working @: {curr_dir}")

import shapely
import osmnx as ox
import geopandas as gpd
from gadm import GADMDownloader
from omegaconf import OmegaConf
from functools import reduce

# fetch configs
PATH_CONFIG = "conf/config.yaml"
cfg = OmegaConf.load(PATH_CONFIG)
gadm_version = cfg.fake_data.gadm_version

# download gadm PH data
country_name = "Philippines"
ad_level = 2 # city or municipality
downloader = GADMDownloader(version=str(gadm_version))
gadm = downloader.get_shape_data_by_country_name(
    country_name=country_name, ad_level=ad_level
)

# this should be a non-empty geodataframe
assert len(gadm) > 0

# filter the town of interest accordingly
# let's use Taguig City for this exercise
# we want to isolate the town boundaries
town_keyword = "Taguig"
town_filter = gadm.NAME_2==town_keyword
polygon = gadm.loc[town_filter].geometry.item()

# this should be a unique shapely multipolygon
# with lng, lat format when the bounds is unpacked
assert type(polygon) == shapely.geometry.MultiPolygon
assert len(polygon.geoms) == 1
assert reduce(lambda a, b: a - b, list(polygon.bounds)) < 0

# download the road network in taguig
# for more info, see docs in OSMNx 
network_type = "drive"
simplify = True
retain_all = False
truncate_by_edge = True
clean_periphery = True
G = ox.graph_from_polygon(
    polygon=polygon,
    network_type=network_type,
    simplify=simplify,
    retain_all=retain_all,
    truncate_by_edge=truncate_by_edge,
    clean_periphery=clean_periphery
)

# this should be a non-empty graph
assert len(G.nodes) > 0

# you can visualize the download road network like so
# ox.plot_graph(G)

# save file to local disk
# filepath = f"data/shapefile/gadm_{town_keyword.lower()}.gpkg"

# ADD CODE HERE TO GENERATE FAKE CELLSITES
# 1. Make bounding box for town of interest
# 2. Add coords based on poisson distribution
# 3. Persist shapefile to local disk