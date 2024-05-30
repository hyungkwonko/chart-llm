import os
import pandas as pd
from glob import glob

os.makedirs("./files/htmls/githubfiles/", exist_ok=True)

filepath = "./files/htmls/githubfiles/"

csv_files = glob(filepath + "*.csv")
dfs = []
for file in csv_files:
    print(file)
    df = pd.read_csv(file)
    dfs.append(df)

merged_df = pd.concat(dfs, axis=0)
merged_df.to_csv(f"./files/htmls/githubfiles/all_htmls.csv", index=False)
print(f"completed: all_htmls.csv")
