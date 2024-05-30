import json
from glob import glob
import pandas as pd
import math
import numpy as np
import Levenshtein
import hashlib


def get_hash(file_path):
    with open(file_path, "rb") as f:
        data = json.load(f)
        content = json.dumps(data, indent=4)
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


def sort_and_filter_json(json_data, keys):
    if isinstance(json_data, dict):
        # Sort keys in the dictionary
        sorted_data = {
            key: sort_and_filter_json(value, keys)
            for key, value in sorted(json_data.items())
        }

        # Remove unwanted keys and their descendants
        filtered_data = {key: sorted_data[key] for key in sorted_data if key in keys}

        return filtered_data

    if isinstance(json_data, list):
        # Sort and filter each element in the list
        return [sort_and_filter_json(item, keys) for item in json_data]

    return json_data


filter = pd.read_csv("./files/v5/csvfiles/keys.csv")
# keys = ["q1_visqa", "q2_data2vis", "q3_nvBench", "q4_vega-lite", "q5_ours"]
keys = ["q4_vega-lite"]

dists = []

for ix, key in enumerate(keys):
    filter_tmp = [
        x for x in list(filter[key]) if not (isinstance(x, float) and math.isnan(x))
    ]

    if key == "q5_ours":
        files = glob("./files/v5/jsonfiles/d7/*.json")
    elif key == "q1_visqa":
        files = glob("./benchmark/VisQA-release/dataset/dataset/*/specs/*.json")
    elif key == "q2_data2vis":
        files = glob("./benchmark/data2vis/examples/*/*.json")
    elif key == "q3_nvBench":
        files = glob("./benchmark/nvBench/vega/*.json")
    elif key == "q4_vega-lite":
        files = glob("./benchmark/vega-lite/*.vl.json")
    else:
        print("error")
        exit()

    filter_tmp.append("root")

    complexities = []
    hashes = {}

    for i, file in enumerate(files):
        print(f"progress... {i} / {len(files)}")

        data, hash_value = get_hash(file)
        if hash_value in hashes:
            print(f"{i}, {file}")
        else:
            hashes[hash_value] = file
            # print(json.dumps(data, indent=4))
            data = sort_and_filter_json(data, filter_tmp)
            # print(json.dumps(data, indent=4))
            data = replace_values_with_empty_string(data)
            # print(json.dumps(data, indent=4))
            data = json.dumps(data, indent=4)

            complexities.append(data)

    # Calculate pairwise Levenshtein distances
    dist = calculate_pairwise_levenshtein_distance(complexities)
    dists.append(np.mean(dist))
    print(dists)

for i in range(len(keys)):
    print(f"key: {keys[i]} \t\t levenshtein_distance: {dists[i]}")
