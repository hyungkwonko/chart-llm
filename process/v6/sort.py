import csv
import json
import hashlib
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


def get_hash(file_path):
    with open(file_path, "rb") as f:
        # 1. load json file
        data = json.load(f)

        # 2. sort json file using key
        data = sort_json(data)

        print(data)

        # 3. save using same format (will be tested for redundancy check)
        content = json.dumps(data, indent=2)

        # 4. convert it to hash
        content_encoded = content.encode()
        return data, hashlib.sha256(content_encoded).hexdigest()


file = "./files/v6/jsonfiles/d4/vl_1388.vl.json"

get_hash(file)
