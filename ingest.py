import pandas as pd
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_qdrant import QdrantVectorStore
from qdrant_client import QdrantClient
from qdrant_client.http.models import Distance, VectorParams

# Configuration
CSV_FILE = "insurance_test_cases.csv"
COLLECTION_NAME = "manual_test_context"
QDRANT_URL = "http://localhost:6333"

def ingest_data():
    # 1. Load the CSV data using Pandas
    print(f"Reading {CSV_FILE}...")
    df = pd.read_csv(CSV_FILE)
    
    # 2. Convert CSV rows into LangChain Documents
    # We combine columns into a single string for better embedding context
    documents = []
    for _, row in df.iterrows():
        content = f"Title: {row['Title']}\nModule: {row['Module']}\nPre-conditions: {row['Pre-conditions']}\nSteps: {row['Steps']}\nExpected Result: {row['Expected Result']}"
        metadata = {"id": row['ID'], "module": row['Module']}
        documents.append(Document(page_content=content, metadata=metadata))
    
    # 3. Initialize Local Embeddings (Runs on your CPU)
    # This model is small, fast, and great for text similarity
    print("Initializing embedding model (all-MiniLM-L6-v2)...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    
    # 4. Set up Qdrant Client
    client = QdrantClient(url=QDRANT_URL)
    
    # Create collection if it doesn't exist
    # Using 384 dimensions for all-MiniLM-L6-v2
    vectors_config = VectorParams(size=384, distance=Distance.COSINE)
    
    if not client.collection_exists(COLLECTION_NAME):
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=vectors_config
        )
        print(f"Created collection: {COLLECTION_NAME}")

    # 5. Store documents in Qdrant
    print(f"Vectorizing and storing {len(documents)} test cases...")
    QdrantVectorStore.from_documents(
        documents=documents,
        embedding=embeddings,
        url=QDRANT_URL,
        collection_name=COLLECTION_NAME,
    )
    
    print("✅ Ingestion complete! Your local context is ready.")

if __name__ == "__main__":
    try:
        ingest_data()
    except Exception as e:
        print(f"❌ Error: {e}. Ensure Qdrant is running on {QDRANT_URL}")