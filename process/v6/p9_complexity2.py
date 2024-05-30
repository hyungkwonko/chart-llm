# 1. remove redundant codes
# 2. sort keys
# 3. remove keys that are not defined in vega-lite v5 schema & "datasets" and "values"
# 4. replace all values
# 5. calculate pairwise Levenshtein distances


import json
from glob import glob
import pandas as pd
import math
import numpy as np
import Levenshtein
import hashlib


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


def calculate_pairwise_levenshtein_distance(lst):
    distances = []
    for i in range(len(lst)):
        print(f"progress... {i} ///// {len(lst)}")
        for j in range(i + 1, len(lst)):
            distance = Levenshtein.distance(lst[i], lst[j])
            # print(distance)
            distances.append(distance)
    return distances


def replace_values_with_empty_string(json_data):
    if isinstance(json_data, dict):
        # Iterate through the dictionary
        for key, value in json_data.items():
            if isinstance(value, dict) or isinstance(value, list):
                # Recursively call the function for nested dictionaries or lists
                replace_values_with_empty_string(value)
            else:
                # Replace value with an empty string
                json_data[key] = ""

    if isinstance(json_data, list):
        # Iterate through the list
        for item in json_data:
            if isinstance(item, dict) or isinstance(item, list):
                # Recursively call the function for nested dictionaries or lists in the list
                replace_values_with_empty_string(item)
            else:
                # Replace value with an empty string
                item = ""

    return json_data


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


filter = pd.read_csv("./files/v6/csvfiles/keys.csv")
keys = [
    "q1_visqa",
    "q2_data2vis",
    "q3_chartseer",
    "q4_nvBench",
    "q5_vega-lite",
    "q6_ours",
]
keys = ["q6_ours"]

dists = []


for ix, key in enumerate(keys):
    filter_tmp = [
        x for x in list(filter[key]) if not (isinstance(x, float) and math.isnan(x))
    ]
    filter_tmp = ["datasets", "values"]

    if key == "q6_ours":
        files = glob("./files/v6/jsonfiles/d6/*.json")
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

    complexities = []
    hashes = {}

    for i, file in enumerate(files):
        print(f"progress... {i} / {len(files) - 1}")

        # 1. remove redundant codes
        # 2. sort keys
        data, hash_value = get_hash(file)
        if hash_value in hashes:
            print(f"{i}, {file}")
        else:
            hashes[hash_value] = file
            # 3. remove certain keys
            data = filter_json(data, filter_tmp)
            # if data != data2 and file == "./files/v6/jsonfiles/d6/vl_0026.vl.json":
            #     print(file)
            #     print(data)
            #     print("=")
            #     print(data2)
            #     exit()

            # 4. replace all values
            data = replace_values_with_empty_string(data)
            data = json.dumps(data, indent=2)

            complexities.append(data)

    # 5. calculate pairwise Levenshtein distances
    dist = calculate_pairwise_levenshtein_distance(complexities)
    dists.append(np.mean(dist))
    print(dists)

for i in range(len(keys)):
    print(f"key: {keys[i]} \t\t levenshtein_distance: {dists[i]}")
