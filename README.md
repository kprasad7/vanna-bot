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
