# GPT에 넣을 input용 Vega-Lite 만들기
# 1. read file
# 2. Datasets, Value 없애는 작업 해야 함
# 3. 빈칸 없애는 작업 해야 함
# 4. save new file

import json
from glob import glob
import os
import json
import re
import numpy as np


EXCLUDE_KEYS = ["datasets", "values"]
new_folder = "./files/v6/jsonfiles/d6_input/"
file_list = glob("./files/v6/jsonfiles/d6/*.json")
file_list = np.sort(file_list)
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

    # 1. read file
    with open(file, "r") as f:
        data = json.load(f)

    # 2. Datasets, Value 없애는 작업 해야 함
    data = replace_values(data)
    json_string = json.dumps(data)

    # 3. 빈칸 없애는 작업 해야 함
    json_string = compress_json(json_string)

    # 4. save new file
    with open(f"{new_folder}{file.split('/')[-1]}", "w") as f:
        f.write(json_string)
