import os
import time
import json
import openai
import pandas as pd
from dotenv import load_dotenv

load_dotenv(".env")

# NAMES = ["bm", "bmllmp", "bmllmpllmp2", "half"]
NAMES = ["llmp", "llmp2"]
# NAMES = ["bm", "bmllmp", "bmllmpllmp2", "half", "llmp", "llmp2"]

os.makedirs("exp/finetuning/result", exist_ok=True)

for i, name in enumerate(NAMES):
    with open(f"exp/finetuning/data/model_{name}.txt", "r") as file:
        model_name = file.read().strip()

    for j in range(5):
        outputs = []
        correct_nums = 0

        with open("exp/finetuning/data/bm_test.jsonl", "r") as file:
            for line in file:
                json_line = json.loads(line)
                prompt = json_line["prompt"].strip()
                response = openai.completions.create(
                    model=model_name, prompt=prompt, max_tokens=10, stop="END"
                )

                ans = json_line["completion"].replace("END", "").strip()
                pred = response.choices[0].text.strip()
                correct = int(ans == pred)
                correct_nums += correct

                output = {
                    "Prompt": prompt.replace("\n\n###", ""),
                    "Answer": ans,
                    "Prediction": pred,
                    "Correct": correct,
                }
                outputs.append(output)
                # print(output)

                time.sleep(0.7)

        df = pd.DataFrame(outputs)
        df.to_csv(f"exp/finetuning/result/result_{j}_{name}.csv", index=False)

        print(f"{name}, {j}, correct_nums: {correct_nums}")
