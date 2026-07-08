"""
PDF Reader Tool

Responsible for extracting text from uploaded PDF files.
"""

from pypdf import PdfReader


def extract_text_from_pdf(uploaded_file):
    """
    Extract all text from a PDF file.

    Parameters
    ----------
    uploaded_file : UploadedFile
        Streamlit uploaded PDF.

    Returns
    -------
    str
        Complete extracted text.
    """

    reader = PdfReader(uploaded_file)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text