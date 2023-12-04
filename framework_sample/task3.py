import os
import json
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI
from framework.utils import get_nl

load_dotenv(".env")

MODELS = ["gpt-3.5-turbo-0613", "gpt-4-0613", "gpt-4-32k-0613"]

filename = os.path.join("framework_sample", "sample.vl.json")
dataname = os.path.join("framework_sample", "superstore.csv")


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
Step 8. Generate a compositional question using these operations, without including any visual attributes such as color, length, size, or position.
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
    return prompt


def run_agent(prompt, model, temp=0.0):
    llm = ChatOpenAI(temperature=temp, model=model)
    out = llm.predict(prompt)

    return out


if __name__ == "__main__":
    with open(filename, "r") as file:
        vl = json.load(file)

    prompt = get_prompt_question(vl)

    out = run_agent(prompt, model=MODELS[1])

    print(out)
    print(get_nl(out, pattern=r"Step 1\. Decision:(.+?)Step 2\."))
    print(get_nl(out, pattern=r"Step 2\. Conclusion:(.+?)Step 3\."))
    print(get_nl(out, pattern=r"Step 3\. Specific Value:(.+?)Step 4\."))
    lookup_non = get_nl(out, pattern=r"Step 4\. Lookup Question:(.+?)Step 5\.")
    print(get_nl(out, pattern=r"Step 5\. Visual Attributes:(.+?)Step 6\."))
    lookup_vis = get_nl(out, pattern=r"Step 6\. Paraphrased Question:(.+?)Step 7\.")
    print(get_nl(out, pattern=r"Step 7\. Operations:(.+?)Step 8\."))
    comp_non = get_nl(out, pattern=r"Step 8\. Compositional Question:(.+?)Step 9\.")
    print(get_nl(out, pattern=r"Step 9\. Visual Attributes:(.+?)Step 10\."))
    comp_vis = get_nl(out, pattern=r"Step 10\. Paraphrased Question:(.+?)Step 11\.")
    open_ended = get_nl(out, pattern=r"Step 11\. Open-ended Question:(.+)")

    print("=" * 10)
    print(f"lookup_non: {lookup_non}")
    print(f"lookup_vis: {lookup_vis}")
    print(f"comp_non: {comp_non}")
    print(f"comp_vis: {comp_vis}")
    print(f"open_ended: {open_ended}")
