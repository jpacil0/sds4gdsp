"""This python script creates a fake cellsites dataset.
We'll be assuming here that the cellsites are built exclusively on road intersections
and is unique per location (node in the graph); this does not reflect the real-world.
OUTPUT: 'data/fake_cellsites.csv'
"""

import os
os.chdir("../")
curr_dir = os.getcwd()
print(f"working @: {curr_dir}")

import random
import shapely
import osmnx as ox
import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
from gadm import GADMDownloader
from omegaconf import OmegaConf
from functools import reduce
from shapely.geometry import Point, MultiPolygon
from sds4gdsp.processor import get_coords_from_graph, dedupe_points

# fetch configs
PATH_CONFIG = "conf/config.yaml"
cfg = OmegaConf.load(PATH_CONFIG)
seed = cfg.seed
gadm_version = cfg.fake_cellsites.gadm_version
sample_frac = cfg.fake_cellsites.sample_frac
min_distance = cfg.fake_cellsites.min_distance
town_keyword = cfg.fake_cellsites.town_keyword

# for reproducibility
random.seed(seed)

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
# edit in the yaml config file as needed
# we want to isolate the town boundaries
town_filter = gadm.NAME_2==town_keyword
polygon = gadm.loc[town_filter].geometry.item()

# this should be a unique shapely multipolygon
# with lng, lat format when the bounds is unpacked
assert type(polygon) == MultiPolygon
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

nodes = list(G.nodes)
random.shuffle(nodes)
coords = get_coords_from_graph(G, nodes)
points = list(map(lambda z: Point(z), coords))

# let's sample a small fraction of the nodes from the town graph
sampled_nodes = random.sample(nodes, int(len(nodes)*sample_frac))
sampled_coords = get_coords_from_graph(G, sampled_nodes)
sampled_points = list(map(lambda z: Point(z), sampled_coords))
deduped_points = dedupe_points(points, min_distance)

# check sampled points vis-a-vis the nodes of original graph
filepath = "docs/fake_cellsites.png"
fig, ax = plt.subplots(1, 1, figsize=(10, 10))
gpd.GeoSeries(points).plot(ax=ax, color="red", alpha=0.4, markersize=50)
gpd.GeoSeries(map(lambda s: shapely.wkt.loads(s), deduped_points)).plot(markersize=100, color="blue", alpha=1, ax=ax)
ax.plot(*polygon.geoms[0].exterior.xy, linewidth=5, zorder=0)
ax.legend(["road intersection", "cellsite", "town boundary"], loc="lower right", facecolor="white", framealpha=1)
ax.ticklabel_format(useOffset=False)
plt.savefig(filepath)

# save file to local disk
filepath = f"data/fake_cellsites.csv"
fake_cellsites = pd.DataFrame(dict(
    uid=[f"glo-cel-{str(i+1).zfill(3)}" for i in range(len(deduped_points))],
    coords=deduped_points
))
fake_cellsites.to_csv(filepath, index=False)