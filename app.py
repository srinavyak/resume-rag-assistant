import streamlit as st
from ask import answer_question

st.set_page_config(page_title="Resume RAG Assistant", page_icon="📄")

st.title("📄 Resume RAG Assistant")
st.caption("Ask questions grounded in Sri Navya's resume and project notes — powered by RAG + Gemini.")

question = st.text_input("Ask a question:", placeholder="e.g. What did she build at Quadrant Resources?")

if question:
    with st.spinner("Retrieving and generating answer..."):
        answer, sources = answer_question(question)

    st.markdown("### Answer")
    st.write(answer)

    if sources:
        st.markdown("### Sources")
        for s in sources:
            st.markdown(f"- {s}")

st.divider()
st.caption("Built with Python, Chroma, and the Gemini API — retrieval-augmented generation over resume/project data.")