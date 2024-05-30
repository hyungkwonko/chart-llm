# 1. load json file
# 2. sort json file using key
# 3. save using same format (will be tested for redundancy check)
# 4. if it is a unique file, then convert it to hash
# 5. get all keys
# 6. save Key - Count pair

import csv
import json
import hashlib
from glob import glob
from collections import Counter
import numpy as np


EXCLUDE_KEYS = ["datasets", "values"]


def sort_json(json_data):
    if isinstance(json_data, dict):
        sorted_data = {
            key: sort_json(value) for key, value in sorted(json_data.items())
        }
        return sorted_data

    if isinstance(json_data, list):
        return [sort_json(item) for item in json_data]

    return json_data


def get_all_keys(json_data):
    keys = []
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            keys.append(key)
            if key not in EXCLUDE_KEYS:
                keys.extend(get_all_keys(value))
    elif isinstance(json_data, list):
        for item in json_data:
            if isinstance(item, dict) and any(key in item for key in EXCLUDE_KEYS):
                continue
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


# keys = [
#     "q1_visqa",
#     "q2_data2vis",
#     "q3_chartseer",
#     "q4_nvBench",
#     "q5_vega-lite",
#     "q6_ours",
# ]
keys = ["q6_ours"]

for key in keys:
    print(f"progress... {key}")
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

    all_keys = []
    for i, file in enumerate(files):
        # print(f"{i}, {file}")
        json_content, hash_value = get_hash(file)
        if hash_value not in hashes:
            hashes[hash_value] = file
            # 5. get all keys except for "datasets" and "values"
            all_key = get_all_keys(json_content)
            all_keys += all_key
        else:
            print(f"hash error: {i}, {file}")

    item_counts = Counter(all_keys)
    output_file = f"./files/v6/csvfiles/item_counts_{key}.csv"

    # 6. save Key - Count pair
    with open(output_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Item", "Count"])  # Write header
        writer.writerows(item_counts.items())

    print(f"File: {output_file}, len(hashes): {len(hashes)}, len(files): {len(files)}")
