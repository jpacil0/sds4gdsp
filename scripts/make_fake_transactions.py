"""This python script creates a fake telco transactions dataset.
OUTPUT: 'data/fake_transactions.csv'
"""

import os
os.chdir("../")
curr_dir = os.getcwd()
print(f"working @: {curr_dir}")

import random
import numpy as np
import pandas as pd
from itertools import permutations
from omegaconf import OmegaConf
from sklearn.preprocessing import StandardScaler, MinMaxScaler
from sds4gdsp.processor import calc_haversine_distance, scale_minmax, apply_softmax

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
scaler = StandardScaler()
scaler = MinMaxScaler()

cellsite_pairs = list(permutations(fake_cellsites.uid.tolist(), 2))
dist_matrix = pd.DataFrame(cellsite_pairs, columns=["site1", "site2"])
dist_matrix = dist_matrix.merge(fake_cellsites, left_on="site1", right_on="uid")\
    .rename(columns={"coords": "coords1"})\
    .drop(columns=["uid"])
dist_matrix = dist_matrix.merge(fake_cellsites, left_on="site2", right_on="uid")\
    .rename(columns={"coords": "coords2"})\
    .drop(columns=["uid"])
dist_matrix["distance"] = dist_matrix.apply(lambda x: calc_haversine_distance(x.coords1, x.coords2), axis=1)
dist_matrix = dist_matrix.sort_values(
    by=["site1", "site2"],
    key=lambda col: col.apply(lambda x: int(x.split("-")[-1])),
    ascending=[True, True]
)\
    .reset_index(drop=True)
scaler = StandardScaler()
dist_matrix["distance_scaled"] = dist_matrix.groupby("site1")["distance"].apply(
    lambda arr: 1 - scale_minmax(arr)
).tolist()
dist_matrix["latch_proba"] = dist_matrix.groupby("site1")["distance_scaled"].apply(lambda arr: apply_softmax(arr)).tolist()

# check this out, this should be 111
dist_matrix.groupby("site1").latch_proba.sum().sum()

# next steps
# 1. standardize or scale; change to minmax scaling
# 2. invert the order? sub 1
# 2. apply softmax


site_filter = dist_matrix.site1=="glo-cel-1"
dist_matrix_sample = dist_matrix.loc[site_filter]
dist_matrix_sample.latch_proba.hist()


# standardscaler -> softmax

from sklearn.preprocessing import StandardScaler

arr = [1, 2, 3]
scaler.fit_transform(np.array(arr).reshape(-1, 1)).flatten().tolist()

random.choices?

# save file to local disk
# fake_transactions = ...
# filepath = "data/fake_subscribers.csv"
# fake_transactions.to_csv(filepath, index=False)