import re
from glob import glob
import json

pattern = r"vlSpec1\s\s*=\s*({.*?});"

filenames = glob("./nvBench_VegaLite/*.html")

for (
    i,
    filename,
) in enumerate(filenames):
    with open(f"{filename}", "r") as file:
        html_content = file.read()

    match = re.search(pattern, html_content, re.DOTALL)

    if match:
        # Retrieve the specific text
        data = match.group(1)
        data = data.replace("'", '"')
        # print(data)
        data = json.loads(data)
        outname = filename.replace("./VIS_", "").replace(".html", "")
        with open(f"./vega/vega_{outname.zfill(4)}.vg.json", "w") as file:
            json.dump(data, file)
        print(f"progres... {filename}, {outname}")
    else:
        print("Pattern not found.")
        exit()
