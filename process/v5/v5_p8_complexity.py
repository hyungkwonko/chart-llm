import json
import hashlib
from glob import glob
import pandas as pd
import math
import numpy as np


def filter_json(json_data, keys):
    if isinstance(json_data, dict):
        # Sort keys in the dictionary
        sorted_data = {
            key: filter_json(value, keys) for key, value in json_data.items()
        }

        # Remove unwanted keys and their descendants
        filtered_data = {key: sorted_data[key] for key in sorted_data if key in keys}

        return filtered_data

    if isinstance(json_data, list):
        # Sort and filter each element in the list
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
        data = json.load(f)
        content = json.dumps(data, indent=4)
        content_encoded = content.encode()
        return data, hashlib.sha256(content_encoded).hexdigest()


filter = pd.read_csv("./files/v5/csvfiles/keys.csv")
keys = ["q1_visqa", "q2_data2vis", "q3_nvBench", "q4_vega-lite", "q5_ours"]

nlevels_all = []
abfs_all = []

for ix, key in enumerate(keys):
    filter_tmp = [
        x for x in list(filter[key]) if not (isinstance(x, float) and math.isnan(x))
    ]
    filter_tmp.append("root")

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

    nlevels = []
    abfs = []
    hashes = {}

    for i, file in enumerate(np.sort(files)):
        # print(f"progress... {index}")

        all_keys = []
        data, hash_value = get_hash(file)
        if hash_value in hashes:
            print(f"{i}, {file}")
        else:
            hashes[hash_value] = file
            data = filter_json(data, filter_tmp)

            # 1. JSON depth 구하기
            nlevel = calculate_depth(data)
            nlevels.append(nlevel)

            # 2. key가지고 graph 만들기
            edge_list = extract_edges(data)

            # 3. average branching factor 구하기
            abf = calculate_average_branching_factor(edge_list)
            abfs.append(abf)

    nlevels_all.append(np.mean(nlevels))
    abfs_all.append(np.mean(abfs))

    print(
        f"key: {key} \t\t nested level: {np.mean(nlevels)} \t\t Average Branching factor: {np.mean(abfs)}"
    )

out = pd.DataFrame()
out["key"] = keys
out["nested_level"] = nlevels_all
out["abf"] = abfs_all
out.to_csv("./files/v5/csvfiles/complexity.csv", index=False)
