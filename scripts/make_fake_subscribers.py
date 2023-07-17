"""This python script creates a fake telco subscriber dataset.
We'll be adding some descriptors used in the Unified User Profile (UUP).
OUTPUT: 'data/fake_subscribers.csv'
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
num_subs = cfg.fake_subscribers.num_subs
min_age = cfg.fake_subscribers.min_age
max_age = cfg.fake_subscribers.max_age

# for reproducibility
random.seed(seed)

fake_subscribers = pd.DataFrame()

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
    fake_subscribers = pd.concat([fake_subscribers, data], ignore_index=True)

filepath = "data/fake_subscribers.csv"
fake_subscribers.to_csv(filepath, index=False)