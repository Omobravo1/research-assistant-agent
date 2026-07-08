"""
Simple Vector Store

Temporary implementation.

Later we'll replace this with FAISS.
"""

class VectorStore:

    def __init__(self):

        self.documents = []

    def add_document(
        self,
        filename,
        chunks,
        embeddings,
    ):

        for chunk, embedding in zip(chunks, embeddings):

            self.documents.append(
                {
                    "filename": filename,
                    "chunk": chunk,
                    "embedding": embedding,
                }
            )

    def count(self):

        return len(self.documents)

    def all_documents(self):

        return self.documents