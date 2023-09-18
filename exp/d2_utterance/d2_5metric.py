"""
Calculate across / with distribution metrics of paraphrased NL datasets

DATA_TYPE task4: Paraphrasing using one-axis
DATA_TYPE task4_two: Paraphrasing using two-axes
"""

import os
import ast
import numpy as np
import pandas as pd

from exp.analysis.compute_diversity import (
    embed_sentences,
    calculate_across_distance,
    calculate_within_distance,
)

np.random.seed(0)

DATA_TYPE = "task4"  # ["task4", "task4_two"]

D_LOC = os.path.join("exp", "d2_utterance", "nlv2_after.csv")
D2_LOC = os.path.join("exp", "d2_utterance", "result", "task2.csv")
D3_LOC = os.path.join("exp", "d2_utterance", "result", f"{DATA_TYPE}.csv")

N = 5

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
    original = df["commands"]
    emb1 = embed_sentences(original)

    within = calculate_within_distance(emb1)

    print(f"{within}")

    metrics["fds"].append(np.nan)
    metrics["precisions"].append(np.nan)
    metrics["recalls"].append(np.nan)
    metrics["remove_clique"].append(within[0])
    metrics["chamfer"].append(within[1])
    metrics["mst_dispersion"].append(within[2])
    metrics["span"].append(within[3])
    metrics["sparseness"].append(within[4])
    metrics["entropy"].append(within[5])

    df["concat"] = df["dataset"] + "-" + df["visId"] + "-" + df["Phrasing_Type"]
    df["count"] = df.groupby("concat")["concat"].transform("count")
    df = df[["dataset", "visId", "Phrasing_Type", "count"]].drop_duplicates()
    df["dataset"] = df["dataset"].str.lower()

    df2 = pd.read_csv(D2_LOC)
    df3 = pd.read_csv(D3_LOC)

    merged_df = pd.merge(
        df2,
        df[["dataset", "visId", "count", "Phrasing_Type"]],
        left_on=["dnames", "vids"],
        right_on=["dataset", "visId"],
        how="left",
    )

    merged_df = merged_df[
        ["command", "query", "question", "Phrasing_Type", "count", "dnames", "vids"]
    ].drop_duplicates()

    result = df2[["command", "query", "question"]].values.flatten().tolist()
    emb2 = embed_sentences(result)
    fd, precision, recall = calculate_across_distance(emb1, emb2, embedding=False)
    within2 = calculate_within_distance(emb2)

    print(
        f"===== len(result): {len(result)} fd: {fd}, precision: {precision}, recall: {recall}"
    )
    print(f"{within2}")

    for i in range(N):
        dfs = []

        for j, row in merged_df.iterrows():
            count = row["count"]
            dname = row["dnames"]
            vid = row["vids"]
            ptype = row["Phrasing_Type"]
            sentence = ast.literal_eval(row[ptype])[0]

            df_tmp = df3.loc[
                (df3["dnames"] == dname)
                & (df3["vids"] == vid)
                & (df3["ptypes"] == ptype)
            ]
            df_tmp = df_tmp.sample(n=count)
            dfs.append(df_tmp)

        result = pd.concat(dfs, axis=0, ignore_index=True)

        paraphrase = result["sentences"].tolist()
        emb2 = embed_sentences(paraphrase)
        within2 = calculate_within_distance(emb2)

        fd, precision, recall = calculate_across_distance(emb1, emb2)
        print(
            f"{i}, len(result): {len(result)}, fd: {fd}, precision: {precision}, recall: {recall}"
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

        result.to_csv(
            os.path.join(
                "exp", "d2_utterance", "result", f"{DATA_TYPE}_selected_{i}.csv"
            ),
            index=False,
        )

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
        os.path.join("exp", "d2_utterance", "result", f"{DATA_TYPE}_metrics.csv"),
        index=False,
    )
