import os
import ast
import pandas as pd

filename = os.path.join("exp", "d2_utterance", "nlv1_before.csv")
savename = os.path.join("exp", "d2_utterance", "nlv2_after.csv")


df_new = {
    "dataset": [],
    "visId": [],
    "commands": [],
    "count": [],
    "Sequence_Length": [],
    "Phrasing_Type": [],
}

if __name__ == "__main__":
    df = pd.read_csv(filename)

    datasets = df["dataset"].tolist()
    vidids = df["visId"].tolist()
    commands = df["commands"].tolist()
    counts = df["count"].tolist()
    seqlengths = df["Sequence_Length"].tolist()
    phrasetypes = df["Phrasing_Type"].tolist()

    for i, command in enumerate(commands):
        if df["Sequence_Length"][i] > 1:
            if not command.startswith("["):
                command = "[" + command
            if not command.endswith("]"):
                command = command + "]"
            my_list = ast.literal_eval(command)
            df_new["dataset"].extend([df["dataset"][i]] * df["Sequence_Length"][i])
            df_new["visId"].extend([df["visId"][i]] * df["Sequence_Length"][i])
            df_new["commands"].extend(my_list)
            df_new["count"].extend([df["count"][i]] * df["Sequence_Length"][i])
            df_new["Sequence_Length"].extend(
                [df["Sequence_Length"][i]] * df["Sequence_Length"][i]
            )
            df_new["Phrasing_Type"].extend(
                [df["Phrasing_Type"][i]] * df["Sequence_Length"][i]
            )
        else:
            if command.startswith("'"):
                command = "[" + command
            if not command.startswith("["):
                command = "['" + command
            if command.endswith(","):
                command = command + "]"
            my_list = ast.literal_eval(command)
            df_new["dataset"].extend([df["dataset"][i]])
            df_new["visId"].extend([df["visId"][i]])
            df_new["commands"].extend(my_list)
            df_new["count"].extend([df["count"][i]])
            df_new["Sequence_Length"].extend([df["Sequence_Length"][i]])
            df_new["Phrasing_Type"].extend([df["Phrasing_Type"][i]])

    df_new["commands"] = [x.strip() for x in df_new["commands"]]

    pd.DataFrame(df_new).to_csv(savename, index=False)
