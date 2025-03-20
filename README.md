# vanna-bot

A minimal end-to-end solution that indexes the [vanna-ai/vanna](https://github.com/vanna-ai/vanna) repository (public GitHub) and provides a Q&A interface using local embeddings (Hugging Face) and FastAPI.

## Features

- **No external clone needed**: Fetches files from GitHub.
- **Local Embeddings**: Uses `sentence-transformers` to embed text.
- **In-Memory VectorStore**: No external database needed.
- **FastAPI**: Exposes a `/ask` endpoint for Q&A.
- **HTML/CSS/JS**: Minimal front-end to query the backend.
- **Out-of-Scope Handling**: If no relevant context, respond with an out-of-scope message.
- **References**: Return the files used for each answer.

## Requirements

- Python 3.8 or higher.
- The following Python packages (see `requirements.txt`):
  - `fastapi`
  - `uvicorn`
  - `requests`
  - `sentence-transformers`  
  - `numpy`

Install via:

```bash
pip install -r requirements.txt


2️⃣ Set up a virtual environment (recommended)
bash
Copy
Edit
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
3️⃣ Install dependencies
bash
Copy
Edit
pip install -r requirements.txt
🔧 Configuration
The project uses config.py to configure the embedding model (sentence-transformers).
FAISS indexes are stored in vector_index.faiss.
Metadata for indexed files is stored in metadata.pkl.
🏗 Usage
1️⃣ Index documents
Run the following command to index text files in the repository:

bash
Copy
Edit
python indexing.py
This will create:

vector_index.faiss → FAISS index of embeddings
metadata.pkl → Metadata about indexed files
2️⃣ Start the API Server
Once the index is built, start the FastAPI server:

bash
Copy
Edit
python main.py
The API will be accessible at:

http://localhost:5500/ → Serves the UI
http://localhost:5500/ask → Handles search queries
3️⃣ Query the API
Send a search query using curl:

bash
Copy
Edit
curl -X POST "http://localhost:5500/ask" -H "Content-Type: application/json" \
     -d '{"question": "What is the code in indexing.py?"}'
📜 API Endpoints
Method	Endpoint	Description
GET	/	Serve the UI
POST	/ask	Retrieve relevant file content
📦 Dependencies
This project uses the following Python packages:

faiss-cpu
sentence-transformers
numpy
fastapi
uvicorn
boto3
pydantic
pickle
