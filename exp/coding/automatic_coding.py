# 1. Code generation
# (2-1) Manual inspection (by researchers)
# 2-2. Code pre-process
# 3. Embedding using OPENAI "text-embedding-ada-002"
# 4. Dimension reduction
# 5. Clustering
# 6. Save file

import os
import time
import numpy as np
import pandas as pd
from collections import Counter

import openai
from dotenv import load_dotenv

# from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from functools import reduce

# STOP_WORDS = set(stopwords.words("english"))
STOP_WORDS = ["language", "use of"]
lemmatizer = WordNetLemmatizer()

MODELS = ["gpt-3.5-turbo-0613", "gpt-4-0613", "text-embedding-ada-002"]
load_dotenv("./codes/generate/.env")
openai.api_key = os.getenv("OPENAI_API_KEY")

n_dim = 5
param = 5
reduction = True
method = "hdbscan"
embedding_model = "openai"

data_loc = "dfall"  # ["df1", "df2", "df3", "dfall", "dfall_processed"]
code_loc = f"./coding/result/d_code_{data_loc}.csv"
embeddings_loc = f"./coding/result/d_embeddings_{embedding_model}.npy"
file_loc = f"./coding/result/d_code_clusters_{method}_{reduction}_{param}_{embedding_model}.csv"


def get_embedding(text):
    print(text)
    response = openai.Embedding.create(model=MODELS[2], input=[text])
    embedding = response["data"][0]["embedding"]
    return embedding


def preprocess(text):
    tokens = text.split(";")
    tokens = [token.lower().strip() for token in tokens]

    tokens = [
        reduce(lambda token, rep: token.replace(rep, "").strip(), STOP_WORDS, token)
        for token in tokens
    ]
    # tokens = [token for token in tokens if token not in STOP_WORDS]
    tokens = [lemmatizer.lemmatize(token) for token in tokens if token]
    # print(f"text: {text}\ntokens: {tokens}")
    return tokens


def generate_code(prompt):
    try:
        response = openai.ChatCompletion.create(
            model=MODELS[1],
            messages=[{"role": "user", "content": prompt}],
            max_tokens=30,
            n=1,
            stop=None,
            temperature=0.0,
        )
        code = response["choices"][0]["message"]["content"].strip()
    except:
        code = "-"  # error case
    time.sleep(1.0)
    return code


def make_prompt(sent):
    prompt = f"""
Let's perform a thematic analysis in the field of human-computer interaction. Generate characteristics of languages leveraged in the given sentence. The total number is five and each of them is separated by semicolons. Do not add numbering or any explanations.

Sentence: {sent}

##
; ; ; ;
"""
    return prompt


if __name__ == "__main__":
    # 1. Code generation
    if os.path.exists(code_loc):
        code_data = pd.read_csv(code_loc)
        codes = code_data["codes"].to_list()
        print("code file loaded")
    else:
        os.makedirs(code_loc, exist_ok=True)

        if data_loc == "df1":
            df = pd.read_csv("./coding/d1_description.csv")["description"]
            task = ["description"] * len(df)
        elif data_loc == "df2":
            df = pd.read_csv("./coding/d2_nlvcorpus.csv")["utterance"]
            task = ["utterance"] * len(df)
        elif data_loc == "df3":
            df = pd.read_csv("./coding/d3_questions.csv")["question"]
            task = ["question"] * len(df)
        elif data_loc == "dfall":
            df1 = pd.read_csv("./coding/d1_description.csv")["description"]  # 2147
            df2 = pd.read_csv("./coding/d2_nlvcorpus.csv")["utterance"]  # 893
            df3 = pd.read_csv("./coding/d3_questions.csv")["question"]  # 629
            df = pd.concat([df1, df2, df3], axis=0)  # 3669
            task = (
                ["description"] * len(df1)
                + ["utterance"] * len(df2)
                + ["question"] * len(df3)
            )
        else:
            print("data_loc error")
            exit()
        df = df.values.tolist()

        codes = []
        for i, sent in enumerate(df):
            prompt = make_prompt(sent)
            code = generate_code(prompt)
            codes.append(code)
            print(f"{str(i).zfill(4)} codes: {code}")
        code_data = pd.DataFrame(
            {
                "task": task,
                "sentence": df,
                "codes": codes,
            }
        )
        code_data.to_csv(code_loc, index=False)
        print("code file saved")

    # 2. Code pre-process
    code_processed = [preprocess(code) for code in codes]
    code_processed = [item for sublist in code_processed for item in sublist]

    # 2-1. Save frequency
    count = Counter(code_processed)
    count_df = pd.DataFrame(list(count.items()), columns=["code", "freq"])
    count_df.to_csv("./coding/result/freq.csv", index=False)

    # 2-2. only for unique
    code_processed = list(set(code_processed))
    # code_processed = list(set(code_processed))[:50]

    # 3. Embedding
    if os.path.exists(embeddings_loc):
        embeddings = np.load(embeddings_loc)
        print("embedding file loaded")
    else:
        if embedding_model == "sentbert":
            from sentence_transformers import SentenceTransformer

            model = SentenceTransformer(embedding_model)
            embeddings = model.encode(code_processed)
        else:
            embeddings = [get_embedding(text) for text in code_processed]
        np.save(embeddings_loc, embeddings)
        print("embedding file saved")

    # 4. Dimension reduction
    if reduction:
        import umap

        reducer = umap.UMAP(n_components=n_dim, verbose=True)
        embeddings = reducer.fit_transform(embeddings)

    # 5. Clustering
    if method == "kmeans":
        from sklearn.cluster import KMeans

        kmeans = KMeans(n_clusters=param)
        clusters = kmeans.fit_predict(embeddings)
    elif method == "hdbscan":
        from sklearn.cluster import HDBSCAN

        hdb = HDBSCAN(min_cluster_size=param)
        clusters = hdb.fit_predict(embeddings)
    elif method == "dbscan":
        from sklearn.cluster import DBSCAN

        dbscan = DBSCAN(eps=0.5, min_samples=param)
        clusters = dbscan.fit_predict(embeddings)
    else:
        print("clustering method error")
        exit()

    # 6. Save file
    results_df = pd.DataFrame(
        {
            "code_processed": code_processed,
            "cluster": clusters,
        }
    )

    results_df.to_csv(file_loc, index=False)
