# Minimal End-to-End Vanna Repository Indexing & Q&A Solution

## 📌 Overview
This project provides a minimal end-to-end solution that indexes the `vanna-ai/vanna` repository from GitHub and enables a Q&A interface using local embeddings (Hugging Face) and FastAPI.

## 🚀 Features
- **Automated GitHub Repository Indexing** – Clones the `vanna-ai/vanna` repo and processes all relevant text-based files.
- **Local Embeddings for Search** – Uses Hugging Face models to generate embeddings for repository files.
- **Efficient FAISS-Based Retrieval** – Enables fast, vector-based lookup of relevant file content.
- **GitHub File Linking** – Each indexed file includes a direct GitHub link for easy reference.
- **FastAPI-Powered Q&A Interface** – Users can ask questions about the repo’s code, structure, and files.
- **Claude 2.0 Integration (AWS Bedrock)** – Enhances responses by summarizing relevant content.

## 🛠️ Installation & Setup

### 1️⃣ Clone the Repository
```bash
https://github.com/kprasad7/vanna-bot/tree/main
cd vanna-bot
```

### 2️⃣ Set Up a Virtual Environment (Recommended)
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Run Indexing
```bash
python indexing.py
```
This step embeds the repository using Hugging Face models and stores it in a FAISS index.

### 5️⃣ Start the FastAPI Server
```bash
python -m uvicorn main:app --host 0.0.0.0 --port 5500 --reload --log-level debug

```
The server runs at [http://127.0.0.1:8000](http://127.0.0.1:8000).

## ✅ Requirements
- Python 3.8 or higher.
- The following Python packages (see `requirements.txt`):
  - `fastapi`
  - `uvicorn`
  - `requests`
  - `sentence-transformers`  
  - `numpy`
  - `faiss-cpu`
  - `boto3`
  - `pydantic`
  - `pickle`

## 🔧 Configuration
- The project uses `config.py` to configure the embedding model (`sentence-transformers`).
- FAISS indexes are stored in `vector_index.faiss`.
- Metadata for indexed files is stored in `metadata.pkl`.

## 🏗 Usage

### 1️⃣ Index Documents
Run the following command to index text files in the repository:
```bash
python indexing.py
```
This will create:
- `vector_index.faiss` → FAISS index of embeddings
- `metadata.pkl` → Metadata about indexed files

### 2️⃣ Start the API Server
Once the index is built, start the FastAPI server:
```bash
python main.py
```
The API will be accessible at:
- [http://localhost:5500/](http://localhost:5500/) → Serves the UI
- [http://localhost:5500/ask](http://localhost:5500/ask) → Handles search queries

### 3️⃣ Query the API
Send a search query using `curl`:
```bash
curl -X POST "http://localhost:5500/ask" -H "Content-Type: application/json" \
     -d '{"question": "What is the code in indexing.py?"}'
```

## 📜 API Endpoints
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Serves the UI |
| POST | `/ask` | Retrieves relevant file content |

## 📦 Dependencies
This project uses the following Python packages:
- `faiss-cpu`
- `sentence-transformers`
- `numpy`
- `fastapi`
- `uvicorn`
- `boto3`
- `pydantic`
- `pickle`
- 

**To use Postman for testing this endpoint, you should set up a POST request to the full URL where your backend is running. For example, if you're running the backend locally on port 5500, you would use:

bash
Copy
http://localhost:5500/ask
In Postman:

Method: Set to POST.
URL: Enter http://localhost:5500/ask.
Headers:
Key: Content-Type
Value: application/json
Body: Choose the raw option and select JSON. Then include a JSON payload similar to the following:
json
Copy
{
  "question": "What is the code in main.py?",
  "sessionId": "your-session-id"
}**

## 🔗 License
This project follows the license of the `vanna-ai/vanna` repository.
