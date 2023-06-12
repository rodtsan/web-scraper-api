import re
from flask import json
import graphene
from flask import json
import openai
import pandas as pd
import numpy as np
import os
from openai.embeddings_utils import get_embedding, cosine_similarity
import settings
from utils.paths import CURRENT_PATH

openai.organization = settings.OPENAI_API_ORG
openai.api_key = settings.OPENAI_API_KEY


def find_similarites(
    search_input, csv_file
) -> list[dict[any, any]] | list:
    # Read Data File Containing Words
    cvs_filepath = f"{os.getcwd()}/files/embeddings/{csv_file}"
    df = pd.read_csv(cvs_filepath)
    
    
    csv_embeddings_filepath = (
        f"{os.getcwd()}/files/embeddings/{os.path.splitext(csv_file)[0]}_embeddings.csv"
    )

    if os.path.exists(csv_embeddings_filepath):
        df = pd.read_csv(csv_embeddings_filepath)
    else:
        df["embedding"] = df["text"].apply(
            lambda x: get_embedding(x, engine="text-embedding-ada-002")
        )
        df.to_csv(csv_embeddings_filepath)

    # df = pd.read_csv(csv_embeddings_filepath)
    df["embedding"] = df["embedding"].apply(eval).apply(np.array)
    # print(df)

    # Semantic Search
    # Now that we have our word embeddings stored, let's load them into a new dataframe and use it for semantic search.
    # Since the 'embedding' in the CSV is stored as a string, we'll use apply() and to interpret this string as Python
    # code and convert it to a numpy array so that we can perform calculations on it.
    search_input_vector = get_embedding(search_input, engine="text-embedding-ada-002")
    df["similarities"] = df["embedding"].apply(
        lambda x: cosine_similarity(x, search_input_vector)
    )
    df = df.sort_values("similarities", ascending=False).head(20)

    df_2_js = df.to_json(orient="table")

    js_2_dict = json.loads(df_2_js)["data"]

    if bool(js_2_dict):
        return [{k: v for k, v in sr.items() if "Unnamed" not in k} for sr in js_2_dict]

    return []


class SearchResult(graphene.ObjectType):
    index = graphene.Int()
    # Unnamed = graphene.String()
    text = graphene.String()
    embedding = graphene.String()
    similarities = graphene.String()

    class Meta:
        name = "search_input"


class Topic(graphene.ObjectType):
    filename = graphene.String()
    name = graphene.String()
