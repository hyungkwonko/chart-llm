# compute the number of composite views which has the keys in COMPOSITE_KEYS

import json
import json
import numpy as np
from glob import glob
import pandas as pd


COMPOSITE_KEYS = ["layer", "facet", "concat", "repeat", "resolve", "vconcat", "hconcat"]
# COMPOSITE_KEYS = ["facet", "concat", "repeat", "resolve", "vconcat", "hconcat"]
COMPOSITE_LAYERS = ["layer"]

name = "ours"
file_list = glob("./files/v6/jsonfiles/d6/*.json")
file_list = np.sort(file_list)

# name = "gallery"
# file_list = glob("./benchmark/vega-lite/*.vl.json")

composite = []
composite_layer = []
print(f"len: {len(file_list)}")


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


for i, file in enumerate(file_list):
    with open(file, "r") as f:
        data = json.load(f)
    file_out = get_all_keys(data)

    if any(key in file_out for key in COMPOSITE_KEYS):
        composite.append(True)
    else:
        composite.append(False)

    if any(key in file_out for key in COMPOSITE_LAYERS):
        composite_layer.append(True)
    else:
        composite_layer.append(False)

    print(f"progress... {file}... {composite[-1]}...{sum(composite)}")


out = pd.DataFrame()
out["file_list"] = file_list
out["composite_key"] = composite
out["composite_layer"] = composite_layer
out.to_csv(f"./files/v6/csvfiles/composite-{name}.csv", index=False)
