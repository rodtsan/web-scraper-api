import openai
import pandas as pd
import numpy as np
import os
from openai.embeddings_utils import get_embedding, cosine_similarity

import settings

openai.organization = settings.OPENAI_API_ORG
openai.api_key = settings.OPENAI_API_KEY

# Read Data File Containing Words
w_filepath = f"{os.getcwd()}/files/words.csv"
df = pd.read_csv(w_filepath)

we_filepath = f"{os.getcwd()}/files/word_embeddings.csv"
# df['embedding'] = df['text'].apply(lambda x: get_embedding(x, engine='text-embedding-ada-002'))
# df.to_csv(we_filepath)

df = pd.read_csv(we_filepath)
df['embedding'] = df['embedding'].apply(eval).apply(np.array)
# print(df)

# Semantic Search
# Now that we have our word embeddings stored, let's load them into a new dataframe and use it for semantic search. 
# Since the 'embedding' in the CSV is stored as a string, we'll use apply() and to interpret this string as Python
# code and convert it to a numpy array so that we can perform calculations on it.

search_term = input('Enter a search term: ')

search_term_vector = get_embedding(search_term, engine="text-embedding-ada-002")
df["similarities"] = df['embedding'].apply(lambda x: cosine_similarity(x, search_term_vector))
df = df.sort_values("similarities", ascending=False).head(20)
print(df)