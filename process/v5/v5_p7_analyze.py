import csv
import json
import hashlib
from glob import glob
from collections import Counter


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
        data = json.load(f)
        content = json.dumps(data, indent=4)
        content_encoded = content.encode()
        return data, hashlib.sha256(content_encoded).hexdigest()


names = ["q1_visqa", "q2_data2vis", "q3_nvBench", "q4_vega-lite", "q5_ours"]
# names = ["q4_vega-lite"]

for name in names:
    print(f"progress... {name}")
    if name == "q5_ours":
        files = glob("./files/v5/jsonfiles/d7/*.json")
    elif name == "q1_visqa":
        files = glob("./benchmark/VisQA-release/dataset/dataset/*/specs/*.json")
    elif name == "q2_data2vis":
        files = glob("./benchmark/data2vis/examples/*/*.json")
    elif name == "q3_nvBench":
        files = glob("./benchmark/nvBench/vega/*.json")
    elif name == "q4_vega-lite":
        files = glob("./benchmark/vega-lite/*.vl.json")
    else:
        print("error")
        exit()

    hashes = {}

    all_keys = []
    for i, file in enumerate(files):
        json_content, hash_value = get_hash(file)
        if hash_value in hashes:
            print(f"{i}, {file}")
        else:
            hashes[hash_value] = file
            all_key = get_all_keys(json_content)
            all_keys += all_key

    item_counts = Counter(all_keys)
    output_file = f"./files/v5/csvfiles/item_counts_{name}.csv"

    with open(output_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Item", "Count"])  # Write header
        writer.writerows(item_counts.items())

    print(f"File: {output_file}, len(hashes): {len(hashes)}, len(files): {len(files)}")
