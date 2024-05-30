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

os.makedirs("./files/htmls/githubfiles/", exist_ok=True)

query1 = (
    '"https://vega.github.io/schema/vega-lite/v2" AND .csv language:html -user:vega'
)
query2 = '"https://vega.github.io/schema/vega-lite/v2" AND "values": [ language:html -user:vega'
query3 = (
    '"https://vega.github.io/schema/vega-lite/v3" AND .csv language:html -user:vega'
)
query4 = '"https://vega.github.io/schema/vega-lite/v3" AND "values": [ language:html -user:vega'
query5 = (
    '"https://vega.github.io/schema/vega-lite/v4" AND .csv language:html -user:vega'
)
query6 = '"https://vega.github.io/schema/vega-lite/v4" AND "values": [ language:html -user:vega'
query7 = (
    '"https://vega.github.io/schema/vega-lite/v5" AND .csv language:html -user:vega'
)
query8 = '"https://vega.github.io/schema/vega-lite/v5" AND "values": [ language:html -user:vega'
queries = [query1, query2, query3, query4, query5, query6, query7, query8]

for ix, q in enumerate(queries):
    result = g.search_code(q)

    print(f"Number of searched items: {result.totalCount}: {q}")

    for i in range(math.ceil(result.totalCount / 100)):
        items = []
        for item in result.get_page(i):
            print(item.html_url)
            items.append(item.html_url)
            time.sleep(0.7)
        df = pd.DataFrame(items, columns=["repo"])
        df.to_csv(f"./files/htmls/githubfiles/{ix}_{i}.csv", index=False)
