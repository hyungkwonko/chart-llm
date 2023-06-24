import os
import json


# input_file = "./benchmark/chartseer/vegaspecs.txt"
input_file = "./benchmark/chartseer/vegaspecs-processed.txt"
output_dir = "./benchmark/chartseer/jsonfiles/"


with open(input_file, "r") as file:
    lines = file.readlines()

unique_lines = set(lines)

print(len(unique_lines))

os.makedirs(output_dir, exist_ok=True)

for i, line in enumerate(unique_lines):
    print(f"processing... {i} / {len(unique_lines) - 1}")
    filename = os.path.join(output_dir, f"output_{str(i).zfill(4)}.json")
    data = json.loads(line)
    with open(filename, "w") as file:
        json.dump(data, file, indent=2)
