import pandas as pd

json_file_path = "./population.json"
csv_file_path = "./population.csv"

df = pd.read_json(json_file_path)
df.to_csv(csv_file_path, index=False)
