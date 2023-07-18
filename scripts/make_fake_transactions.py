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
from itertools import combinations
from omegaconf import OmegaConf
from sklearn.preprocessing import StandardScaler
from sds4gdsp.processor import calc_haversine_distance, z_score

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
dist_matrix["distance_scaled"] = dist_matrix.groupby("site1")["distance"].apply(lambda col: (col - col.mean()) / col.std()).tolist()
dist_matrix["latch_proba"] = dist_matrix.groupby("site1")["distance_scaled"].apply(lambda arr: softmax(arr)).tolist()



dist_matrix.groupby("site1").distance.apply(
    lambda x: scaler.fit_transform(x.to_numpy().reshape(-1, 1)).reshape(1, len(x))[0]
).reset_index()

# next steps
# 1. standardize or scale
# 2. invert the order? sub 1
# 2. apply softmax

scaler = StandardScaler()
site_filter = dist_matrix.site1=="glo-cel-99"
dist_matrix_sample = dist_matrix.loc[site_filter]
arr = dist_matrix_sample.distance.to_numpy()
arr_scaled = scaler.fit_transform(arr.reshape(-1, 1))\
    .reshape(1, len(arr))[0]

scaler.fit_transform(np.array([1, 2, 3]).reshape(-1, 1)).reshape(1, 3)


# compare dist
fig, ax = plt.subplots(1, 2, figsize=(10, 5))
pd.Series(arr).hist(ax=ax[0], color="blue", alpha=0.1)
pd.Series(arr_scaled).hist(ax=ax[1], color="red", alpha=0.1)


np.sum(softmax(arr_scaled))

# standardscaler -> softmax


random.choices?

# save file to local disk
# fake_transactions = ...
# filepath = "data/fake_subscribers.csv"
# fake_transactions.to_csv(filepath, index=False)