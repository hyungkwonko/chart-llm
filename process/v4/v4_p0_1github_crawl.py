from github import Github
import time
import pandas as pd
import math

per_page = 100

import os
from dotenv import load_dotenv

load_dotenv(".env")
github_key = os.getenv("GITHUB_KEY")


# Replace <token> with your personal access token
g = Github(
    github_key,
    per_page=per_page,
)

highs = ["encoding", "mark", "projection", "transform", "composition"]
lowss = [
    [
        "field",
        "type",
        "scale",
        "format",
        "axis",
        "value",
        "legend",
        "condition",
        "aggregate",
        "sort",
        "time",
        "unit",
        "datum",
        "stack",
        "bin",
        "header",
        "band",
        "impute",
    ],
    [
        "text",
        "line",
        "point",
        "bar",
        "geoshape",
        "circle",
        "rule",
        "area",
        "arc",
        "rect",
        "square",
        "tick",
        "boxplot",
        "image",
        "trail",
        "errorband",
        "errorbar",
    ],
    ["projection"],
    [
        "filter",
        "calculate",
        "lookup",
        "aggregate",
        "timeunit",
        "regression",
        "window",
        "fold",
        "stack",
        "pivot",
        "bin",
        "joinaggregate",
        "density",
        "flatten",
        "loess",
        "impute",
        "quantile",
        "sample",
    ],
    ["layer", "resolve", "repeat", "facet", "concat"],
]

for h_index, high in enumerate(highs):
    lows = lowss[h_index]

    for low in lows:
        if high == "projection":
            txt = f"{high}"
        elif high == "composition":
            txt = f"{low}"
        else:
            txt = f'{high}" "{low}'
        query1 = (
            '"schema": "https://vega.github.io/schema/vega-lite/v4" ".csv" "'
            # '"schema": "https://vega.github.io/schema/vega-lite/v5" ".csv" "'
            + txt
            + '" language:JSON -is:fork -user:vega'
        )
        query2 = (
            '"schema": "https://vega.github.io/schema/vega-lite/v4" "'
            # '"schema": "https://vega.github.io/schema/vega-lite/v5" "'
            + txt
            + '" language:JSON -is:fork -user:vega NOT ".csv"'
        )
        queries = [query1, query2]

        for ix, q in enumerate(queries):
            result = g.search_code(q)
            print(f"Q_{ix+1}_{low}: Number of searched items: {result.totalCount}")
            for i in range(math.ceil(result.totalCount / 100)):
                items = []
                for item in result.get_page(i):
                    print(item.html_url)
                    items.append(item.html_url)
                    time.sleep(1.0)
                df = pd.DataFrame(items, columns=["repo"])
                df.to_csv(
                    f"./files/v1/githubfiles/{high}_{low}_q{ix+1}_{i}.csv", index=False
                )
