import random
import numpy as np

from dotenv import load_dotenv
from framework.utils import AXES
from langchain.chat_models import ChatOpenAI

np.random.seed(0)

load_dotenv(".env")

MODELS = ["gpt-3.5-turbo-0613", "gpt-4-0613", "gpt-4-32k-0613"]


def gen_prompt(sent, axes):
    prompt = f"""
{axes[0][2]}
Score of 1 indicates a higher tendency to use {axes[0][0]} language and a Score of 5 indicates a higher tendency to use {axes[0][1]} language.
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


def run_agent(sent, axes, model=MODELS[1], temp=0.0):
    llm = ChatOpenAI(temperature=temp, model=model)
    prompt = gen_prompt(sent, axes)
    return llm.predict(prompt)


if __name__ == "__main__":
    print("provide input: ")
    sentence = input()

    if sentence == "":
        sentence = (
            "Create a bar chart showing the sum of profit from different regions."
        )
        print(f"proceeding with default sentence: {sentence}")

    axe = random.sample(AXES, 2)
    out = run_agent(sentence, axe, model=MODELS[1])

    print(axe)
    print(out)
