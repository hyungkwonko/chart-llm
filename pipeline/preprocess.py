"""
Preprocessing Vega-Lite specifications for input to LLMs

1. reading files
2. extracting inline datasets
3. minification
4. saving new files
"""

import json
from glob import glob
import os
import json
import re
import numpy as np


EXCLUDE_KEYS = ["datasets", "values"]
new_folder = "./docs/data/chart_48_in/"
file_list = np.sort(glob("./docs/data/chart/*.json"))
print(f"len: {len(file_list)}")

os.makedirs(new_folder, exist_ok=True)


def replace_values(json_data):
    if isinstance(json_data, dict):
        for key, value in json_data.items():
            if key in EXCLUDE_KEYS:
                json_data[key] = ""
            else:
                if isinstance(value, dict) or isinstance(value, list):
                    replace_values(value)

    if isinstance(json_data, list):
        # Iterate through the list
        for item in json_data:
            if isinstance(item, dict) or isinstance(item, list):
                # Recursively call the function for nested dictionaries or lists in the list
                replace_values(item)
            else:
                if item in EXCLUDE_KEYS:
                    item = ""

    return json_data


def compress_json(json_data):
    compressed_json = re.sub(r"\s+", " ", json_data)
    return compressed_json


for i, file in enumerate(file_list):
    print(f"progress... {file}")

    # 1. Reading files
    with open(file, "r") as f:
        data = json.load(f)

    # 2. Remove Datasets, Value
    data = replace_values(data)
    json_string = json.dumps(data)

    # 3. Minification
    json_string = compress_json(json_string)

    # 4. Saving new files
    with open(f"{new_folder}{file.split('/')[-1]}", "w") as f:
        f.write(json_string)
