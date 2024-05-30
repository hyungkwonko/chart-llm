import urllib.request
import pandas as pd
import time
import ssl

ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLSv1_2)

file = pd.read_csv("./files/v4/csvfiles/datav4-d3.csv")
urls = file["raw"]

print(f"Number of URLs: {len(urls)}")

for i, url in enumerate(urls):
    # if i < 7116:
    #     continue
    print(f"url_{i}: {url}")
    response = urllib.request.urlopen(url)
    content = response.read().decode("utf-8")
    with open(f"./files/v4/jsonfiles/d3all/vl_{str(i).zfill(4)}.vl.json", "w") as f:
        f.write(content)
    time.sleep(0.1)
