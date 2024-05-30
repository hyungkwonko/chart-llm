# 1. hash 만들어서 unique한지 파악
# 2. JSON depth 구하기
# 3. key가지고 graph 만들기
# 4. average branching factor 구하기


import json
import hashlib
import math
import numpy as np
import pandas as pd
from glob import glob


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


def calculate_depth(data, level=0):
    if isinstance(data, dict):
        max_depth = level
        for key, value in data.items():
            depth = calculate_depth(value, level + 1)
            max_depth = max(max_depth, depth)
        return max_depth
    elif isinstance(data, list):
        max_depth = level
        for item in data:
            depth = calculate_depth(item, level + 1)
            max_depth = max(max_depth, depth)
        return max_depth
    else:
        return level


def extract_edges(data, parent=None, edges=None, i=1):
    if edges is None:
        edges = []

    if isinstance(data, dict):
        for key, value in data.items():
            node = (
                (f"{parent}!{i-1}", f"{key}!{i}")
                if parent is not None
                else ("root!0", f"{key}!{i}")
            )
            edges.append(node)
            edges = extract_edges(value, key, edges, i + 1)

    elif isinstance(data, list):
        for item in data:
            if isinstance(item, dict):
                edges = extract_edges(item, parent, edges, i + 1)

    return edges


def calculate_average_branching_factor(graph):
    num_nodes = len(set(sum(graph, ())))
    num_edges = len(graph)
    if num_nodes > 0:
        average_branching_factor = num_edges / num_nodes
        return average_branching_factor
    else:
        return 0


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

filter = pd.read_csv("./files/v6/csvfiles/keys.csv")

nlevels_all = []
abfs_all = []

for key in keys:
    filter_tmp = [
        x for x in list(filter[key]) if not (isinstance(x, float) and math.isnan(x))
    ]
    filter_tmp.extend(["datasets", "values"])

    if key == "q6_ours":
        files = glob("./files/v6/jsonfiles/d6/*.json")
        # files = ["./files/v6/jsonfiles/d6/vl_0004.vl.json"]
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

    nlevels = []
    abfs = []
    hashes = {}

    for i, file in enumerate(np.sort(files)):
        # print(f"progress... {i}")

        data, hash_value = get_hash(file)
        if hash_value not in hashes:
            # 1. hash 만들어서 unique한지 파악
            hashes[hash_value] = file
            data = filter_json(data, filter_tmp)

            # 2. JSON depth 구하기
            nlevel = calculate_depth(data)
            nlevels.append(nlevel)

            # 3. key가지고 graph 만들기
            edge_list = extract_edges(data)

            # 4. average branching factor 구하기
            abf = calculate_average_branching_factor(edge_list)
            abfs.append(abf)
        # else:
        #     print(f"{i}, {file}")

    nlevels_all.append(np.mean(nlevels))
    abfs_all.append(np.mean(abfs))

    print(
        f"key: {key}, len(files): {len(files)} len(hashes): {len(hashes)}, nested level: {np.mean(nlevels)}, Average Branching factor: {np.mean(abfs)}"
    )

out = pd.DataFrame()
out["key"] = keys
out["nested_level"] = nlevels_all
out["abf"] = abfs_all
out.to_csv("./files/v6/csvfiles/complexity.csv", index=False)
