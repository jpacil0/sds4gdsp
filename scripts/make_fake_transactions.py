"""This python script creates a fake telco transactions dataset.
OUTPUT: 'data/fake_transactions.csv'
"""

import os
os.chdir("../")
curr_dir = os.getcwd()
print(f"working @: {curr_dir}")

import random
import pandas as pd
from itertools import combinations
from omegaconf import OmegaConf
from sds4gdsp.processor import calc_haversine_distance

PATH_CONFIG = "conf/config.yaml"
cfg = OmegaConf.load(PATH_CONFIG)
seed = cfg.seed

# for reproducibility
random.seed(seed)

# load relevant datasets
filepath_subscribers = "data/fake_subscribers.csv"
fake_subscribers = pd.read_csv(filepath_subscribers)
filepath_cellsites = "data/fake_cellsites.csv"
fake_cellsites = pd.read_csv(filepath_cellsites)

# make a distance matrix as reference, here are the assumptions:
# 1: the hop probability is a function of distance
# 2: the sub is always moving? check this
cellsite_pairs = list(combinations(fake_cellsites.uid.tolist(), 2))
dist_matrix = pd.DataFrame(cellsite_pairs, columns=["site1", "site2"])
dist_matrix = dist_matrix.merge(fake_cellsites, left_on="site1", right_on="uid")\
    .rename(columns={"coords": "coords1"})\
    .drop(columns=["uid"])
dist_matrix = dist_matrix.merge(fake_cellsites, left_on="site2", right_on="uid")\
    .rename(columns={"coords": "coords2"})\
    .drop(columns=["uid"])
dist_matrix["distance"] = dist_matrix.apply(lambda x: calc_haversine_distance(x.coords1, x.coords2), axis=1)
dist_matrix.sort_values(by=["site1", "distance"], ascending=[0, 0], inplace=True)


# save file to local disk
# fake_transactions = ...
# filepath = "data/fake_subscribers.csv"
# fake_transactions.to_csv(filepath, index=False)