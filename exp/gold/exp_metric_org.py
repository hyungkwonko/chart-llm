"""
Calculate across / with distribution metrics of LLM-generated NL datasets
"""

import os

import numpy as np
import pandas as pd

from exp.analysis.compute_diversity import (
    embed_sentences,
    calculate_across_distance,
    calculate_within_distance,
)

np.random.seed(0)

N = 5
DATA_TYPE = "task2_original"  # [""task2_original", "task3_original"]

D_LOC = os.path.join("exp", "gold", "result", "gold.csv")
D2_LOC = os.path.join("framework", "result", f"task2.csv")
D3_LOC = os.path.join("framework", "result", f"task3.csv")


metrics = {
    "fds": [],
    "precisions": [],
    "recalls": [],
    "remove_clique": [],
    "chamfer": [],
    "mst_dispersion": [],
    "span": [],
    "sparseness": [],
    "entropy": [],
}

if __name__ == "__main__":
    df = pd.read_csv(D_LOC)
    if DATA_TYPE == "task2_original":
        cols = ["command", "query", "question"]
        original = df.loc[:, cols].values.ravel().tolist()
        df2 = pd.read_csv(D2_LOC)
        cols2 = ["commands", "queries", "questions"]
        paraphrase = df2.loc[:, cols2].values.ravel().tolist()
    else:
        cols = [
            "lookup-nonvisual",
            "lookup-visual",
            "compositional-nonvisual",
            "compositional-visual",
            "open-ended",
        ]
        original = df.loc[:, cols].values.ravel().tolist()
        df2 = pd.read_csv(D3_LOC)
        paraphrase = df2.loc[:, cols].values.ravel().tolist()

    emb1 = embed_sentences(original)
    within = calculate_within_distance(emb1)

    metrics["fds"].append(np.nan)
    metrics["precisions"].append(np.nan)
    metrics["recalls"].append(np.nan)
    metrics["remove_clique"].append(within[0])
    metrics["chamfer"].append(within[1])
    metrics["mst_dispersion"].append(within[2])
    metrics["span"].append(within[3])
    metrics["sparseness"].append(within[4])
    metrics["entropy"].append(within[5])
    print(f"len(original): {len(original)}: {within}")

    emb2 = embed_sentences(paraphrase)

    fd, precision, recall = calculate_across_distance(emb1, emb2, embedding=False)
    within2 = calculate_within_distance(emb2)

    print(
        f"len(paraphrase): {len(paraphrase)}, fd: {fd}, precision: {precision}, recall: {recall}"
    )
    print(f"{within2}")

    metrics["fds"].append(fd)
    metrics["precisions"].append(precision)
    metrics["recalls"].append(recall)
    metrics["remove_clique"].append(within2[0])
    metrics["chamfer"].append(within2[1])
    metrics["mst_dispersion"].append(within2[2])
    metrics["span"].append(within2[3])
    metrics["sparseness"].append(within2[4])
    metrics["entropy"].append(within2[5])

    metrics = pd.DataFrame(metrics)
    metrics.to_csv(
        os.path.join(
            "exp",
            "gold",
            "result",
            f"metrics_{DATA_TYPE}.csv",
        ),
        index=False,
    )
