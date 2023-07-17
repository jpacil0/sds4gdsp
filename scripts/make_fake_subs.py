"""This python script creates a fake telco subscriber dataset.
We'll be adding some descriptors used in the Unified User Profile (UUP).
OUTPUT: 'data/fake_subs.csv'
"""

import random
import pandas as pd
from omegaconf import OmegaConf
from faker import Faker
fake = Faker()

PATH_CONFIG = "conf/config.yaml"
cfg = OmegaConf.load(PATH_CONFIG)
num_subs = cfg.fake_data.num_subs
min_age = cfg.fake_data.min_age
max_age = cfg.fake_data.max_age

random.seed(2023)

fake_data = pd.DataFrame()

for i in range(num_subs):
    uid = f"glo-{i+1}"
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
    fake_data = pd.concat([fake_data, data], ignore_index=True)

filepath = "data/fake_subs.csv"
fake_data.to_csv(filepath, index=False)