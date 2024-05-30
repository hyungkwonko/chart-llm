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


arvind_data = "./benchmark/vega-lite/examples/specs/*.vl.json"
arvind_data2 = "./benchmark/vega-lite/examples/specs/normalized/*.vl.json"
arvind_files = glob(arvind_data) + glob(arvind_data2)
arvind_files = np.sort(arvind_files)

our_data = "./files/v1/jsonfiles/d5/*.vl.json"
our_files = glob(our_data)
our_files = np.sort(our_files)

hashes = {}

# there are 7 repeatition: 716 --> 709
for j, file_path in enumerate(arvind_files):
    hash_value = get_hash(file_path)

    if hash_value in hashes:
        print(f"{j}, {file_path}")
    else:
        hashes[hash_value] = file_path

print(f"len(hashes): {len(hashes)}")

m = 0
uniq = []

for i, file_path in enumerate(our_files):
    # print(file_path)
    if (i == 89) or (i == 90) or (826 <= i <= 834) or (869 <= i <= 873):
        m += 1
        uniq.append(0)
        continue
    hash_value = get_hash(file_path)
    if hash_value in hashes:
        # os.remove(file_path)
        # print(f"Removed duplicate file: {file_path}")
        m += 1
        uniq.append(0)
    else:
        hashes[hash_value] = file_path
        uniq.append(1)

print(f"total - duplicates: {len(our_files)} - {m} = {len(our_files) - m}")

df = pd.DataFrame()
df["path"] = our_files
df["unique"] = uniq
df.to_csv("./files/v1/csvfiles/d5.csv", index=False)

print("file saved")
