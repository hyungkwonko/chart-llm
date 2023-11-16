"""
Paraphrase NL datasets of utterance datasets w/ one axis
"""

import os
import ast
import pandas as pd

from datetime import datetime
from dotenv import load_dotenv

from framework.utils import get_nl, AXES
from langchain.chat_models import ChatOpenAI


load_dotenv(".env")

D_LOC = os.path.join("exp", "d2_utterance", "result", "task2.csv")

MODELS = ["gpt-3.5-turbo-0613", "gpt-4-0613", "gpt-4-32k-0613"]

TEMPERATURE = 0.0

df_data = {
    "sentences": [],
    "axes": [],
    "ptypes": [],
    "dnames": [],
    "vids": [],
    "scores": [],
}


def gen_prompt(sent, axes):
    prompt = f"""
{axes[2]}

Score of 1 indicates a higher tendency to use {axes[0]} language and a Score of 5 indicates a higher tendency to use {axes[1]} language.
Rewrite the following sentence as if it were spoken by a person with a given score for language usage.

Sentence: {sent}

##
Score 1:
Score 2:
Score 3:
Score 4:
Score 5:
"""
    return prompt


def run_agent(sent, axes, model, temp=0.0):
    llm = ChatOpenAI(temperature=temp, model=model)
    return tuple(llm.predict(gen_prompt(sent, axes[i])) for i in range(4))


if __name__ == "__main__":
    df = pd.read_csv(D_LOC)

    for i, row in df.iterrows():
        num_ptypes = 3
        num_axes = len(AXES)  # 4
        num_score = 5
        count = num_axes * num_score  # axes 4, score 5

        command = ast.literal_eval(row["command"])[0]
        query = ast.literal_eval(row["query"])[0]
        question = ast.literal_eval(row["question"])[0]
        dname = row["dnames"]
        vid = row["vids"]

        df_data["ptypes"].extend(
            ["command"] * count + ["query"] * count + ["question"] * count
        )
        df_data["dnames"].extend([row["dnames"]] * count * num_ptypes)
        df_data["vids"].extend([row["vids"]] * count * num_ptypes)
        df_data["scores"].extend([1, 2, 3, 4, 5] * num_axes * num_ptypes)

        axes_data = []
        for _ in range(num_ptypes):
            for j in range(num_axes):
                axes_data.extend([f"{AXES[j][0]}-{AXES[j][1]}"] * num_score)

        df_data["axes"].extend(axes_data)

        for sent in [command, query, question]:
            print(f"{i}: command/query/question: {sent}")
            out = run_agent(sent, AXES, model=MODELS[1], temp=TEMPERATURE)
            for k, o in enumerate(out):
                # print(f"AXES: {AXES[k][0]}-{AXES[k][1]}\n{o}")
                df_data["sentences"].append(get_nl(o, pattern=r"Score 1:(.+?)(?:\n|$)"))
                df_data["sentences"].append(get_nl(o, pattern=r"Score 2:(.+?)(?:\n|$)"))
                df_data["sentences"].append(get_nl(o, pattern=r"Score 3:(.+?)(?:\n|$)"))
                df_data["sentences"].append(get_nl(o, pattern=r"Score 4:(.+?)(?:\n|$)"))
                df_data["sentences"].append(get_nl(o, pattern=r"Score 5:(.+?)(?:\n|$)"))
                # print(f"len(df_data['sentences']): {len(df_data['sentences'])}")

        df = pd.DataFrame(df_data)
        df.to_csv(
            os.path.join(
                "exp",
                "d2_utterance",
                "result",
                f"task4_tmp_{datetime.now()}.csv",
            ),
            index=False,
        )

    df = pd.DataFrame(df_data)
    df.to_csv(os.path.join("exp", "d2_utterance", "result", "task4.csv"), index=False)
