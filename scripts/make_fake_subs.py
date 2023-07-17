"""This python script creates a fake telco subscriber dataset.
We'll be adding some descriptors used in the Unified User Profile (UUP).
OUTPUT: 'data/fake_subs.csv'
"""

# import os
# os.chdir("../")
# curr_dir = os.getcwd()
# print(f"working @: {curr_dir}")

import random
import pandas as pd
from omegaconf import OmegaConf
from faker import Faker
fake = Faker()

PATH_CONFIG = "conf/config.yaml"
cfg = OmegaConf.load(PATH_CONFIG)
seed = cfg.seed
num_subs = cfg.fake_subs.num_subs
min_age = cfg.fake_subs.min_age
max_age = cfg.fake_subs.max_age

# for reproducibility
random.seed(seed)

fake_subs = pd.DataFrame()

for i in range(num_subs):
    uid = f"glo-sub-{i+1}"
    gender = random.choice(["male", "female"])
    name = fake.name_male() if gender=="male" else fake.name_female()
    age = random.randint(min_age, max_age)
    chi_indicator = random.choice([0, 1])
    gcash_user_indicator = random.choice(["Y", "N"])
    data = pd.DataFrame(
        dict(
            uid=uid,
            gender=gender,
            age=age,
            name=name,
            chi_indicator=chi_indicator,
            gcash_user_indicator=gcash_user_indicator
        ), index=[0]
    )
    fake_subs = pd.concat([fake_subs, data], ignore_index=True)

filepath = "data/fake_subs.csv"
fake_subs.to_csv(filepath, index=False)