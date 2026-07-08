import streamlit as st
from agent.llm import ask_llm

# -------------------------
# Page Configuration
# -------------------------

st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------
# Session State
# -------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

# -------------------------
# Sidebar
# -------------------------

with st.sidebar:

    st.title("🔬 Research Assistant")

    st.markdown("---")

    uploaded_files = st.file_uploader(
        "Upload Research Papers (PDF)",
        type=["pdf"],
        accept_multiple_files=True
    )

    st.markdown("---")

    if st.button("🗑 Clear Chat"):
        st.session_state.messages = []
        st.rerun()

    st.button("📄 Generate Report")

    st.button("⚙ Settings")

    st.markdown("---")

    st.info(
        """
        **Version:** 1.0

        Built using:

        - Streamlit
        - OpenAI
        - LangChain
        - FAISS
        """
    )

# -------------------------
# Main Page
# -------------------------

st.title("🔬 AI Research Assistant")

st.caption(
    "Search the web, analyze research papers, and generate professional reports."
)

# -------------------------
# Display Chat History
# -------------------------

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -------------------------
# Chat Input
# -------------------------

prompt = st.chat_input("Ask me anything...")

if prompt:

    # Save and display the user's message
    st.session_state.messages.append(
        {
            "role": "user",
            "content": prompt
        }
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI response
    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            response = ask_llm(prompt)

            st.markdown(response)

    # Save the assistant's response
    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response
        }
    )