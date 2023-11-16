"""
Task 4: Paraphrasing
"""

import os
import random
import pandas as pd

from dotenv import load_dotenv
from datetime import datetime

from framework.utils import get_nl, AXES

from langchain.chat_models import ChatOpenAI


def run_agent(sent, axes, model, temp=0.0):
    llm = ChatOpenAI(temperature=temp, model=model)

    # num_elements = random.randint(0, 2)
    num_elements = random.randint(1, 2)
    random_axes = random.sample(axes, num_elements)

    len_axes = len(random_axes)

    if len_axes == 0:
        return f"Paraphrase: {sent}", "<NONE>", "<NONE>"
    elif len_axes == 1:
        # first_integer = random.randint(1, 5)
        first_integer = random.choice([1, 5])

        out1 = llm.predict(
            f"""
{random_axes[0][2]}
Score-A of 1 indicates a higher tendency to use {random_axes[0][0]} language and a Score-A of 5 indicates a higher tendency to use {random_axes[0][1]} language.
Rewrite the following sentence as if it were spoken by a person with a given score for language usage.

Sentence: {sent}
Score-A: {first_integer}

##
Paraphrase:
"""
        )
        return out1, random_axes, [first_integer]
    else:
        # first_integer = random.randint(1, 5)
        # second_integer = random.randint(1, 5)
        first_integer = random.choice([1, 5])
        second_integer = random.choice([1, 5])

        out1 = llm.predict(
            f"""
{random_axes[0][2]}
{random_axes[1][2]}
Score-A of 1 indicates a higher tendency to use {random_axes[0][0]} language and a Score-A of 5 indicates a higher tendency to use {random_axes[0][1]} language.
Score-B of 1 indicates a higher tendency to use {random_axes[1][0]} language and a Score-B of 5 indicates a higher tendency to use {random_axes[1][1]} language.
Rewrite the following sentence as if it were spoken by a person with a given score for language usage.

Sentence: {sent}
Score-A: {first_integer}, Score-B: {second_integer}

##
Paraphrase:
"""
        )
        return out1, random_axes, [first_integer, second_integer]


load_dotenv(".env")

MODELS = ["gpt-3.5-turbo-0613", "gpt-4-0613", "gpt-4-32k-0613"]

SAMPLE_SENTENCES = [
    "Create a pie chart with 'Regime' as color and 'value' as the angle.",
]
# SAMPLE_SENTENCES = pd.read_csv(
#     os.path.join("docs", "data", "baseline", "d2_utterance.csv")
# )


paraphrases, sentences, axes, values = [], [], [], []

if __name__ == "__main__":
    for sentence in SAMPLE_SENTENCES:
        output, ax, value = run_agent(sentence, AXES, model=MODELS[1])

        if "Paraphrase:" in output:
            paraphrase = get_nl(output, pattern=r"Paraphrase:(.+)")
        else:
            paraphrase = output.replace("Paraphrase: ", "").strip()

        paraphrases.append(paraphrase)
        axes.append([sub_list[:-1] for sub_list in ax])
        values.append(value)
        sentences.append(sentence)

    data = {
        "originals": sentences,
        "paraphrases": paraphrases,
        "axes": axes,
        "values": values,
    }

    print(f"originals: {sentences}")
    print(f"paraphrases: {paraphrases}")
    print(f"axes: {axes}")
    print(f"values: {values}")

    df = pd.DataFrame(data)
    df.to_csv(
        os.path.join("framework", "result", f"task4_{datetime.now()}.csv"),
        index=False,
    )
