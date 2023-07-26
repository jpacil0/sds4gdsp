"""This python script creates a fake telco subscriber dataset.
OUTPUT: 'data/fake_subscribers.csv'
"""

# import os
# os.chdir("../")
# curr_dir = os.getcwd()
# print(f"working @: {curr_dir}")

import hydra
import random
import pandas as pd
from omegaconf import DictConfig
from faker import Faker

@hydra.main(version_base=None, config_path="../conf", config_name="config")
def main(cfg: DictConfig) -> None:

    seed = cfg.seed
    filepath = cfg.fake_subscribers.filepath
    num_subs = cfg.fake_subscribers.num_subs
    min_age = cfg.fake_subscribers.min_age
    max_age = cfg.fake_subscribers.max_age

    # initialize faker module
    fake = Faker()

    # for reproducibility
    random.seed(seed)

    fake_subscribers = pd.DataFrame()

    for i in range(num_subs):
        uid = f"glo-sub-{str(i+1).zfill(3)}"
        gender = random.choice(["male", "female"])
        name = fake.name_male() if gender=="male" else fake.name_female()
        age = random.randint(min_age, max_age)
        chi_indicator = random.choice([0, 1])
        ewallet_user_indicator = random.choice(["Y", "N"])
        data = pd.DataFrame(
            dict(
                uid=uid,
                gender=gender,
                age=age,
                name=name,
                chi_indicator=chi_indicator,
                ewallet_user_indicator=ewallet_user_indicator
            ), index=[0]
        )
        fake_subscribers = pd.concat([fake_subscribers, data], ignore_index=True)

    fake_subscribers.to_csv(filepath, index=False)
    print(f"OK. Successfully saved '{filepath}'")

if __name__ == "__main__":
    main()