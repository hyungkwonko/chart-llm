# server.py
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from utils import get_ftt_str, get_nl, get_instruction
from prompt import (
    get_prompt_L1,
    get_prompt_L2,
    get_prompt_L2_2,
    get_prompt_utterance,
    get_prompt_utterance2,
    get_prompt_question,
    get_prompt_paraphrase,
)

import os
import json
import pandas as pd

from openai import OpenAI
from dotenv import load_dotenv

from langchain.chat_models import ChatOpenAI
from langchain.agents import create_pandas_dataframe_agent


app = Flask(__name__)
CORS(app)

load_dotenv(".env")


NUM_VALUES = 5
NUMBER_MAX_DISPLAY = 9999
MODELS = ["gpt-3.5-turbo", "gpt-4", "gpt-4-32k-0613"]
SELECTED_MODEL = MODELS[0]


def run_agent(client, prompt, model):
    response = client.chat.completions.create(
        model=model,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content


@app.route("/generate_nl", methods=["POST"])
def generate_nl():
    data = request.get_json()

    selectedTypeId = data.get("selectedTypeId")
    selectedIndices = data.get("selectedIndices")
    selectedSemantics = data.get("selectedSemantics")
    feature = data.get("feature")
    utteranceType = data.get("utteranceType")
    questionType = data.get("questionType")
    visualizationType = data.get("visualizationType")
    higherLevelDecision = data.get("higherLevelDecision")
    paraphrase = data.get("paraphrase")
    selectedAxis = data.get("selectedAxis")
    axisScore = data.get("axisScore")

    print(f"Selected Type ID: {selectedTypeId}")
    print(f"Selected Indices: {selectedIndices}")
    print(f"Selected Semantics: {selectedSemantics}")
    print(f"questionType: {questionType}")
    print(f"visualizationType: {visualizationType}")
    print(f"higherLevelDecision: {higherLevelDecision}")
    print(f"paraphrase: {paraphrase}")
    print(f"selectedAxis: {selectedAxis}")
    print(f"axisScore: {axisScore}")

    nl = {}

    if selectedTypeId == "l2":
        llm = ChatOpenAI(model=SELECTED_MODEL, request_timeout=120)
    else:
        client = OpenAI()

    if selectedTypeId == "l1":
        semantics = [key for key, value in selectedSemantics.items() if value]

        for index in selectedIndices:
            filename = os.path.join("data", "chart", f"{index}.vl.json")
            dataname = os.path.join("data", "tech", f"{index}.csv")

            with open(filename, "r") as file:
                vl = json.load(file)

            df = pd.read_csv(dataname)
            ftt_str = get_ftt_str(vl, df, NUM_VALUES)
            prompt = get_prompt_L1(vl, ftt_str, semantics)

            out = run_agent(client, prompt, SELECTED_MODEL)
            l1caption = get_nl(out, pattern=r"Step 3\. Level 1 NL Description:(.+)")
            print("out: ", out)
            print("l1caption: ", l1caption)

            nl[index] = l1caption

    elif selectedTypeId == "l2":
        for index in selectedIndices:
            filename = os.path.join("data", "chart", f"{index}.vl.json")
            dataname = os.path.join("data", "tech", f"{index}.csv")

            with open(filename, "r") as file:
                vl = json.load(file)

            df = pd.read_csv(dataname)
            ftt_str = get_ftt_str(vl, df, NUM_VALUES)
            prompt = get_prompt_L2(vl, feature)
            out = llm.predict(prompt)

            prompts = get_nl(out, pattern=r"Step 2\. Questions:(.+)")
            prompts = prompts.strip().split(";")
            prompts = [
                f"Refer to this: {ftt_str}\nDo not draw any charts to answer the question.\n\nQuestion: {prompt}"
                for prompt in prompts
            ]

            agent = create_pandas_dataframe_agent(
                llm,
                data,
                verbose=True,
                number_max_display=NUMBER_MAX_DISPLAY,
            )

            info = ""
            for prompt in prompts:
                tmp = agent.run(prompt)
                info += f"{tmp}\n"
            info = info.rstrip("\n")

            prompt = get_prompt_L2_2(info, ftt_str)
            l2caption = llm.predict(prompt)
            nl[index] = l2caption

    elif selectedTypeId == "utterance":
        semantics = [key for key, value in selectedSemantics.items() if value]

        for index in selectedIndices:
            filename = os.path.join("data", "chart", f"{index}.vl.json")
            dataname = os.path.join("data", "tech", f"{index}.csv")

            with open(filename, "r") as file:
                vl = json.load(file)

            df = pd.read_csv(dataname)
            ftt_str = get_ftt_str(vl, df, NUM_VALUES)
            prompt = get_prompt_utterance(vl, ftt_str, semantics)

            out = run_agent(client, prompt, SELECTED_MODEL)
            inst = get_nl(out, pattern=r"Step 3\. Instructions:(.+)")
            inst_first = get_instruction(inst, semantics)
            inst_first_concat = "\n".join(inst_first)

            print(f"inst_first_concat: {inst_first_concat}")

            prompt = get_prompt_utterance2(utteranceType, inst_first_concat)
            utterance = run_agent(client, prompt, SELECTED_MODEL)
            utterance = get_nl(utterance, pattern=r"Step 3\. Utterance:(.+)")

            print(f"utterance: {utterance}")

            if paraphrase:
                prompt = get_prompt_paraphrase(utterance, selectedAxis, axisScore)
                out = run_agent(client, prompt, SELECTED_MODEL)
                if "Paraphrase:" in out:
                    utterance = get_nl(out, pattern=r"Paraphrase:(.+)")
                else:
                    utterance = out.replace("Paraphrase: ", "").strip()

            nl[index] = utterance

    elif selectedTypeId == "question":
        for index in selectedIndices:
            filename = os.path.join("data", "chart", f"{index}.vl.json")

            with open(filename, "r") as file:
                vl = json.load(file)

            prompt = get_prompt_question(
                vl, higherLevelDecision, questionType, visualizationType
            )
            out = run_agent(client, prompt, SELECTED_MODEL)
            question = get_nl(out, pattern=r"Question:(.+)")

            if paraphrase:
                prompt = get_prompt_paraphrase(question, selectedAxis, axisScore)
                out = run_agent(client, prompt, SELECTED_MODEL)
                if "Paraphrase:" in out:
                    question = get_nl(out, pattern=r"Paraphrase:(.+)")
                else:
                    question = out.replace("Paraphrase: ", "").strip()

            nl[index] = question

    return jsonify(
        {
            "status": "success",
            "message": "Data received successfully!",
            "nl": nl,
        }
    )


@app.route("/data/chart/<filename>")
def send_vega_lite_file(filename):
    return send_from_directory("data/chart", filename)


@app.route("/")
def index():
    return "Flask server is running!"


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5678, debug=True)
    # app.run(debug=True, port=5678)
