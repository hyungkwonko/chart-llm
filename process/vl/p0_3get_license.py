import requests
import json
import pandas as pd
import time
import numpy as np

import os
from dotenv import load_dotenv

load_dotenv(".env")
github_key = os.getenv("GITHUB_KEY")

headers = {"Authorization": f"token {github_key}"}

version = "vl"

df = pd.read_csv(f"./files/vl/csvfiles/vl-d2.csv")
urls = df["url"]

xs = []

for i, url in enumerate(urls):
    txt = url.split("/")
    owner = txt[3]
    repo = txt[4]
    x = owner + "/" + repo
    xs.append(x)

mysets = np.sort(list(set(xs)))

print(f"len(xs): {len(xs)}, len(list(set(xs))): {len(list(set(xs)))}")

license_keys = []
license_urls = []

for i, myset in enumerate(mysets):
    time.sleep(2.0)

    txt = myset.split("/")
    owner = txt[0]
    repo = txt[1]

    url = f"https://api.github.com/repos/{owner}/{repo}/license"

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = json.loads(response.text)
        license_key = data["license"]["key"]
        license_url = data["license"]["url"]
        license_keys.append(license_key)
        license_urls.append(license_url)
        print(f"{i},{owner},{repo},{data['license']['key']},{data['license']['url']}")
    else:
        license_keys.append("none")
        license_urls.append("none")
        print(f"{i},{owner},{repo},{response.status_code},{response.status_code}")

df2 = pd.DataFrame()

df2["owner_repo"] = mysets
df2["license_key"] = license_keys
df2["license_url"] = license_urls
df2.to_csv(f"./files/vl/csvfiles/data-{version}-d2-license.csv", index=False)
print("file saved")
