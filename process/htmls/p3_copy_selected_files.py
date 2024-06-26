import os
import json
import pandas as pd

# path to the raw folder
raw_folder = "./files/htmls/jsonfiles/d0/"
select_folder = "./files/htmls/jsonfiles/d1/"

# path to the raw_select folder
os.makedirs(select_folder, exist_ok=True)

# list of filenames to be copied
df = pd.read_csv("./files/htmls/csvfiles/d2.csv")
df_index_0 = df["index_json_0"]

for i, index in enumerate(df_index_0):
    print(f"processing... {i} / {len(df_index_0)-1}")
    filename = raw_folder + "vl_" + str(index).zfill(4) + ".vl.json"
    new_file_name = select_folder + "vl_" + str(i).zfill(4) + ".vl.json"

    with open(filename, "r") as f:
        data = json.load(f)
        content = json.dumps(data, indent=2)

    with open(new_file_name, "w") as f:
        f.write(content)

print("saved all")
