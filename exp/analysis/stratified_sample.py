import os
import pandas as pd
from sklearn.model_selection import StratifiedShuffleSplit

multiple = True
test_size = 0.24

file_in = os.path.join("exp", "analysis", "data", "strata.csv")
file_out = os.path.join("exp", "analysis", "data", "strata_sample.csv")

if __name__ == "__main__":
    df = pd.read_csv(file_in)

    if multiple:
        df["strat_col"] = (
            df["level"].astype(str)
            + "_"
            + df["interaction"].astype(str)
            + "_"
            + df["composite"].astype(str)
        )
    else:
        df["strat_col"] = df["level"]

    split = StratifiedShuffleSplit(n_splits=1, test_size=test_size)

    for train_index, test_index in split.split(df, df["strat_col"]):
        strat_train_set = df.loc[train_index]
        strat_test_set = df.loc[test_index]

    strat_test_set["name"] = [f"vis_{str(i).zfill(4)}" for i in strat_test_set["index"]]
    strat_test_set.to_csv(file_out, index=False)
    print(f"saved file: len(strat_test_set): {len(strat_test_set)}")
    print("strat_test_set\n", strat_test_set)
