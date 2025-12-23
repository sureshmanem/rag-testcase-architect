import streamlit as st
import pandas as pd
import io
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from langchain_ollama import OllamaLLM
from qdrant_client import QdrantClient

# --- CONFIGURATION ---
QDRANT_URL = "http://localhost:6333"
COLLECTION_NAME = "manual_test_context"
MODEL_NAME = "llama3.2:3b"  # Ensure you ran 'ollama pull llama3.2:3b'

# --- UI HEADER ---
st.set_page_config(page_title="GenAI Test Case Generator", layout="wide")
st.title("🧪 GenAI Manual Test Case Generator")
st.markdown("Generate professional insurance test cases locally using RAG.")

# --- SIDEBAR: STATUS & CONFIG ---
with st.sidebar:
    st.header("Settings")
    st.info(f"LLM: {MODEL_NAME}\n\nVector Store: Qdrant (Local)")
    
    # Optional: Quick check if Qdrant is alive
    try:
        client = QdrantClient(url=QDRANT_URL)
        count = client.get_collection(collection_name=COLLECTION_NAME).points_count
        st.success(f"Context Ready: {count} cases indexed.")
    except Exception:
        st.error("Qdrant not connected. Run 'ingest.py' first.")

# --- MAIN LOGIC ---
user_story = st.text_area("Paste User Story (Insurance Domain):", 
                          placeholder="Example: As a customer, I want to pay my premium using a digital wallet like PayPal...",
                          height=200)

if st.button("Generate Test Suite"):
    if not user_story:
        st.warning("Please enter a user story first.")
    else:
        with st.spinner("🔍 Fetching style context and generating tests..."):
            try:
                # 1. Setup Embeddings and Vector Store
                embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
                vector_store = QdrantVectorStore.from_existing_collection(
                    embedding=embeddings,
                    collection_name=COLLECTION_NAME,
                    url=QDRANT_URL
                )

                # 2. Retrieve top 2 similar test cases for context
                search_results = vector_store.similarity_search(user_story, k=2)
                context_text = "\n---\n".join([doc.page_content for doc in search_results])

                # 3. Initialize Local LLM (Ollama)
                llm = OllamaLLM(model=MODEL_NAME)

                # 4. Construct the Prompt
                prompt = f"""
                You are a Senior Quality Engineer in the Insurance Domain.
                Use the following EXISTING TEST CASES as examples of the required style, level of detail, and formatting:
                
                {context_text}
                
                NEW USER STORY TO TEST:
                {user_story}
                
                TASK: Generate a set of manual test cases (Positive, Negative, and Edge Cases).
                FORMAT: Return a markdown table with columns: ID, Title, Pre-conditions, Steps, Expected Result.
                """

                # 5. Generate Response
                response = llm.invoke(prompt)

                # 6. Display Results
                st.subheader("Generated Manual Test Suite")
                st.markdown(response)

                # --- EXPORT TO CSV (Simple Parser) ---
                st.download_button(
                    label="Download Results as Text",
                    data=response,
                    file_name="generated_tests.txt",
                    mime="text/plain"
                )

            except Exception as e:
                st.error(f"An error occurred: {e}")

# --- FOOTER ---
st.divider()
st.caption("Powered by LangChain + Qdrant + Ollama | 100% Local & Private")