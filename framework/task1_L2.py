"""
NL Generation
Task 1: Level 2/3 Chart Caption Generation
"""

import os
import json
import tiktoken
import numpy as np
import pandas as pd

from glob import glob
from time import sleep
from datetime import datetime
from dotenv import load_dotenv

from openai.error import RateLimitError, InvalidRequestError
from langchain.chat_models import ChatOpenAI
from framework.utils import get_ftt_str, get_nl
from langchain.agents import create_pandas_dataframe_agent


load_dotenv(".env")

NUMBER_MAX_DISPLAY = 9999

SLEEP_TIME = 10.0
NUM_VALUES = 5
VEGA_LITE_URLS = np.sort(glob(os.path.join("docs", "data", "chart_48_in", "*.vl.json")))
DATA_URLS = np.sort(glob(os.path.join("docs", "data", "csv_48_process", "*.csv")))

MODELS = ["gpt-3.5-turbo-0613", "gpt-4-0613", "gpt-4-32k-0613"]
ENC = tiktoken.encoding_for_model("gpt-4")


data_df = {
    "L2": [],
    "features": [],
    "operations": [],
    "questions": [],
    "infos": [],
    "mids": [],
    "outs": [],
    "out2s": [],
}


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
    prompt_len = len(ENC.encode(prompt))
    return prompt, prompt_len


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
    for i in range(len(VEGA_LITE_URLS)):
        print(f"VL[{i}]: {VEGA_LITE_URLS[i]}, DATA[{i}]: {DATA_URLS[i]}")

        with open(VEGA_LITE_URLS[i], "r") as file:
            vl = json.load(file)

        data = pd.read_csv(DATA_URLS[i])
        ftt_str = get_ftt_str(vl, data, NUM_VALUES)

        prompt, prompt_len = get_prompt_L2(vl)
        print(f"prompt_len: {prompt_len}")

        try:
            if prompt_len < 8192:
                info, out, out2, mid = run_agent(prompt, data, ftt_str, model=MODELS[1])
            elif prompt_len < 32768:
                info, out, out2, mid = run_agent(prompt, data, ftt_str, model=MODELS[2])
            else:
                info = "Error: prompt length exceeds maximum limit"
                out, out2, mid = -1, -1, -1
        except RateLimitError as err:
            print(f"Error: {err}, sleep for {SLEEP_TIME} seconds")
            sleep(SLEEP_TIME)
            info, out, out2, mid = run_agent(prompt, data, ftt_str, model=MODELS[1])
        except InvalidRequestError as err:
            print(f"Error: {err}")
            info, out, out2, mid = err, -1, -1, -1

        data_df["infos"].append(info)
        data_df["mids"].append(mid)
        data_df["outs"].append(out)
        data_df["out2s"].append(out2)

        data_df["features"].append(
            get_nl(out, pattern=r"Step 1\. Features:(.+?)Step 2\.")
        )
        data_df["operations"].append(
            get_nl(out, pattern=r"Step 2\. Operations:(.+?)Step 3\.")
        )
        data_df["questions"].append(get_nl(out, pattern=r"Step 3\. Questions:(.+)"))

        data_df["L2"].append(out2)

    df = pd.DataFrame(data_df)
    df.to_csv(
        os.path.join("framework", "result", f"task1_L2_{datetime.now()}.csv"),
        index=False,
    )
