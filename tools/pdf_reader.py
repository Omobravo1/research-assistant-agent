"""
PDF Reader Tool
"""

from pypdf import PdfReader


class PDFReader:

    def extract_text(self, uploaded_file):

        reader = PdfReader(uploaded_file)

        text = ""

        for page in reader.pages:

            page_text = page.extract_text()

            if page_text:

                text += page_text + "\n"

        return text

    def get_page_count(self, uploaded_file):

        reader = PdfReader(uploaded_file)

        return len(reader.pages)

    def get_statistics(self, uploaded_file):

        text = self.extract_text(uploaded_file)

        uploaded_file.seek(0)

        pages = self.get_page_count(uploaded_file)

        uploaded_file.seek(0)

        words = len(text.split())

        characters = len(text)

        return {
            "pages": pages,
            "words": words,
            "characters": characters,
            "text": text,
        }