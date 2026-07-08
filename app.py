import streamlit as st

from agent.orchestrator import ResearchAgent
from tools.pdf_reader import PDFReader

# ---------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------

st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔬",
    layout="wide",
)

# ---------------------------------------------------
# AGENT
# ---------------------------------------------------

agent = ResearchAgent()

pdf_reader = PDFReader()

# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

if "documents" not in st.session_state:
    st.session_state.documents = []

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

        st.session_state.documents = []

        st.markdown("---")

        st.subheader("📚 Uploaded Papers")

        for pdf in uploaded_files:

            pdf.seek(0)

            stats = pdf_reader.get_statistics(pdf)

            st.session_state.documents.append(stats)

            st.success(pdf.name)

            st.caption(
                f"""
Pages: {stats['pages']}

Words: {stats['words']:,}

Characters: {stats['characters']:,}
"""
            )

    st.markdown("---")

    if st.button("🗑 Clear Chat"):

        st.session_state.messages = []

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

            response = agent.process(prompt)

            st.markdown(response)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )