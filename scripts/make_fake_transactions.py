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
from sklearn.preprocessing import StandardScaler
from sds4gdsp.processor import calc_haversine_distance, convert_distances_to_probas, scale_feature

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
cellsite_pairs = list(permutations(fake_cellsites.uid.tolist(), 2))
matrix = pd.DataFrame(cellsite_pairs, columns=["site1", "site2"])
matrix = matrix.merge(fake_cellsites, left_on="site1", right_on="uid")\
    .rename(columns={"coords": "coords1"})\
    .drop(columns=["uid"])
matrix = matrix.merge(fake_cellsites, left_on="site2", right_on="uid")\
    .rename(columns={"coords": "coords2"})\
    .drop(columns=["uid"])
matrix["distance"] = matrix.apply(lambda x: calc_haversine_distance(x.coords1, x.coords2), axis=1)
matrix = matrix.sort_values(
    by=["site1", "site2"],
    key=lambda col: col.apply(lambda x: int(x.split("-")[-1])),
    ascending=[True, True]
)\
    .reset_index(drop=True)
scaler = StandardScaler()
# distances = matrix.distance.tolist()
# probas = convert_distances_to_probas(distances, scaler)
matrix["distance_scaled"] = matrix.groupby("site1")["distance"].apply(lambda x: scale_feature(x, scaler)).explode().tolist()
matrix["proba"] = matrix.groupby("site1")["distance_scaled"].apply(lambda x: convert_distances_to_probas(x)).explode().tolist()

# check this out
matrix.groupby("site1").proba.sum()

f = matrix.site1=="glo-cel-100" 
matrix.loc[f]\
    .proba.hist()


matrix["scaled_distance"] = matrix.groupby("site1")["distance"].apply(lambda x: scale_feature(x, scaler)).explode().tolist()
convert_distances_to_probas(col, scaler)

type(apply_softmax(ds))
type(convert_distances_to_probas(ds, scaler))


matrix.groupby("site1")["distance"].apply(lambda col: convert_distances_to_probas(col, scaler)).reset_index()




matrix["latch_proba"] = matrix.groupby("site1")["distance_scaled"].apply(lambda arr: apply_softmax(arr)).tolist()

# check this out, this should be 111
matrix.groupby("site1").latch_proba.sum().sum()

# next steps
# 1. try binning the feature
# 1. standardize or scale; change to minmax scaling
# 2. invert the order? sub 1
# 2. apply softmax


site_filter = matrix.site1=="glo-cel-10"
matrix_sample = matrix.loc[site_filter]


# standardscaler -> softmax

from sklearn.preprocessing import StandardScaler

arr = [1, 2, 3]
scaler.fit_transform(np.array(arr).reshape(-1, 1)).flatten().tolist()

random.choices?

# save file to local disk
# fake_transactions = ...
# filepath = "data/fake_subscribers.csv"
# fake_transactions.to_csv(filepath, index=False)


ds = matrix_sample.distance.tolist()

scaler = StandardScaler()
ds_scld = scaler.fit_transform(np.array(ds).reshape(-1, 1)).flatten().tolist()

alpha = 1
ds_proba = np.exp(-alpha*np.array(ds_scld))
prob_df = pd.DataFrame(
    dict(distance=ds, proba=ds_proba)
)
display(prob_df.sort_values(by="distance"))

sampleList = [10, 20, 30, 40]
weights = [0.1, 0.2, 0.6, 0.5]
random.choices(
    population=sampleList, weights=weights, k=1
)

type(convert_distances_to_probas(ds, scaler, 1))