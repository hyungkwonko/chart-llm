"""
Paraphrase NL datasets of gold standard datasets

TASK_TYPE 2: Utterance (Command, Query, Question)
TASK_TYPE 3: Question (Visual/Non-visual, Lookup/Compositional, Open-ended)

DATA_TYPE task4: Paraphrasing using one-axis
DATA_TYPE task4_two: Paraphrasing using two-axes
"""

import os
import ast
import random
import numpy as np
import pandas as pd

from dotenv import load_dotenv
from framework.utils import get_nl, AXES
from langchain.chat_models import ChatOpenAI

np.random.seed(0)

load_dotenv(".env")

N = 5
MODELS = ["gpt-3.5-turbo-0613", "gpt-4-0613", "gpt-4-32k-0613"]
DATA_TYPE = "task4"  # ["task4", "task4_two"]
TASK_TYPE = 2  # [2, 3]

D_LOC = {
    1: os.path.join("framework", "result", "task1.csv"),
    2: os.path.join("framework", "result", "task2.csv"),
    3: os.path.join("framework", "result", "task3.csv"),
}

COLS = {
    1: ["L1", "L2", "L3"],
    2: ["commands", "queries", "questions"],
    3: [
        "lookup-nonvisual",
        "lookup-visual",
        "compositional-nonvisual",
        "compositional-visual",
        "open-ended",
    ],
}

DATA_LIST = {
    "task4": {
        "paraphrases": [],
        "sentences": [],
        "ptypes": [],
        "axes": [],
        "scores": [],
    },
    "task4_two": {
        "paraphrases": [],
        "sentences": [],
        "ptypes": [],
        "axes": [],
        "axes2": [],
        "scores": [],
        "scores2": [],
    },
}


def gen_prompt(sent, axes, score):
    prompt = f"""
{axes[0][2]}

Score of 1 indicates a higher tendency to use {axes[0][0]} language and a Score of 5 indicates a higher tendency to use {axes[0][1]} language.
Rewrite the following sentence as if it were spoken by a person with a given score for language usage.

Sentence: {sent}

##
Score {score}:
"""
    return prompt


def gen_prompt2(sent, axes, score, score2):
    prompt = f"""
{axes[0][2]}
{axes[1][2]}
Score-A of 1 indicates a higher tendency to use {axes[0][0]} language and a Score-A of 5 indicates a higher tendency to use {axes[0][1]} language.
Score-B of 1 indicates a higher tendency to use {axes[1][0]} language and a Score-B of 5 indicates a higher tendency to use {axes[1][1]} language.
Rewrite the following sentence as if it were spoken by a person with a given score for language usage.

Sentence: {sent}

##
Score-A {score}, Score-B {score2}:
"""
    return prompt


def run_agent(sent, axes, score, score2=-1, model=MODELS[1], temp=0.0):
    llm = ChatOpenAI(temperature=temp, model=model)
    if score2 > 0:
        prompt = gen_prompt2(sent, axes, score, score2)
    else:
        prompt = gen_prompt(sent, axes, score)
    return llm.predict(prompt)


if __name__ == "__main__":
    df = pd.read_csv(D_LOC[TASK_TYPE])
    df = df[COLS[TASK_TYPE]].drop_duplicates()

    for i in range(N):
        dlist = DATA_LIST[DATA_TYPE]
        # if i < 1:
        #     continue
        if DATA_TYPE == "task4":
            for j, row in df.iterrows():
                for col in COLS[TASK_TYPE]:
                    score = random.randint(1, 5)
                    if TASK_TYPE == 2:
                        sent_list = ast.literal_eval(row[col])
                        sent = " ".join(sent_list)
                    else:
                        sent = row[col]
                    axe = random.sample(AXES, 1)

                    dlist["sentences"].append(sent)
                    dlist["axes"].append(axe)
                    dlist["ptypes"].append(col)
                    dlist["scores"].append(score)

                    out = run_agent(sent, axe, score, model=MODELS[1])
                    # out = get_nl(out, pattern=r"Score [1-5]:(.+?)(?:\n|$)")
                    dlist["paraphrases"].append(out)

                    print(f"{i}-{j}: {sent}")

                result = pd.DataFrame(dlist)
                result.to_csv(
                    os.path.join(
                        "exp",
                        "gold",
                        "result",
                        f"{DATA_TYPE}_{TASK_TYPE}_selected_tmp.csv",
                    ),
                    index=False,
                )

        else:
            for j, row in df.iterrows():
                for col in COLS[TASK_TYPE]:
                    score = random.randint(1, 5)
                    score2 = random.randint(1, 5)
                    if TASK_TYPE == 2:
                        sent_list = ast.literal_eval(row[col])
                        sent = " ".join(sent_list)
                    else:
                        sent = row[col]
                    axe = random.sample(AXES, 2)

                    dlist["sentences"].append(sent)
                    dlist["axes"].append(axe[0])
                    dlist["axes2"].append(axe[1])
                    dlist["ptypes"].append(col)
                    dlist["scores"].append(score)
                    dlist["scores2"].append(score2)

                    out = run_agent(sent, axe, score, score2, model=MODELS[1])
                    # out = get_nl(
                    #     out, pattern=r"Score-A [1-5], Score-B [1-5]:(.+?)(?:\n|$)"
                    # )
                    dlist["paraphrases"].append(out)

                    print(f"{i}-{j}: {sent}")

                result = pd.DataFrame(dlist)
                result.to_csv(
                    os.path.join(
                        "exp",
                        "gold",
                        "result",
                        f"{DATA_TYPE}_{TASK_TYPE}_selected_tmp.csv",
                    ),
                    index=False,
                )

        result = pd.DataFrame(dlist)
        result.to_csv(
            os.path.join(
                "exp", "gold", "result", f"{DATA_TYPE}_{TASK_TYPE}_selected.csv"
            ),
            index=False,
        )
