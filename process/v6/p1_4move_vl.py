import os
import json
import pandas as pd

# path to the raw folder
raw_folder = "./files/vl/jsonfiles/"
select_folder = "./files/v6/jsonfiles/d5/"

# path to the raw_select folder
os.makedirs(select_folder, exist_ok=True)

# list of filenames to be copied
data = pd.read_csv("./files/vl/csvfiles/dv-all.csv")
data_version_folder = data["version_folder"]
data_index6 = data["index_6"]
data_index7 = data["index_7"]

for i, v in enumerate(data_version_folder):
    print(f"processing... {i} / {len(data_version_folder)-1}")
    filename = f"{raw_folder}{v}/vl_{str(data_index6[i]).zfill(4)}.vl.json"
    new_file_name = f"{select_folder}vl_{str(data_index7[i]).zfill(4)}.vl.json"

    with open(filename, "r") as f:
        data = json.load(f)
        content = json.dumps(data, indent=2)

    with open(new_file_name, "w") as f:
        f.write(content)

print("saved all")
