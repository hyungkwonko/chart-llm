import urllib.request
import pandas as pd
import time
import ssl
import os
import json

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)

# fname = "data-vl-d3"
fname = "data-v3-d4"
fname = "d0_v2"
foldername = "./files/v2v3vl/jsonfiles/d0_v2"

os.makedirs(foldername, exist_ok=True)

file = pd.read_csv(f"./files/v2v3vl/csvfiles/{fname}.csv")
urls = file["raw"]

print(f"Number of URLs: {len(urls)}")

for i, url in enumerate(urls):
    print(f"url_{i}: {url}")
    response = urllib.request.urlopen(url)
    content = response.read().decode("utf-8")

    json_content = json.loads(content)  # Convert content to JSON structure

    with open(f"{foldername}/vl_{str(i).zfill(4)}.vl.json", "w") as f:
        json.dump(json_content, f, indent=2)  # Save JSON content with an indent of 2

    time.sleep(0.1)
