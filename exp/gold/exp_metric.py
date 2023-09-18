"""
Calculate across / with distribution metrics of paraphrased NL datasets

TASK_TYPE 2: Utterance (Command, Query, Question)
TASK_TYPE 3: Question (Visual/Non-visual, Lookup/Compositional, Open-ended)

DATA_TYPE task4: Paraphrasing using one-axis
DATA_TYPE task4_two: Paraphrasing using two-axes
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
DATA_TYPE = "task4"  # ["task4", "task4_two"]
TASK_TYPE = 2  # [2, 3]

D_LOC = os.path.join("exp", "gold", "result", "gold.csv")
D2_LOC = os.path.join("exp", "gold", "result", f"{DATA_TYPE}_{TASK_TYPE}_selected.csv")

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
    if TASK_TYPE == 2:
        original = df.loc[:, ["command", "query", "question"]].values.ravel().tolist()
    else:
        original = (
            df.loc[
                :,
                [
                    "lookup-nonvisual",
                    "lookup-visual",
                    "compositional-nonvisual",
                    "compositional-visual",
                    "open-ended",
                ],
            ]
            .values.ravel()
            .tolist()
        )

    emb1 = embed_sentences(original)
    within = calculate_within_distance(emb1)

    print(f"len(original): {len(original)}: {within}")

    metrics["fds"].append(np.nan)
    metrics["precisions"].append(np.nan)
    metrics["recalls"].append(np.nan)
    metrics["remove_clique"].append(within[0])
    metrics["chamfer"].append(within[1])
    metrics["mst_dispersion"].append(within[2])
    metrics["span"].append(within[3])
    metrics["sparseness"].append(within[4])
    metrics["entropy"].append(within[5])

    df2 = pd.read_csv(D2_LOC)
    df2 = df2["paraphrases"].tolist()
    size = len(df2) // N

    for i in range(N):
        paraphrase = df2[i * size : (i + 1) * size]
        emb2 = embed_sentences(paraphrase)

        fd, precision, recall = calculate_across_distance(emb1, emb2, embedding=False)
        within2 = calculate_within_distance(emb2)

        print(
            f"{i}, len(paraphrase): {len(paraphrase)}, fd: {fd}, precision: {precision}, recall: {recall}"
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

    metrics["fds"].append(np.mean(metrics["fds"][1:]))
    metrics["precisions"].append(np.mean(metrics["precisions"][1:]))
    metrics["recalls"].append(np.mean(metrics["recalls"][1:]))
    metrics["remove_clique"].append(np.mean(metrics["remove_clique"][1:]))
    metrics["chamfer"].append(np.mean(metrics["chamfer"][1:]))
    metrics["mst_dispersion"].append(np.mean(metrics["mst_dispersion"][1:]))
    metrics["span"].append(np.mean(metrics["span"][1:]))
    metrics["sparseness"].append(np.mean(metrics["sparseness"][1:]))
    metrics["entropy"].append(np.mean(metrics["entropy"][1:]))

    metrics["fds"].append(np.std(metrics["fds"][1:]))
    metrics["precisions"].append(np.std(metrics["precisions"][1:]))
    metrics["recalls"].append(np.std(metrics["recalls"][1:]))
    metrics["remove_clique"].append(np.std(metrics["remove_clique"][1:]))
    metrics["chamfer"].append(np.std(metrics["chamfer"][1:]))
    metrics["mst_dispersion"].append(np.std(metrics["mst_dispersion"][1:]))
    metrics["span"].append(np.std(metrics["span"][1:]))
    metrics["sparseness"].append(np.std(metrics["sparseness"][1:]))
    metrics["entropy"].append(np.std(metrics["entropy"][1:]))

    metrics = pd.DataFrame(metrics)
    metrics.to_csv(
        os.path.join(
            "exp",
            "gold",
            "result",
            f"metrics_{DATA_TYPE}_{TASK_TYPE}.csv",
        ),
        index=False,
    )
