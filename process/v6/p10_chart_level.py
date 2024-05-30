# 1. load json file
# 2. sort json file using key
# 3. save using same format (will be tested for redundancy check)
# 4. convert it to hash
# 5. get all keys for each file removing dependents of "datasets" and "values"
# 6. filter keys that are not defined in vega-lite v5 schema
# 7. calculate level based on the stat of our data
# 8. save number of keys for each file, also save the level of each file

import json
import hashlib
import math
import numpy as np
import pandas as pd
from glob import glob
from collections import Counter


def sort_json(json_data):
    if isinstance(json_data, dict):
        sorted_data = {
            key: sort_json(value) for key, value in sorted(json_data.items())
        }
        return sorted_data

    if isinstance(json_data, list):
        return [sort_json(item) for item in json_data]

    return json_data


def filter_json(json_data, keys):
    if isinstance(json_data, dict):
        # Remove unwanted keys and their descendants
        filtered_data = {
            key: filter_json(value, keys) if key not in keys else ""
            for key, value in json_data.items()
        }
        return filtered_data

    if isinstance(json_data, list):
        # Filter each element in the list
        return [filter_json(item, keys) for item in json_data]

    return json_data


def get_all_keys(json_data):
    keys = []
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            keys.append(key)
            keys.extend(get_all_keys(value))
    elif isinstance(json_data, list):
        for item in json_data:
            keys.extend(get_all_keys(item))
    return keys


def get_hash(file_path):
    with open(file_path, "rb") as f:
        # 1. load json file
        data = json.load(f)

        # 2. sort json file using key
        data = sort_json(data)

        # 3. save using same format (will be tested for redundancy check)
        content = json.dumps(data, indent=2)

        # 4. convert it to hash
        content_encoded = content.encode()
        return data, hashlib.sha256(content_encoded).hexdigest()


keys = [
    "q1_visqa",
    "q2_data2vis",
    "q3_chartseer",
    "q4_nvBench",
    "q5_vega-lite",
    "q6_ours",
]
# keys = ["q5_vega-lite"]
keys = ["q6_ours"]

filter = pd.read_csv("./files/v6/csvfiles/keys.csv")
counters = []

for key in keys:
    filter_tmp = [
        x for x in list(filter[key]) if not (isinstance(x, float) and math.isnan(x))
    ]
    filter_tmp.extend(["datasets", "values"])

    if key == "q6_ours":
        files = glob("./files/v6/jsonfiles/d6/*.json")
        # files = ["./files/v6/jsonfiles/d6/vl_0004.vl.json"]
        # files = ["./benchmark/vega-lite/bar_grouped_fixed_width.vl.json"]
    elif key == "q1_visqa":
        files = glob("./benchmark/VisQA-release/dataset/*/specs/*.json")
    elif key == "q2_data2vis":
        files = glob("./benchmark/data2vis/examples/*/*.json")
    elif key == "q3_chartseer":
        files = glob("./benchmark/chartseer/jsonfiles/*.json")
    elif key == "q4_nvBench":
        files = glob("./benchmark/nvBench/vega/*.json")
    elif key == "q5_vega-lite":
        files = glob("./benchmark/vega-lite/*.vl.json")
    else:
        print("error")
        exit()

    files = np.sort(files)

    hashes = {}

    nums = []
    nums_for_stat = []
    for i, file in enumerate(files):
        data, hash_value = get_hash(file)
        if hash_value not in hashes:
            hashes[hash_value] = file
            # 5. get all keys
            data = filter_json(data, filter_tmp)
            all_key = get_all_keys(data)
            # 6. filter keys that are not defined in vega-lite v5 schema
            filtered_key = [x for x in all_key if x not in filter_tmp]
            nums.append(len(filtered_key))
            nums_for_stat.append(len(filtered_key))
        else:
            nums.append(-1)

    # 7. calculate level based on the stat of our data
    levels = [
        "x"
        if num <= 0
        else "easy"
        if num <= 16
        else "medium"
        if num <= 24
        else "hard"
        if num <= 41
        else "hardest"
        for num in nums
    ]
    # levels = [
    #     "x"
    #     if num <= 0
    #     else "easy"
    #     if num <= 30
    #     else "medium"
    #     if num <= 39
    #     else "hard"
    #     if num <= 58
    #     else "hardest"
    #     for num in nums
    # ]

    # 8. save number of keys for each file
    out = pd.DataFrame()
    out["file"] = files
    out["num"] = nums
    out["level"] = levels
    out.to_csv(f"./files/v6/csvfiles/num_{key}.csv", index=False)
    # out.to_csv(f"./files/v6/csvfiles/num_{key}_5standard.csv", index=False)

    item_counts = Counter(levels)
    counters.append(item_counts)

    print(f"key: {key}, item_counts: {item_counts.items()}")

    # if key == "q5_vega-lite":
    st = pd.Series(nums_for_stat)
    print(st.describe())

dfs = []
for i, cnt in enumerate(counters):
    df = pd.DataFrame.from_dict(dict(cnt), orient="index", columns=[keys[i]])
    dfs.append(df)

result = pd.concat(dfs, axis=1)
result.to_csv("./files/v6/csvfiles/counters.csv", index_label="element")
