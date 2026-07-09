"""
Retriever
"""

from rag.embeddings import EmbeddingGenerator


class Retriever:

    def __init__(self, vector_store):

        self.vector_store = vector_store

        self.embedding_generator = EmbeddingGenerator()

    def retrieve(
        self,
        question,
        k=3,
    ):

        query_embedding = self.embedding_generator.create_embedding(
            question
        )

        return self.vector_store.search(
            query_embedding,
            k,
        )