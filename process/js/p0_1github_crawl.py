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

os.makedirs("./files/js/githubfiles/", exist_ok=True)

query1 = (
    '"https://vega.github.io/schema/vega-lite/v" "url" -is:fork -user:vega extension:js'
)
query2 = '"https://vega.github.io/schema/vega-lite/v" NOT "url" -is:fork -user:vega extension:js'
queries = [query1, query2]
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
        df.to_csv(f"./files/js/githubfiles/{ix}_{i}.csv", index=False)
