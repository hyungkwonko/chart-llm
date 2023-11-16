"""
Paraphrase NL datasets of utterance datasets w/ two axes
"""

import os
import ast
import pandas as pd

from datetime import datetime
from dotenv import load_dotenv

from framework.utils import get_nl, AXES
from langchain.chat_models import ChatOpenAI

from itertools import combinations


load_dotenv(".env")

D_LOC = os.path.join("exp", "d2_utterance", "result", "task2.csv")
MODELS = ["gpt-3.5-turbo-0613", "gpt-4-0613", "gpt-4-32k-0613"]

df_data = {
    "sentences": [],
    "axes": [],
    "axes2": [],
    "ptypes": [],
    "dnames": [],
    "vids": [],
    "scores": [],
    "scores2": [],
}


def gen_prompt(sent, axes):
    prompt = f"""
{axes[0][2]}
{axes[1][2]}
Score-A of 1 indicates a higher tendency to use {axes[0][0]} language and a Score-A of 5 indicates a higher tendency to use {axes[0][1]} language.
Score-B of 1 indicates a higher tendency to use {axes[1][0]} language and a Score-B of 5 indicates a higher tendency to use {axes[1][1]} language.
Rewrite the following sentence as if it were spoken by a person with a given score for language usage.

Sentence: {sent}

##
Score-A 1, Score-B 1:
Score-A 1, Score-B 2:
Score-A 1, Score-B 3:
Score-A 1, Score-B 4:
Score-A 1, Score-B 5:

Score-A 2, Score-B 1:
Score-A 2, Score-B 2:
Score-A 2, Score-B 3:
Score-A 2, Score-B 4:
Score-A 2, Score-B 5:

Score-A 3, Score-B 1:
Score-A 3, Score-B 2:
Score-A 3, Score-B 3:
Score-A 3, Score-B 4:
Score-A 3, Score-B 5:

Score-A 4, Score-B 1:
Score-A 4, Score-B 2:
Score-A 4, Score-B 3:
Score-A 4, Score-B 4:
Score-A 4, Score-B 5:

Score-A 5, Score-B 1:
Score-A 5, Score-B 2:
Score-A 5, Score-B 3:
Score-A 5, Score-B 4:
Score-A 5, Score-B 5:
"""
    return prompt


def run_agent(sent, axes_list, model, temp=0.0):
    llm = ChatOpenAI(temperature=temp, model=model)
    return tuple(llm.predict(gen_prompt(sent, axes)) for axes in axes_list)


