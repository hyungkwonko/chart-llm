import os
import json
import pandas as pd
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from framework.utils import get_ftt_str, get_nl


load_dotenv(".env")

NUM_VALUES = 5

MODELS = ["gpt-3.5-turbo-0613", "gpt-4-0613", "gpt-4-32k-0613"]
filename = os.path.join("framework_sample", "sample.vl.json")
dataname = os.path.join("framework_sample", "superstore.csv")


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
    return prompt


def run_agent(prompt, model, temp=0.0):
    llm = ChatOpenAI(temperature=temp, model=model)
    out = llm.predict(prompt)
    return out


if __name__ == "__main__":
    with open(filename, "r") as file:
        vl = json.load(file)

    data = pd.read_csv(dataname)
    ftt_str = get_ftt_str(vl, data, NUM_VALUES)

    prompt = get_prompt_L1(vl, ftt_str)
    out = run_agent(prompt, model=MODELS[1])

    print(out)
    print(get_nl(out, pattern=r"Step 1\. Composite Views:(.+?)Step 2\."))
    print(get_nl(out, pattern=r"Step 2\. Chart Semantics:(.+?)Step 3\."))
    print("=" * 10)
    print(get_nl(out, pattern=r"Step 3\. Level 1 NL Description:(.+)"))
