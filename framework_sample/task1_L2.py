import os
import json
import pandas as pd
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from framework.utils import get_ftt_str, get_nl
from langchain.agents import create_pandas_dataframe_agent


load_dotenv(".env")

NUM_VALUES = 5
NUMBER_MAX_DISPLAY = 9999
MODELS = ["gpt-3.5-turbo-0613", "gpt-4-0613", "gpt-4-32k-0613"]

filename = os.path.join("framework_sample", "sample.vl.json")
dataname = os.path.join("framework_sample", "superstore.csv")


def get_prompt_L2(vl):
    prompt = f"""
{vl}

Let's generate question(s) step by step.

Step 1. What is the most prominent and meaningful feature in the given chart?
Step 2. What is the mathematical operation(s) (e.g., max, min, sum, difference, and average) required to describe the feature?
Step 3. Generate question(s) using the mathematical operation(s) required to describe the feature. If there are multiple questions, separate them with semicolon(;).

##
Step 1. Features:
Step 2. Operations:
Step 3. Questions:
"""
    return prompt


def run_agent(prompt, data, ftt_str, model, temp=0.0, return_intermediate_steps=True):
    llm = ChatOpenAI(temperature=temp, model=model)
    out = llm.predict(prompt)

    prompts = get_nl(out, pattern=r"Step 3\. Questions:(.+)")
    prompts = prompts.strip().split(";")
    prompts = [
        f"Refer to this: {ftt_str}\nDo not draw any charts to answer the question.\n\nQuestion: {prompt}"
        for prompt in prompts
    ]

    agent = create_pandas_dataframe_agent(
        llm,
        data,
        verbose=True,
        return_intermediate_steps=return_intermediate_steps,
        number_max_display=NUMBER_MAX_DISPLAY,
    )

    mid = ""
    info = ""

    for prompt in prompts:
        if return_intermediate_steps:
            tmp = agent(prompt)
            info += f"{tmp['output']}\n"
            mid += f"{tmp['intermediate_steps']}\n"
        else:
            tmp = agent.run(prompt)
            info += f"{tmp}\n"

    info = info.rstrip("\n")
    mid = mid.rstrip("\n")

    out2 = llm.predict(
        f"""
Information: {info}

{ftt_str}

Generate a concise level 2 NL description of a visualization, with 1 or 2 sentences. It contains statistical and relational properties of the visualization (e.g., descriptive statistics, extrema, outliers, correlations, point-wise comparisons).

##
Level 2 NL Description:
"""
    )

    return info, out, out2, mid


if __name__ == "__main__":
    with open(filename, "r") as file:
        vl = json.load(file)

    data = pd.read_csv(dataname)
    ftt_str = get_ftt_str(vl, data, NUM_VALUES)

    prompt = get_prompt_L2(vl)
    info, out, out2, mid = run_agent(prompt, data, ftt_str, model=MODELS[1])

    print(info)
    print(mid)
    print(out)
    print("=" * 10)
    print(f"Level 2 NL Description: {out2}")
