from github import Github
import time
import pandas as pd
import math
import os

from dotenv import load_dotenv

load_dotenv(".env")
github_key = os.getenv("GITHUB_KEY")

per_page = 100

# Replace <token> with your personal access token
g = Github(
    github_key,
    per_page=per_page,
)

os.makedirs("./files/vgvgjson/githubfiles/", exist_ok=True)

query1 = '"https://vega.github.io/schema/vega-lite/v" -is:fork -user:vega extension:vg'
query2 = '"https://vega.github.io/schema/vega-lite/v5" NOT "url" -is:fork -user:vega extension:vg.json'
query3 = '"https://vega.github.io/schema/vega-lite/v5" "url" -is:fork -user:vega extension:vg.json'
query4 = (
    '"https://vega.github.io/schema/vega-lite/v4" -is:fork -user:vega extension:vg.json'
)
query5 = (
    '"https://vega.github.io/schema/vega-lite/v3" -is:fork -user:vega extension:vg.json'
)
query6 = (
    '"https://vega.github.io/schema/vega-lite/v2" -is:fork -user:vega extension:vg.json'
)
# query5 = 'extension:vl -is:fork -user:vega NOT "$schema"'
queries = [query1, query2, query3, query4, query5, query6]
# queries = [query1, query3]

for ix, q in enumerate(queries):
    print(q)
    result = g.search_code(q)

    print(f"{ix}: Number of searched items: {result.totalCount}")

    for i in range(math.ceil(result.totalCount / 100)):
        items = []
        for item in result.get_page(i):
            print(item.html_url)
            items.append(item.html_url)
            time.sleep(0.7)
        df = pd.DataFrame(items, columns=["repo"])
        df.to_csv(f"./files/vgvgjson/githubfiles/{ix}_{i}.csv", index=False)
