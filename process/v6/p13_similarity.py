from sentence_transformers import SentenceTransformer, util
from glob import glob
import numpy as np
import pandas as pd
import json

NUMS = 5

file_list = glob("./files/v6/jsonfiles/d6_input/*.json")
# file_list = glob("./files/v6/jsonfiles/d6/*.json")
file_list = np.sort(file_list)

sentences = []
for file in file_list:
    with open(file, "r") as f:
        data = json.load(f)
        data = json.dumps(data)
    sentences.append(data)

model = SentenceTransformer("all-MiniLM-L6-v2")
embeddings = model.encode(sentences)

cosine_scores = util.cos_sim(embeddings, embeddings).numpy()

# Get top 5 indices with highest similarity
top_indices = np.argsort(-cosine_scores, axis=1)[:, :NUMS]

# Retrieve top indices and their corresponding values
top_values = np.take_along_axis(cosine_scores, top_indices, axis=1)

output_data = np.column_stack((top_indices, top_values))

# Define column names
column_names = ["index_" + str(i) for i in range(NUMS)] + [
    "value_" + str(i) for i in range(NUMS)
]

# Save the data to a CSV file
df = pd.DataFrame(output_data, columns=column_names)
df.to_csv("./files/exp/similarity.csv", index=False)
