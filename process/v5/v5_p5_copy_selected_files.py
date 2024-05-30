import os
import shutil
import pandas as pd

# path to the raw folder
raw_folder = "./files/v1/jsonfiles/d6/"
select_folder = "./files/v1/jsonfiles/d7/"

# path to the raw_select folder
os.makedirs(select_folder, exist_ok=True)

# list of filenames to be copied
df = pd.read_csv("./files/v1/csvfiles/d7.csv")
df_index_0 = df["index_3"]
# df_index_3 = df["index_3"]

for i, index in enumerate(df_index_0):
    print(f"processing... {i} / {len(df_index_0)-1}")
    filename = raw_folder + "vl_" + str(index).zfill(4) + ".vl.json"
    new_file_name = select_folder + "vl_" + str(i).zfill(4) + ".vl.json"
    shutil.copy(filename, new_file_name)

print("saved all")
