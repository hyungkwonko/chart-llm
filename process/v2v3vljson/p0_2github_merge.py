import os
import pandas as pd
from glob import glob

os.makedirs("./files/v2v3vl/githubfiles/", exist_ok=True)

filepath = "./files/v2v3vl/githubfiles/"

queries = ["v3", "v2", "vl"]
# queries = ["vl"]

for q in queries:
    csv_files = glob(filepath + q + "_*")
    dfs = []
    for file in csv_files:
        df = pd.read_csv(file)
        dfs.append(df)

    merged_df = pd.concat(dfs, axis=0)
    merged_df.to_csv(f"./files/v2v3vl/githubfiles/{q}.csv", index=False)
    print(f"completed: {q}.csv")
