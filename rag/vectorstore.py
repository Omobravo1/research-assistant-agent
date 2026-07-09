"""
FAISS Vector Store
"""

import faiss
import numpy as np


class VectorStore:

    def __init__(self):

        self.index = None

        self.documents = []

    def add_document(
        self,
        filename,
        chunks,
        embeddings,
    ):

        embeddings = np.array(
            embeddings,
            dtype="float32",
        )

        if self.index is None:

            dimension = embeddings.shape[1]

            self.index = faiss.IndexFlatL2(dimension)

        self.index.add(embeddings)

        for chunk in chunks:

            self.documents.append(
                {
                    "filename": filename,
                    "chunk": chunk,
                }
            )

    def search(
        self,
        query_embedding,
        k=3,
    ):

        query_embedding = np.array(
            [query_embedding],
            dtype="float32",
        )

        distances, indices = self.index.search(
            query_embedding,
            k,
        )

        results = []

        for index in indices[0]:

            results.append(
                self.documents[index]
            )

        return results

    def count(self):

        if self.index is None:

            return 0

        return self.index.ntotal