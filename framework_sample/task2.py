import os
import json
import pandas as pd
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from framework.utils import get_ftt_str, get_nl, get_nl_all, get_instruction


load_dotenv(".env")

NUM_VALUES = 5
MODELS = ["gpt-3.5-turbo-0613", "gpt-4-0613", "gpt-4-32k-0613"]

filename = os.path.join("framework_sample", "sample.vl.json")
dataname = os.path.join("framework_sample", "superstore.csv")


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
    return prompt


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
    with open(filename, "r") as file:
        vl = json.load(file)

    data = pd.read_csv(dataname)
    ftt_str = get_ftt_str(vl, data, NUM_VALUES)

    prompt = get_prompt_utterance(vl, ftt_str)

    out, inst, out2 = run_agent(prompt, model=MODELS[1])

    print(out)
    print(out2)
    print(inst)
    print(get_nl_all(out2, pattern=r"Step 1\. Primary Information:(.+?)(?:\n|$)"))
    print(get_nl_all(out2, pattern=r"Step 2\. Secondary Information:(.+?)(?:\n|$)"))

    command = get_nl_all(out2, pattern=r"Step 3\. Command:(.+?)(?:\n|$)")
    query = get_nl_all(out2, pattern=r"Step 4\. Query:(.+?)(?:\n|$)")
    question = get_nl_all(out2, pattern=r"Step 5\. Question:(.+?)(?:\n|$)")

    print("=" * 10)
    print(f"command: {command}")
    print(f"query: {query}")
    print(f"question: {question}\n")