if __name__ == "__main__":
    df = pd.read_csv(D_LOC)

    for i, row in df.iterrows():
        num_ptypes = 3
        num_axes = 6  # 4C2
        num_score = 25
        count = num_axes * num_score  # axes 6, score 25

        command = ast.literal_eval(row["command"])[0]
        query = ast.literal_eval(row["query"])[0]
        question = ast.literal_eval(row["question"])[0]
        dname = row["dnames"]
        vid = row["vids"]

        df_data["ptypes"].extend(
            ["command"] * count + ["query"] * count + ["question"] * count
        )
        df_data["dnames"].extend([row["dnames"]] * num_ptypes * count)
        df_data["vids"].extend([row["vids"]] * num_ptypes * count)
        df_data["scores"].extend([1, 2, 3, 4, 5] * 5 * num_ptypes * num_axes)
        df_data["scores2"].extend(
            [1, 1, 1, 1, 1, 2, 2, 2, 2, 2, 3, 3, 3, 3, 3, 4, 4, 4, 4, 4, 5, 5, 5, 5, 5]
            * num_ptypes
            * num_axes
        )

        axes_list = list(combinations(AXES, 2))

        axes_data = []
        axes_data2 = []
        for _ in range(num_ptypes):
            for axes_l in axes_list:
                axes_data.extend([f"{axes_l[0][0]}-{axes_l[0][1]}"] * num_score)
                axes_data2.extend([f"{axes_l[1][0]}-{axes_l[1][1]}"] * num_score)
        df_data["axes"].extend(axes_data)
        df_data["axes2"].extend(axes_data2)

        for sent in [command, query, question]:
            print(f"{i}: command/query/question: {sent}")
            out = run_agent(sent, axes_list, model=MODELS[1])
            for k, o in enumerate(out):
                df_data["sentences"].append(
                    get_nl(o, pattern=r"Score-A 1, Score-B 1:(.+?)(?:\n|$)")
                )
                df_data["sentences"].append(
                    get_nl(o, pattern=r"Score-A 1, Score-B 2:(.+?)(?:\n|$)")
                )
                df_data["sentences"].append(
                    get_nl(o, pattern=r"Score-A 1, Score-B 3:(.+?)(?:\n|$)")
                )
                df_data["sentences"].append(
                    get_nl(o, pattern=r"Score-A 1, Score-B 4:(.+?)(?:\n|$)")
                )
                df_data["sentences"].append(
                    get_nl(o, pattern=r"Score-A 1, Score-B 5:(.+?)(?:\n|$)")
                )

                df_data["sentences"].append(
                    get_nl(o, pattern=r"Score-A 2, Score-B 1:(.+?)(?:\n|$)")
                )
                df_data["sentences"].append(
                    get_nl(o, pattern=r"Score-A 2, Score-B 2:(.+?)(?:\n|$)")
                )
                df_data["sentences"].append(
                    get_nl(o, pattern=r"Score-A 2, Score-B 3:(.+?)(?:\n|$)")
                )
                df_data["sentences"].append(
                    get_nl(o, pattern=r"Score-A 2, Score-B 4:(.+?)(?:\n|$)")
                )
                df_data["sentences"].append(
                    get_nl(o, pattern=r"Score-A 2, Score-B 5:(.+?)(?:\n|$)")
                )

                df_data["sentences"].append(
                    get_nl(o, pattern=r"Score-A 3, Score-B 1:(.+?)(?:\n|$)")
                )
                df_data["sentences"].append(
                    get_nl(o, pattern=r"Score-A 3, Score-B 2:(.+?)(?:\n|$)")
                )
                df_data["sentences"].append(
                    get_nl(o, pattern=r"Score-A 3, Score-B 3:(.+?)(?:\n|$)")
                )
                df_data["sentences"].append(
                    get_nl(o, pattern=r"Score-A 3, Score-B 4:(.+?)(?:\n|$)")
                )
                df_data["sentences"].append(
                    get_nl(o, pattern=r"Score-A 3, Score-B 5:(.+?)(?:\n|$)")
                )

                df_data["sentences"].append(
                    get_nl(o, pattern=r"Score-A 4, Score-B 1:(.+?)(?:\n|$)")
                )
                df_data["sentences"].append(
                    get_nl(o, pattern=r"Score-A 4, Score-B 2:(.+?)(?:\n|$)")
                )
                df_data["sentences"].append(
                    get_nl(o, pattern=r"Score-A 4, Score-B 3:(.+?)(?:\n|$)")
                )
                df_data["sentences"].append(
                    get_nl(o, pattern=r"Score-A 4, Score-B 4:(.+?)(?:\n|$)")
                )
                df_data["sentences"].append(
                    get_nl(o, pattern=r"Score-A 4, Score-B 5:(.+?)(?:\n|$)")
                )

                df_data["sentences"].append(
                    get_nl(o, pattern=r"Score-A 5, Score-B 1:(.+?)(?:\n|$)")
                )
                df_data["sentences"].append(
                    get_nl(o, pattern=r"Score-A 5, Score-B 2:(.+?)(?:\n|$)")
                )
                df_data["sentences"].append(
                    get_nl(o, pattern=r"Score-A 5, Score-B 3:(.+?)(?:\n|$)")
                )
                df_data["sentences"].append(
                    get_nl(o, pattern=r"Score-A 5, Score-B 4:(.+?)(?:\n|$)")
                )
                df_data["sentences"].append(
                    get_nl(o, pattern=r"Score-A 5, Score-B 5:(.+?)(?:\n|$)")
                )

        df = pd.DataFrame(df_data)
        df.to_csv(
            os.path.join(
                "exp", "d2_utterance", "result", f"task4_two_tmp_{datetime.now()}.csv"
            ),
            index=False,
        )

    df = pd.DataFrame(df_data)
    df.to_csv(
        os.path.join("exp", "d2_utterance", "result", "task4_two.csv"), index=False
    )
