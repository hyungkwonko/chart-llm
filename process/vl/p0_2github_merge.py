import os
import pandas as pd
from glob import glob

os.makedirs("./files/vl/githubfiles/", exist_ok=True)

filepath = "./files/vl/githubfiles/"

csv_files = glob(filepath + "*_*")
dfs = []
for file in csv_files:
    df = pd.read_csv(file)
    dfs.append(df)

merged_df = pd.concat(dfs, axis=0)
merged_df.to_csv(f"./files/vl/githubfiles/merged.csv", index=False)
print(f"completed: merged.csv")
