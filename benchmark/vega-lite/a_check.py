from glob import glob

files = glob("*.json")

for file in files:
    if not file.endswith("vl.json"):
        print(file)

# test_minimal.json
# repeat_layer_size.json
# selection_layer.json --> selection_layer.vl.json
