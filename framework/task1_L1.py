"""
NL Generation
Task 1: Level 1 Chart Caption Generation
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


load_dotenv(".env")

SLEEP_TIME = 10.0
NUM_VALUES = 5
VEGA_LITE_URLS = np.sort(glob(os.path.join("docs", "data", "chart_48_in", "*.vl.json")))
DATA_URLS = np.sort(glob(os.path.join("docs", "data", "csv_48_process", "*.csv")))

MODELS = ["gpt-3.5-turbo-0613", "gpt-4-0613", "gpt-4-32k-0613"]
ENC = tiktoken.encoding_for_model("gpt-4")


RESULT_FOLDER = os.path.join("framework", "result")
os.makedirs(RESULT_FOLDER, exist_ok=True)

data_df = {
    "out1s": [],
    "composites": [],
    "semantics": [],
    "L1": [],
}


def get_prompt_L1(vl, ftt_str):
    prompt = f"""
{vl}

Let's generate a level 1 NL description step by step.

Step 1. Determine if the visualization contains composite views, such as layered plots, trellis plots, or other types of multiple view displays, and provide a count of the number of plots if any are present.
Step 2. Analyze the semantics of each chart individually, including [Data], [Transform], [Mark], [Chart-Type], [Encoding], [Style], and [Interaction]. Refer to this:
{ftt_str}
Step 3. Generate a level 1 NL description using the semantics. It contains elemental and encoded properties of the visualization (i.e., the visual components that comprise a graphical representation's design and construction).

##
Step 1. Composite Views:
- True/False:
- (If True) Type: (layered, trellis, multiple views)
- Number of plots:
Step 2. Chart Semantics:
- Data:
- Field (Value):
- Transform:
- Mark:
- Chart-Type:
- Encoding:
- Style:
- Interaction (e.g., tooltip):
Step 3. Level 1 NL Description:
"""
    prompt_len = len(ENC.encode(prompt))
    return prompt, prompt_len


def run_agent(prompt, model, temp=0.0):
    llm = ChatOpenAI(temperature=temp, model=model)
    out = llm.predict(prompt)
    return out


if __name__ == "__main__":
    for i in range(len(VEGA_LITE_URLS)):
        print(f"VL[{i}]: {VEGA_LITE_URLS[i]}, DATA[{i}]: {DATA_URLS[i]}")

        with open(VEGA_LITE_URLS[i], "r") as file:
            vl = json.load(file)

        data = pd.read_csv(DATA_URLS[i])
        ftt_str = get_ftt_str(vl, data, NUM_VALUES)

        prompt, prompt_len = get_prompt_L1(vl, ftt_str)
        print(f"prompt_len: {prompt_len}")

        try:
            if prompt_len < 8192:
                out = run_agent(prompt, model=MODELS[1])
            elif prompt_len < 32768:
                out = run_agent(prompt, model=MODELS[2])
            else:
                out = "Error: prompt length exceeds maximum limit"
        except RateLimitError as err:
            print(f"Error: {err}, sleep for {SLEEP_TIME} seconds")
            sleep(SLEEP_TIME)
            out = run_agent(prompt, model=MODELS[1])
        except InvalidRequestError as err:
            print(f"Error: {err}")
            out = err

        data_df["out1s"].append(out)
        data_df["composites"].append(
            get_nl(out, pattern=r"Step 1\. Composite Views:(.+?)Step 2\.")
        )
        data_df["semantics"].append(
            get_nl(out, pattern=r"Step 2\. Chart Semantics:(.+?)Step 3\.")
        )

        l1 = get_nl(out, pattern=r"Step 3\. Level 1 NL Description:(.+)")
        data_df["L1"].append(l1)

    df = pd.DataFrame(data_df)
    df.to_csv(
        os.path.join("framework", "result", f"task1_L1_{datetime.now()}.csv"),
        index=False,
    )
