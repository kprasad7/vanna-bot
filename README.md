 Minimal End-to-End Vanna Repository Indexing & Q&A Solution
📌 Overview
This project provides a minimal end-to-end solution that indexes the vanna-ai/vanna repository from GitHub and enables a Q&A interface using local embeddings (Hugging Face) and FastAPI.

🚀 Features
✔ Automated GitHub Repository Indexing – Clones the vanna-ai/vanna repo and processes all relevant text-based files.
✔ Local Embeddings for Search – Uses Hugging Face models to generate embeddings for repository files.
✔ Efficient FAISS-Based Retrieval – Enables fast, vector-based lookup of relevant file content.
✔ GitHub File Linking – Each indexed file includes a direct GitHub link for easy reference.
✔ FastAPI-Powered Q&A Interface – Users can ask questions about the repo’s code, structure, and files.
✔ Claude 2.0 Integration (AWS Bedrock) – Enhances responses by summarizing relevant content.

🛠️ Installation & Setup
1️⃣ Clone the Repository
sh
Copy
Edit
git clone https://github.com/vanna-ai/vanna.git vanna_repo
cd vanna_repo
2️⃣ Install Dependencies
sh
Copy
Edit
pip install -r requirements.txt
3️⃣ Run Indexing
sh
Copy
Edit
python indexing.py
This step embeds the repository using Hugging Face models and stores it in a FAISS index.

4️⃣ Start the FastAPI Server
sh
Copy
Edit
uvicorn main:app --reload
The server runs at http://127.0.0.1:8000
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
