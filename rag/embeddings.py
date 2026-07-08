"""
Embedding Utility
"""

import os

from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)


class EmbeddingGenerator:

    def __init__(self):

        self.model = "text-embedding-3-small"

    def create_embedding(self, text):

        response = client.embeddings.create(
            model=self.model,
            input=text,
        )

        return response.data[0].embedding

    def create_embeddings(self, chunks):

        embeddings = []

        for chunk in chunks:

            vector = self.create_embedding(chunk)

            embeddings.append(vector)

        return embeddings