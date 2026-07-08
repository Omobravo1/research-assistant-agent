"""
Text Chunking Utility
"""

from langchain_text_splitters import RecursiveCharacterTextSplitter


class TextChunker:

    def __init__(
        self,
        chunk_size=1000,
        chunk_overlap=200,
    ):

        self.splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=[
                "\n\n",
                "\n",
                ". ",
                " ",
                "",
            ],
        )

    def split(self, text):

        return self.splitter.split_text(text)