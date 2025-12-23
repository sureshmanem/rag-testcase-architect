# Insurance Claim Test Case Generation

This project is a Python application that generates test cases for insurance claims. It uses a local LLM and a vector store to generate new test cases based on existing ones, following a Retrieval-Augmented Generation (RAG) approach.

## Project Structure

- `app.py`: The main Streamlit application for generating test cases.
- `ingest.py`: Script for ingesting and vectorizing existing test cases.
- `prepare_data.py`: Script for preparing the data.
- `insurance_test_cases.csv`: Sample test cases in CSV format.
- `requirements.txt`: Python dependencies for this project.

## Core Components

### `ingest.py`: Data Ingestion

This script is responsible for preparing the local context for the RAG model. It reads existing manual test cases from a CSV file, transforms them into a format suitable for semantic search, and stores them in a local Qdrant vector database.

**Process:**
1.  **Load Data**: Reads test cases from `insurance_test_cases.csv` using pandas.
2.  **Create Documents**: Each row from the CSV is converted into a `LangChain Document`. Key fields like Title, Module, Pre-conditions, Steps, and Expected Result are combined into a single text block for rich contextual embedding.
3.  **Initialize Embeddings**: Uses the `all-MiniLM-L6-v2` model from Hugging Face to generate vector embeddings. This is a small, efficient model that runs locally on the CPU.
4.  **Setup Vector Store**: Connects to a local Qdrant instance and creates a new collection (if one doesn't already exist) named `manual_test_context`.
5.  **Vectorize and Store**: The script processes the documents, generates embeddings for each, and stores the resulting vectors in the Qdrant collection.

This script only needs to be run once to set up the vector store, or whenever the source `insurance_test_cases.csv` file is updated.

### `app.py`: Test Case Generation UI

This is a Streamlit web application that provides a user interface for generating new test suites.

**Workflow:**
1.  **User Input**: The user provides a "user story" or a description of a feature to be tested in the insurance domain.
2.  **Context Retrieval (The "R" in RAG)**: The application takes the user's input and performs a similarity search against the Qdrant vector store. It retrieves the top 2 most similar existing test cases. These serve as "few-shot" examples to guide the LLM on the desired style, format, and level of detail.
3.  **Prompt Engineering**: A detailed prompt is constructed, instructing a local Large Language Model (LLM) to act as a Senior Quality Engineer. The prompt includes the retrieved examples and the new user story.
4.  **Generation (The "G" in RAG)**: The complete prompt is sent to a locally running LLM (via Ollama, using `llama3.2:3b`). The LLM generates a new test suite, including positive, negative, and edge cases, formatted as a markdown table.
5.  **Display and Export**: The generated test suite is displayed in the web interface, and the user can download the results as a text file.

## Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone <repository-url>
    cd test-gen-mvp
    ```

2.  **Create a virtual environment:**
    ```bash
    python3 -m venv venv
    source venv/bin/activate
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
4.  **Setup Local LLM and Vector Store:**
    - Make sure you have [Ollama](https://ollama.ai/) installed and running.
    - Pull the required model: `ollama pull llama3.2:3b`
    - Make sure you have [Docker](https://www.docker.com/) installed and running.
    - Start the Qdrant vector store: 
      ```bash
      docker run -p 6333:6333 qdrant/qdrant
      ```

5.  **Ingest Initial Data:**
    Run the ingestion script to populate the vector store:
    ```bash
    python ingest.py
    ```

## Usage

To run the application, execute the following command:

```bash
streamlit run app.py
```

The application will be available at `http://localhost:8501`.

