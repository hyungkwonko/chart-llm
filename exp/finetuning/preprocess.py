import os
import pandas as pd
from sklearn.model_selection import train_test_split

os.makedirs("exp/finetuning/data", exist_ok=True)


def convert_save_jsonl(df, loc, cname):
    jsonl_data = df.apply(
        lambda x: {
            "prompt": x["commands"] + "\n\n###\n\n",
            "completion": x[cname] + " END",
        },
        axis=1,
    ).to_json(orient="records", lines=True)

    with open(loc, "w") as file:
        file.write(jsonl_data)


def get_data(loc, loc2, loc_train, loc_test, cname):
    data = pd.read_csv(loc)
    df = pd.DataFrame(data)

    selected_df = df[[cname, "commands"]]

    convert_save_jsonl(selected_df, loc2, cname)

    train, test = train_test_split(
        selected_df, test_size=0.1, random_state=42, stratify=selected_df[cname]
    )

    convert_save_jsonl(train, loc_train, cname)
    convert_save_jsonl(test, loc_test, cname)


if __name__ == "__main__":
    get_data(
        "exp/d2_utterance/nlv2_after.csv",
        "exp/finetuning/data/bm_all.jsonl",
        "exp/finetuning/data/bm.jsonl",
        "exp/finetuning/data/bm_test.jsonl",
        "visId",
    )

    get_data(
        "exp/d2_utterance/result/task4_selected_0.csv",
        "exp/finetuning/data/llmp_all.jsonl",
        "exp/finetuning/data/llmp.jsonl",
        "exp/finetuning/data/llmp_test.jsonl",
        "vids",
    )

    get_data(
        "exp/d2_utterance/result/task4_two_selected_0.csv",
        "exp/finetuning/data/llmp2_all.jsonl",
        "exp/finetuning/data/llmp2.jsonl",
        "exp/finetuning/data/llmp2_test.jsonl",
        "vids",
    )

    file1_df = pd.read_json("exp/finetuning/data/bm.jsonl", lines=True)
    file2_df = pd.read_json("exp/finetuning/data/llmp.jsonl", lines=True)
    file3_df = pd.read_json("exp/finetuning/data/llmp2.jsonl", lines=True)

    combined1_df = pd.concat([file1_df, file2_df])
    combined1_df.to_json(
        "exp/finetuning/data/bmllmp.jsonl", orient="records", lines=True
    )

    combined2_df = pd.concat([file1_df, file2_df, file3_df])
    combined2_df.to_json(
        "exp/finetuning/data/bmllmpllmp2.jsonl", orient="records", lines=True
    )

    half_len_file1 = len(file1_df) // 2
    half_len_file2 = len(file1_df) - half_len_file1

    combined_half_df = pd.concat(
        [file1_df.iloc[:half_len_file1], file2_df.iloc[:half_len_file2]]
    )

    combined_half_df.to_json(
        "exp/finetuning/data/half.jsonl", orient="records", lines=True
    )
