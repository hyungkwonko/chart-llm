"""
Generate NL datasets
Task 3: Chart Question Generation
"""


import os
import json
import tiktoken
import pandas as pd

from time import sleep
from datetime import datetime
from dotenv import load_dotenv

from openai.error import RateLimitError, InvalidRequestError
from langchain.chat_models import ChatOpenAI
from framework.utils import get_nl

load_dotenv(".env")

SLEEP_TIME = 10.0
NUM_VALUES = 5
JSON_LOC = os.path.join("benchmark", "VisQA-release", "data", "chart-list.json")

MODELS = ["gpt-3.5-turbo-0613", "gpt-4-0613", "gpt-4-32k-0613"]
ENC = tiktoken.encoding_for_model("gpt-4")


data_df = {
    "outs": [],
    "step1s": [],
    "step2s": [],
    "step3s": [],
    "lookup-nonvisual": [],
    "step5s": [],
    "lookup-visual": [],
    "step7s": [],
    "compositional-nonvisual": [],
    "step9s": [],
    "compositional-visual": [],
    "open-ended": [],
    "dnames": [],
}


def get_prompt_question(vl):
    prompt = f"""
{vl}

Let's generate a lookup question, a compositional question, and an open-ended question for a given Vega-Lite spec step by step. The lookup question requires a single value retrieval. The compositional question requires multiple operations.

Step 1. What higher-level decision can be made by analyzing this chart?
Step 2. What is a possible conclusion that can be reached from this decision?
Step 3. What specific value can be retrieved to reach this conclusion?
Step 4. Generate a lookup question using this value, without including any visual attributes such as color, length, size, or position.
Step 5. What visual attributes are required to paraphrase this question?
Step 6. Paraphrase the generated question using the chart's visual attributes.
Step 7. What are the mathematical operations (e.g., max, min, sum, difference, and average) to reach the conclusion in Step 2?
Step 8. Generate a compositional question using this value, without including any visual attributes such as color, length, size, or position.
Step 9. What visual attributes are required to paraphrase this question?
Step 10. Paraphrase the generated question using the chart's visual attributes.
Step 11. Generate an open-ended question to reach the conclusion in Step 2.

##
Step 1. Decision:
Step 2. Conclusion:
Step 3. Specific Value:
Step 4. Lookup Question:
Step 5. Visual Attributes:
Step 6. Paraphrased Question:
Step 7. Operations:
Step 8. Compositional Question:
Step 9. Visual Attributes:
Step 10. Paraphrased Question:
Step 11. Open-ended Question:
"""
    prompt_len = len(ENC.encode(prompt))
    return prompt, prompt_len


def run_agent(prompt, model, temp=0.0):
    llm = ChatOpenAI(temperature=temp, model=model)
    out = llm.predict(prompt)

    return out


if __name__ == "__main__":
    with open(JSON_LOC, "r") as file:
        json_infos = json.load(file)

    for i, json_info in enumerate(json_infos):
        dataset = json_info["dataset"]
        filename = json_info["filename"]
        dnames = json_info["dataset"] + "|" + json_info["name"]
        data_df["dnames"].append(dnames)

        vl_loc = os.path.join("benchmark", "VisQA-release", "data", dataset, filename)
        with open(vl_loc, "r") as file:
            vl = json.load(file)

        prompt, prompt_len = get_prompt_question(vl)
        print(f"prompt_len: {prompt_len}, dnames: {dnames}")

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

        data_df["outs"].append(out)
        data_df["step1s"].append(
            get_nl(out, pattern=r"Step 1\. Decision:(.+?)Step 2\.")
        )
        data_df["step2s"].append(
            get_nl(out, pattern=r"Step 2\. Conclusion:(.+?)Step 3\.")
        )
        data_df["step3s"].append(
            get_nl(out, pattern=r"Step 3\. Specific Value:(.+?)Step 4\.")
        )
        data_df["lookup-nonvisual"].append(
            get_nl(out, pattern=r"Step 4\. Lookup Question:(.+?)Step 5\.")
        )
        data_df["step5s"].append(
            get_nl(out, pattern=r"Step 5\. Visual Attributes:(.+?)Step 6\.")
        )
        data_df["lookup-visual"].append(
            get_nl(out, pattern=r"Step 6\. Paraphrased Question:(.+?)Step 7\.")
        )
        data_df["step7s"].append(
            get_nl(out, pattern=r"Step 7\. Operations:(.+?)Step 8\.")
        )
        data_df["compositional-nonvisual"].append(
            get_nl(out, pattern=r"Step 8\. Compositional Question:(.+?)Step 9\.")
        )
        data_df["step9s"].append(
            get_nl(out, pattern=r"Step 9\. Visual Attributes:(.+?)Step 10\.")
        )
        data_df["compositional-visual"].append(
            get_nl(out, pattern=r"Step 10\. Paraphrased Question:(.+?)Step 11\.")
        )
        data_df["open-ended"].append(
            get_nl(out, pattern=r"Step 11\. Open-ended Question:(.+)")
        )

        df = pd.DataFrame(data_df)
        df.to_csv(
            os.path.join(
                "exp", "d3_question", "result", f"task3_tmp_{datetime.now()}.csv"
            ),
            index=False,
        )

    df = pd.DataFrame(data_df)
    df.to_csv(
        os.path.join("exp", "d3_question", "result", "task3.csv"),
        index=False,
    )
