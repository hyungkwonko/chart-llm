"""
Generate utterance datasets
"""

import os
import json
import tiktoken
import pandas as pd

from time import sleep
from dotenv import load_dotenv

from langchain.chat_models import ChatOpenAI
from openai.error import RateLimitError, InvalidRequestError
from framework.utils import (
    get_ftt_str,
    get_nl,
    get_nl_all,
    get_instruction,
    compress_json,
)


load_dotenv(".env")

SLEEP_TIME = 10.0
NUM_VALUES = 5

D1_LOC = os.path.join("exp", "d2_utterance", "data", "superstore.csv")
D2_LOC = os.path.join("exp", "d2_utterance", "data", "cars.csv")
D3_LOC = os.path.join("exp", "d2_utterance", "data", "movies.csv")
JSON_LOC = os.path.join("exp", "d2_utterance", "data", "vlSpecs.json")

MODELS = ["gpt-3.5-turbo-0613", "gpt-4-0613", "gpt-4-32k-0613"]
ENC = tiktoken.encoding_for_model("gpt-4")

data_df = {
    "outs": [],
    "out2s": [],
    "insts": [],
    "firsts": [],
    "seconds": [],
    "command": [],
    "query": [],
    "question": [],
    "dnames": [],
    "vids": [],
}


def get_prompt_utterance(vl, ftt_str):
    prompt = f"""
{vl}

Step 1. Determine if the visualization contains composite views, such as layered plots, trellis plots, or other types of multiple view displays, and provide a count of the number of plots if any are present.
Step 2. Provide a list of instructions to create the chart using natural language.
- Write instructions for each view and separate with <%>
- Separate each instruction by a semicolon (;)
- Divide each instruction to contain only one specific action
- Use the following chart semantics to specify instructions: [Data], [Chart-Type], [Mark], [Encoding], [Transform], [Style], [Interaction]
Step 3. Given the information about the fields and their synonyms, please replace the field names with their corresponding synonyms.
{ftt_str}

##
Step 1. Composite Views:
- True/False:
- (If True) Type: (layered, trellis, multiple views)
- Number of plots:
Step 2. Instructions:
[View #]; [<Chart Semantic>]: <Instruction>; [<Chart Semantic>]: <Instruction>; ... <%>
Step 3. Instructions:
[View #]; [<Chart Semantic>]: <Instruction>; [<Chart Semantic>]: <Instruction>; ... <%>
"""
    prompt_len = len(ENC.encode(prompt))
    return prompt, prompt_len


def run_agent(prompt, model, temp=0.0):
    llm = ChatOpenAI(temperature=temp, model=model)
    out = llm.predict(prompt)

    inst = get_nl(out, pattern=r"Step 3\. Instructions:(.+)")
    inst_first, _ = get_instruction(inst)
    inst_first_concat = "\n".join(inst_first)

    prompt2 = f"""
{inst_first_concat}
The above are instructions to generate a chart. Let's generate combined instructions ([Command], [Query], [Question]) for each view step by step.

Step 1. Identify the primary information in each view.
Step 2. Identify the secondary information in each view.
Step 3. Generate a [Command] for each view using only the primary info. Please follow these rules:
- Use imperative voice
- Write in a single sentence
- Use only the primary info
- Make it concise and simple
Step 4. Generate a [Query] for each view using only the primary info. Please follow these rules:
- Refrain from using verbs and articles (e.g., a, the)
- Use only variables, fields, attributes, mathematical formulas (e.g., sum, avg, mix, max, count, order), abbreviations (e.g., vs), and prepositions (e.g., of, by, for, with, over, from, to)
- Write in a single sentence
- Use only the primary info
- Make it concise and simple
Step 5. Generate a [Question] for each view using only the primary info. Please follow these rules:
- Ask an inquiry as a question
- Write in a single sentence
- Use only the primary info
- Make it concise and simple

##
View #<Number>:
Step 1. Primary Information:
Step 2. Secondary Information:
Step 3. Command:
Step 4. Query:
Step 5. Question:
"""
    out2 = llm.predict(prompt2)
    return out, inst_first_concat, out2


if __name__ == "__main__":
    with open(JSON_LOC, "r") as f:
        json_data = json.load(f)

    for i, key in enumerate(json_data):
        vl = json_data[key]
        dname, vid = key.split("-")

        data_df["dnames"].append(dname)
        data_df["vids"].append(vid)

        if dname == "superstore":
            data = pd.read_csv(D1_LOC)
        elif dname == "cars":
            data = pd.read_csv(D2_LOC)
        elif dname == "movies":
            data = pd.read_csv(D3_LOC)
        else:
            print("data error")
            exit()

        ftt_str = get_ftt_str(vl, data, NUM_VALUES)
        vl_str = json.dumps(vl)
        vl_str = compress_json(vl_str)

        prompt, prompt_len = get_prompt_utterance(vl, ftt_str)
        print(f"# {str(i+1).zfill(2)}/{str(len(json_data)).zfill(2)} len: {prompt_len}")

        try:
            if prompt_len < 8192:
                out, inst, out2 = run_agent(prompt, model=MODELS[0])
            elif prompt_len < 32768:
                out, inst, out2 = run_agent(prompt, model=MODELS[2])
            else:
                out, inst, out2 = "Error: prompt length exceeds maximum limit"
        except RateLimitError as err:
            print(f"Error: {err}, sleep for {SLEEP_TIME} seconds")
            sleep(SLEEP_TIME)
            out, inst, out2 = run_agent(prompt, model=MODELS[0])
        except InvalidRequestError as err:
            print(f"Error: {err}")
            out, inst, out2 = err, -1, -1

        data_df["outs"].append(out)
        data_df["out2s"].append(out2)
        data_df["insts"].append(inst)
        data_df["firsts"].append(
            get_nl_all(out2, pattern=r"Step 1\. Primary Information:(.+?)(?:\n|$)")
        )
        data_df["seconds"].append(
            get_nl_all(out2, pattern=r"Step 2\. Secondary Information:(.+?)(?:\n|$)")
        )

        command = get_nl_all(out2, pattern=r"Step 3\. Command:(.+?)(?:\n|$)")
        query = get_nl_all(out2, pattern=r"Step 4\. Query:(.+?)(?:\n|$)")
        question = get_nl_all(out2, pattern=r"Step 5\. Question:(.+?)(?:\n|$)")

        data_df["command"].append(command)
        data_df["query"].append(query)
        data_df["question"].append(question)

        print(f"command: {command}")
        print(f"query: {query}")
        print(f"question: {question}\n")

        # break

    df = pd.DataFrame(data_df)
    df.to_csv(os.path.join("exp", "d2_utterance", "result", "task2.csv"), index=False)
