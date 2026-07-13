import os
import streamlit as st

from rag.embeddings import EmbeddingGenerator
from rag.vectorstore import VectorStore
from agent.orchestrator import ResearchAgent
from tools.pdf_reader import PDFReader
from rag.chunker import TextChunker
from rag.retriever import Retriever
from tools.report_generator import ReportGenerator

# ---------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------

st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔬",
    layout="wide",
)

# ---------------------------------------------------
# SERVICES
# ---------------------------------------------------

agent = ResearchAgent()
report_generator = ReportGenerator()
pdf_reader = PDFReader()
chunker = TextChunker()
embedding_generator = EmbeddingGenerator()
vector_store = VectorStore()
retriever = Retriever(vector_store)
# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "documents" not in st.session_state:
    st.session_state.documents = []

if "last_question" not in st.session_state:
    st.session_state.last_question = ""

if "last_answer" not in st.session_state:
    st.session_state.last_answer = ""

if "last_sources" not in st.session_state:
    st.session_state.last_sources = []

if "report_ready" not in st.session_state:
    st.session_state.report_ready = False

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

with st.sidebar:

    st.title("🔬 Research Assistant")

    uploaded_files = st.file_uploader(
        "Upload Research Papers",
        type="pdf",
        accept_multiple_files=True,
    )

    if uploaded_files:

        st.markdown("---")

        st.subheader("📚 Uploaded Papers")

        total_chunks = 0

        for pdf in uploaded_files:

            pdf.seek(0)

            stats = pdf_reader.get_statistics(pdf)

            if not stats["text"].strip():

                st.error(
                    f"{pdf.name} contains no extractable text.\n\n"
                    "It is likely a scanned PDF. OCR is required to process this document."
                )

                continue

            chunks = chunker.split(stats["text"])

            if not chunks:

                st.warning(f"No text chunks could be created from {pdf.name}.")

                continue

            embeddings = embedding_generator.create_embeddings(chunks)

            vector_store.add_document(pdf.name, chunks, embeddings)

            total_chunks += len(chunks)

            st.session_state.documents.append(
                {
                    "name": pdf.name,
                    "pages": stats["pages"],
                    "words": stats["words"],
                    "characters": stats["characters"],
                    "text": stats["text"],
                    "chunks": chunks,
                }
            )

            st.success(pdf.name)

            st.caption(
                                f"""
                Pages: {stats['pages']}

                Words: {stats['words']:,}

                Characters: {stats['characters']:,}

                Chunks: {len(chunks)}
                """
            )

            st.info(
                """
                ✅ Upload one or more research papers.

                🌐 Ask questions about uploaded papers or current topics.

                📄 Generate a downloadable research report.
                """
            )

            with st.expander("Preview First Chunk"):

                st.write(chunks[0][:1000])

        st.markdown("---")

        st.info(f"Total Chunks: {total_chunks}")
        st.success(f"Vectors Stored: {vector_store.count()}")

        st.markdown("---")

        if st.button("📄 Generate Report"):

            if st.session_state.last_answer:

                REPORT_DIR = os.path.join(os.getcwd(), "reports")
                os.makedirs(REPORT_DIR, exist_ok=True)

                filename = os.path.join(REPORT_DIR, "research_report.pdf")

                report_generator.generate(
                    filename,
                    st.session_state.last_question,
                    st.session_state.last_answer,
                    st.session_state.last_sources,
)

                st.session_state.report_ready = True

            else:

                st.warning("Ask a research question first.")

        if st.session_state.report_ready:

            with open("reports/research_report.pdf", "rb") as file:

                st.download_button(
                    label="⬇ Download Report",
                    data=file,
                    file_name="Research_Report.pdf",
                    mime="application/pdf",
                )

        st.markdown("---")

        if st.button("🗑 Clear Chat"):

            st.session_state.messages = []
            st.session_state.documents = []
            st.session_state.last_question = ""
            st.session_state.last_answer = ""
            st.session_state.last_sources = []
            st.session_state.report_ready = False

            
            st.rerun()
# ---------------------------------------------------
# MAIN PAGE
# ---------------------------------------------------

st.title("🔬 AI Research Assistant")

st.caption("Research papers • Web Search • AI")

# ---------------------------------------------------
# CHAT HISTORY
# ---------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# ---------------------------------------------------
# CHAT INPUT
# ---------------------------------------------------

prompt = st.chat_input("Ask a research question...")

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt,
        }
    )

    with st.chat_message("user"):

        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            context = None
            sources = []

            if vector_store.count() > 0:

                retrieved_chunks = retriever.retrieve(prompt)

                context = "\n\n".join(
                    chunk["chunk"]
                    for chunk in retrieved_chunks
                )

                sources = list(
                    set(
                        chunk["filename"]
                        for chunk in retrieved_chunks
                    )
                )

                st.session_state.last_sources = sources
            
            response = agent.process(
                prompt,
                context,
            )

            st.session_state.last_question = prompt
            st.session_state.last_answer = response

            st.markdown(response)

            if vector_store.count() > 0 and sources:

                st.markdown("---")

                st.markdown("### 📚 Sources Used")

                for source in sources:

                    st.write(f"📄 {source}")

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )