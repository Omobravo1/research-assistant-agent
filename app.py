import streamlit as st

from agent.orchestrator import ResearchAgent

from tools.pdf_reader import extract_text_from_pdf

# ---------------------------------------------------
# PAGE CONFIGURATION
# ---------------------------------------------------

st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------
# CREATE AGENT
# ---------------------------------------------------

agent = ResearchAgent()

# ---------------------------------------------------
# SESSION STATE
# ---------------------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------------------------------------------------
# SIDEBAR
# ---------------------------------------------------

with st.sidebar:

    st.title("🔬 Research Assistant")

    st.markdown("---")

    uploaded_files = st.file_uploader(
        "Upload Research Papers",
        type=["pdf"],
        accept_multiple_files=True
    )

    if uploaded_files: st.success(f"{len(uploaded_files)} PDF(s) uploaded.")

    for pdf in uploaded_files:

        text = extract_text_from_pdf(pdf)

        st.write(f"📄 {pdf.name}")

        st.write(f"Characters extracted: {len(text):,}")

        with st.expander("Preview"):

            st.write(text[:1000])

    st.markdown("---")

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.button("📄 Generate Report")

    st.button("⚙ Settings")

    st.markdown("---")

    st.success("Agent Status: Online")

# ---------------------------------------------------
# MAIN PAGE
# ---------------------------------------------------

st.title("🔬 AI Research Assistant")

st.caption(
    "Search the web, analyze research papers, and generate professional reports."
)

# ---------------------------------------------------
# CHAT HISTORY
# ---------------------------------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------------------------------------------
# CHAT INPUT
# ---------------------------------------------------

prompt = st.chat_input("Ask me anything...")

if prompt:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):

        with st.spinner("Researching..."):

            response = agent.process(prompt)

            st.markdown(response)

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )