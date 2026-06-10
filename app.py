from backend import ask_pdf, generate_summary, generate_mcqs, generate_flashcards
import streamlit as st

# =========================
# PAGE CONFIG
# =========================
st.set_page_config(
    page_title="EduGenie",
    page_icon="📚",
    layout="wide"
)

# =========================
# SIDEBAR
# =========================
with st.sidebar:
    st.title("📚 EduGenie")

    pdf_file = st.file_uploader(
        "Upload PDF",
        type=["pdf"]
    )

    st.divider()

    st.subheader("📜 History")
    st.write("Previous questions will appear here")

    st.divider()

    st.subheader("ℹ️ About")
    st.write("AI-Powered Learning Assistant")

# =========================
# MAIN PAGE
# =========================
st.title("📚 EduGenie")
st.markdown("### Learn Smarter with AI")

col1, col2 = st.columns(2)

with col1:
    st.subheader("💬 Ask Questions")

    question = st.text_input(
        "Enter your question"
    )

    if st.button("Ask"):
        st.success("Answer will appear here")

with col2:
    st.subheader("🧠 Study Tools")

    if st.button("📝 Generate Summary"):
        st.info("Summary will appear here")

    if st.button("❓ Generate MCQs"):
        st.info("MCQs will appear here")

    if st.button("💡 Explain Simply"):
        st.info("Simple explanation will appear here")

st.divider()

st.subheader("📄 Output")
st.write("Results will be displayed here.")
