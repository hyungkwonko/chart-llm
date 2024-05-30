import hashlib
import numpy as np
import pandas as pd
import json
from glob import glob


def get_hash(file_path):
    with open(file_path, "rb") as f:
        data = json.load(f)
        content = json.dumps(data, indent=4)
        content_encoded = content.encode()
        return hashlib.sha256(content_encoded).hexdigest()


benchmk_files = glob("./benchmark/vega-lite-v4/*.vl.json")
benchmk_files = np.sort(benchmk_files)

our_data = "./files/v4/jsonfiles/d3/*.vl.json"
our_files = glob(our_data)
our_files = np.sort(our_files)

hashes = {}

for j, file_path in enumerate(benchmk_files):
    hash_value = get_hash(file_path)

    if hash_value in hashes:
        print(f"{j}, {file_path}")
    else:
        hashes[hash_value] = file_path

print(f"len(hashes): {len(hashes)}")

m = 0
uniq = []

for i, file_path in enumerate(our_files):
    print(file_path)
    hash_value = get_hash(file_path)
    if hash_value in hashes:
        # os.remove(file_path)
        # print(f"m: {m}")
        # print(f"Removed duplicate file: {file_path}, m: {m}")
        m += 1
        uniq.append(0)
    else:
        hashes[hash_value] = file_path
        uniq.append(1)

print(f"total - duplicates: {len(our_files)} - {m} = {len(our_files) - m}")

df = pd.DataFrame()
df["path"] = our_files
df["unique"] = uniq
df.to_csv("./files/v4/csvfiles/d3.csv", index=False)

print("file saved")
