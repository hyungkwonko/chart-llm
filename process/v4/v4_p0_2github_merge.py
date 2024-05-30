import os
import pandas as pd
from glob import glob

highs = ["encoding", "mark", "projection", "transform", "composition"]
lowss = [
    ["field", "type", "scale", "format", "axis", "value", "legend", "condition", "aggregate", "sort", "time", "unit", "datum", "stack", "bin", "header", "band", "impute",],
    ["text", "line", "point", "bar", "geoshape", "circle", "rule", "area", "arc", "rect", "square", "tick", "boxplot", "image", "trail", "errorband", "errorbar",],
    ["projection"],
    ["filter", "calculate", "lookup", "aggregate", "timeunit", "regression", "window", "fold", "stack", "pivot", "bin", "joinaggregate", "density", "flatten", "loess", "impute", "quantile", "sample",],
    ["layer", "resolve", "repeat", "facet", "concat"],
]
QS = ["q1", "q2"]

for h_index, HIGH in enumerate(highs):
    folder_path = f"./files/v4/githubfiles/"
    lows = lowss[h_index]

    for LOW in lows:
        for q in QS:
            filename = f"{HIGH}_{LOW}_{q}"
            csv_files = [
                f
                for f in os.listdir(folder_path)
                if f.startswith(filename) and f.endswith(".csv")
            ]
            dfs = []
            for file in csv_files:
                df = pd.read_csv(os.path.join(folder_path, file))
                dfs.append(df)

            if len(dfs) > 1:
                merged_df = pd.concat(dfs, axis=0)
            else:
                merged_df = df
            merged_df.to_csv(f"./files/v4/githubmergefiles/{filename}.csv", index=False)
            print(f"completed: {filename}.csv")

all_files = glob(f"./files/v4/githubfiles/*.csv")
dfs = []
for file in all_files:
    df = pd.read_csv(file)
    dfs.append(df)
merged_df = pd.concat(dfs, axis=0)
merged_df.to_csv(f"./files/v4/githubmergefiles/all.csv", index=False)
print(f"completed: all.csv")