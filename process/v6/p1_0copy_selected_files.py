import os
import json
import pandas as pd

# path to the raw folder
raw_folder_v4 = "./files/v4/jsonfiles/d8/"
raw_folder_v5 = "./files/v5/jsonfiles/d7/"
select_folder = "./files/v6/jsonfiles/d1/"

# path to the raw_select folder
os.makedirs(select_folder, exist_ok=True)

# list of filenames to be copied
data = pd.read_csv("./files/v6/csvfiles/d1.csv")
data_version = data["version"]
data_index = data["index_6"]

for i, v in enumerate(data_version):
    print(f"processing... {i} / {len(data_version)-1}")
    if v == "v4":
        filename = raw_folder_v4 + "vl_" + str(data_index[i]).zfill(4) + ".vl.json"
    else:
        filename = raw_folder_v5 + "vl_" + str(data_index[i]).zfill(4) + ".vl.json"

    new_file_name = select_folder + "vl_" + str(i).zfill(4) + ".vl.json"

    with open(filename, "r") as f:
        data = json.load(f)
        content = json.dumps(data, indent=2)

    with open(new_file_name, "w") as f:
        f.write(content)

print("saved all")
