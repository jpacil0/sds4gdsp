"""This python script creates a fake telco transactions dataset.
OUTPUT: 'data/fake_transactions.csv'
"""

import os
os.chdir("../")
curr_dir = os.getcwd()
print(f"working @: {curr_dir}")

import random
import pandas as pd
from itertools import permutations
from omegaconf import OmegaConf
from sds4gdsp.processor import calc_haversine_distance

PATH_CONFIG = "conf/config.yaml"
cfg = OmegaConf.load(PATH_CONFIG)
seed = cfg.seed
k_nearest_neighbor = cfg.fake_transactions.k_nearest_neighbor
start_date = cfg.fake_transactions.start_date
num_days = cfg.fake_transactions.num_days

# for reproducibility
random.seed(seed)

# load relevant datasets
filepath_subscribers = "data/fake_subscribers.csv"
fake_subscribers = pd.read_csv(filepath_subscribers)
filepath_cellsites = "data/fake_cellsites.csv"
fake_cellsites = pd.read_csv(filepath_cellsites)

# start off with a cellsite permutation reference table
cellsite_pairs = list(permutations(fake_cellsites.uid.tolist(), 2))
matrix = pd.DataFrame(cellsite_pairs, columns=["site1", "site2"])
matrix = matrix.merge(fake_cellsites, left_on="site1", right_on="uid")\
    .rename(columns={"coords": "coords1"})\
    .drop(columns=["uid"])
matrix = matrix.merge(fake_cellsites, left_on="site2", right_on="uid")\
    .rename(columns={"coords": "coords2"})\
    .drop(columns=["uid"])

# filter only the top k possible sites-to-hop per site 
matrix["distance"] = matrix.apply(lambda x: calc_haversine_distance(x.coords1, x.coords2), axis=1)
matrix["rank_nearest"] = matrix.groupby("site1")["distance"].rank("min")
filter_top_k = matrix.rank_nearest <= k_nearest_neighbor
matrix = matrix.loc[filter_top_k].reset_index(drop=True)

# for sanity checking purposes
# comment out code below as needed
num_rows_per_site = 3
matrix.sort_values(
    by=["site1", "site2"],
    key=lambda col: col.apply(lambda x: int(x.split("-")[-1])),
    ascending=[1, 1]
)\
    .reset_index(drop=True)\
    .head(k_nearest_neighbor*num_rows_per_site)

# TODO: Add for loop, simulate the hops per sub per day
# 1. Fetch sub, fetch date, init random origin
# 2. Simulate hop based on matrix