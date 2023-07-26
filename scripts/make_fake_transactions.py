"""This python script creates a fake telco transactions dataset.
OUTPUT: 'data/fake_transactions.csv'
"""

import os
os.chdir("../")
curr_dir = os.getcwd()
print(f"working @: {curr_dir}")

import random
import pendulum
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
cap_start_hr = cfg.fake_transactions.cap_start_hr
stay_proba = cfg.fake_transactions.stay_proba

HRS_IN_A_DAY = 24

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

start_date = pendulum.parse(start_date, exact=True)
end_date = start_date.add(days=num_days-1)
period = pendulum.period(start_date, end_date)

fake_transactions = pd.DataFrame()

for idx, row in fake_subscribers.iterrows():

    curr_sub = row.uid

    # sample a random hour as starting point, this is
    # done to reflect the nature of data in data lake,
    # meaning the sub hasn't moved from his/her prev
    # loc from the previous day (not captured)
    curr_hr = random.sample(range(cap_start_hr), 1)[0]

    # sample home loc for sub, coin this as curr loc
    # let's assume that the first transaction of the
    # month is the home loc of the sub (site level)
    curr_loc = fake_cellsites.uid.sample(1).item()

    for dt in period:

        transaction_dt = str(dt)
        
        # init/reset accu for locs and hrs
        hrs = []
        hrs.append(curr_hr)
        locs = []
        locs.append(curr_loc)

        for hr in range(curr_hr+1, HRS_IN_A_DAY):

            with_transaction = random.choices([True, False], [1-stay_proba, stay_proba])[0]

            if with_transaction:

                hrs.append(hr)

                # identify next site hop based on ref matrix
                # assume equal weighting for top k options
                filter_k = matrix.site1 == curr_loc
                curr_loc = matrix.loc[filter_k].sample(1).site2.item()
                locs.append(curr_loc)

        subs = [curr_sub]*len(locs)
        dts = [transaction_dt]*len(locs)

        # append to fake transactions
        data = pd.DataFrame(
            data=dict(
                sub_id=subs,
                cel_id=locs,
                transaction_dt=dts,
                transaction_hr=hrs
            ),
            index=range(len(locs))
        )
        fake_transactions = \
            pd.concat([fake_transactions, data], ignore_index=True)
        
# save file to local disk
filepath = f"data/fake_transactions.csv"
fake_transactions["uid"] = [f"glo-txn-{str(i+1).zfill(5)}" for i in range(len(fake_transactions))]
fake_transactions = fake_transactions[["uid", "sub_id", "cel_id", "transaction_dt", "transaction_hr"]]
fake_transactions.to_csv(filepath, index=False)