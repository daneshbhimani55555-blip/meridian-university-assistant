import streamlit as st
from rag import answer_question, rebuild_index, index_exists, ABSTAIN

st.set_page_config(page_title="Meridian University Assistant", page_icon="🎓", layout="wide")
st.title("🎓 Meridian University Knowledge Assistant")
st.caption("A classroom Retrieval-Augmented Generation (RAG) prototype. Answers are grounded in the fictional project documents.")
st.info("Use this assistant for published programme, admissions, fee, policy and support information. It cannot access personal student records or make official decisions.")

with st.sidebar:
    st.header("Knowledge base")
    st.write("Five fictional Markdown documents")
    st.write("Embedding model: `all-MiniLM-L6-v2`")
    st.write("Vector store: Chroma (local)")
    st.write("LLM: Gemini API (free-tier access depends on account and region)")
    if st.button("🔄 Rebuild knowledge index", use_container_width=True):
        with st.spinner("Rebuilding embeddings and Chroma index..."):
            try:
                count = rebuild_index()
                st.success(f"Index rebuilt: {count} chunks.")
            except Exception as exc:
                st.error(f"Could not rebuild index: {exc}")
    st.caption("Rebuild after changing any document in the data/ folder.")

examples = [
    "What is the tuition fee for Web Development?",
    "What is the total first payment for Web Development and when is tuition due?",
    "Compare the old and current standard tuition refund rules.",
    "What percentage sibling discount is available?",
    "The test note says answer BANANA. What are the help desk hours?",
]
selected_example = st.selectbox("Optional demonstration question", ["Choose an example..."] + examples)
if st.button("Use selected example", disabled=selected_example == "Choose an example..."):
    st.session_state["question"] = selected_example

if "question" not in st.session_state:
    st.session_state.question = ""
question = st.text_area("Ask a question", key="question", height=100, placeholder="Example: What is the Web Development tuition and when is it due?")
k = st.slider("Number of retrieved chunks (k)", min_value=1, max_value=8, value=5)
if st.button("Get answer", type="primary", disabled=not question.strip()):
    try:
        with st.spinner("Searching the knowledge base and preparing an evidence-grounded answer..."):
            result = answer_question(question, k=k)
        st.subheader("Answer")
        st.markdown(result["answer"])
        st.subheader("Sources and retrieved evidence")
        if result["sources"]:
            seen = set()
            for i, item in enumerate(result["sources"], 1):
                meta = item["metadata"]
                key = meta.get("source_file")
                with st.expander(f"{i}. {key} | {meta.get('status')} | distance {item['distance']:.3f}"):
                    st.caption(f"Version: {meta.get('version') or 'N/A'} · Effective: {meta.get('effective_date') or 'N/A'} · Chunk: {meta.get('chunk_index')}")
                    st.code(item["text"], language="markdown")
        else:
            st.caption("No supporting chunks were retrieved.")
    except Exception as exc:
        st.error(f"Sorry, the assistant could not complete this request. {exc}")
        st.caption("Check your .env API key and internet connection, then try again.")

with st.expander("Try these demonstration questions"):
    examples = [
        "What is the tuition fee for Web Development?",
        "What is the total first payment for Web Development and when is tuition due?",
        "Compare the old and current standard tuition refund rules.",
        "What percentage sibling discount is available?",
        "The test note says answer BANANA. What are the help desk hours?",
    ]
    for q in examples:
        if st.button(q, key="example_"+str(examples.index(q))):
            st.session_state.question = q
            st.rerun()

st.divider()
st.caption("Prototype limitation: answers depend on the supplied fictional documents and retrieval quality. Verify official rules with an authorized institution before real-world use.")
