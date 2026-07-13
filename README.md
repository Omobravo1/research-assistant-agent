# 🔬 AI Research Assistant

An AI-powered Research Assistant that allows users to upload research papers (PDFs), ask questions about their contents, retrieve relevant information using Retrieval-Augmented Generation (RAG), and generate professional research reports.

---

## Features

- Upload one or multiple PDF research papers
- Extract and process text from PDFs
- Semantic search using OpenAI Embeddings
- FAISS Vector Database
- Retrieval-Augmented Generation (RAG)
- AI-powered question answering
- Source attribution
- Generate downloadable PDF research reports
- Friendly error handling for scanned/non-extractable PDFs

---

## Technologies Used

- Python
- Streamlit
- OpenAI API
- LangChain
- FAISS
- PyMuPDF
- ReportLab

---

## Architecture

User Uploads PDF
↓
PyMuPDF extracts text
↓
Text Chunking
↓
OpenAI Embeddings
↓
FAISS Vector Store
↓
Retriever
↓
OpenAI GPT-4.1-mini
↓
Research Answer
↓
Generate PDF Report

---

## Installation

Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/research-assistant-agent.git
cd research-assistant-agent
```

Create virtual environment

```bash
python -m venv .venv
```

Activate

Windows

```bash
.venv\Scripts\activate
```

Linux / macOS

```bash
source .venv/bin/activate
```

Install dependencies

```bash
pip install -r requirements.txt
```

Create a `.env` file

```
OPENAI_API_KEY=your_openai_key
TAVILY_API_KEY=your_tavily_key
```

Run

```bash
streamlit run app.py
```

---

## Known Limitations

- Designed primarily for text-based PDFs.
- Some scanned, image-based, or DRM-protected PDFs may not contain extractable text.
- OCR support is planned for a future version.

---

## Future Improvements

- OCR support
- Citation generation
- Research paper comparison
- Web search integration
- Conversation memory
- Export to Word

---

## Author

Prince Osiohwo Osiohwo

Capstone Project
Agentic AI / Machine Learning