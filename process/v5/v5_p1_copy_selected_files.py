import os
import shutil
import pandas as pd

# path to the raw folder
raw_folder = "./files/v0/jsonfiles/d2/"
select_folder = "./files/v1/jsonfiles/d5/"

# path to the raw_select folder
os.makedirs(select_folder, exist_ok=True)


# list of filenames to be copied
d4 = pd.read_csv("./files/v1/csvfiles/d4.csv")
d4_index_0 = d4["index_0"]
# d4_index_2 = d4["index_2"]

for i, index in enumerate(d4_index_0):
    print(f"processing... {i} / {len(d4_index_0)-1}")
    filename = raw_folder + "file_" + str(index).zfill(4) + ".json"
    new_file_name = select_folder + "vl_" + str(i).zfill(4) + ".vl.json"
    shutil.copy(filename, new_file_name)

print("saved all")
