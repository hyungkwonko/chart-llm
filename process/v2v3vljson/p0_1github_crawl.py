from github import Github
import time
import pandas as pd
import math
import os

per_page = 100

from dotenv import load_dotenv

load_dotenv(".env")
github_key = os.getenv("GITHUB_KEY")

# Replace <token> with your personal access token
g = Github(
    github_key,
    per_page=per_page,
)

os.makedirs("./files/v2v3vl/githubfiles/", exist_ok=True)

# query1 = '"schema": "https://vega.github.io/schema/vega-lite/v3" language:JSON -is:fork -user:vega'
# query2 = '"schema": "https://vega.github.io/schema/vega-lite/v2" language:JSON -is:fork -user:vega'
query1 = '"https://vega.github.io/schema/vega-lite/v3" "url" -is:fork -user:vega language:JSON -extension:vl.json'
query2 = '"https://vega.github.io/schema/vega-lite/v3" NOT "url" -is:fork -user:vega language:JSON -extension:vl.json'
query3 = '"https://vega.github.io/schema/vega-lite/v2" "url" -is:fork -user:vega language:JSON -extension:vl.json'
query4 = '"https://vega.github.io/schema/vega-lite/v2" NOT "url" -is:fork -user:vega language:JSON -extension:vl.json'
query5 = 'extension:vl.json -is:fork -user:vega NOT "$schema"'
queries = [query1, query2, query3, query4]
# queries = [query1, query3]

for ix, q in enumerate(queries):
    print(q)
    result = g.search_code(q)
    if ("v3" in q) and ("NOT" in q):
        name = "v3_no_url"
    elif "v3" in q and "NOT" not in q:
        name = "v3_url"
    elif ("v2" in q) and ("NOT" in q):
        name = "v2_no_url"
    elif "v2" in q and "NOT" not in q:
        name = "v2_url"
    else:
        name = "vl"

    print(f"{name}: Number of searched items: {result.totalCount}")

    for i in range(math.ceil(result.totalCount / 100)):
        items = []
        for item in result.get_page(i):
            print(item.html_url)
            items.append(item.html_url)
            time.sleep(0.7)
        df = pd.DataFrame(items, columns=["repo"])
        df.to_csv(f"./files/v2v3vl/githubfiles/{name}_{i}.csv", index=False)
