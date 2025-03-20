import os
import time
import faiss
import numpy as np
import pickle
import logging
from config import LocalEmbedding

# Setup logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

GITHUB_REPO_URL = "https://github.com/vanna-ai/vanna"
LOCAL_REPO_DIR = "vanna_repo"
INDEX_FILE = "vector_index.faiss"
METADATA_FILE = "metadata.pkl"
FULL_FILE_INDEX_FILE = "full_file_index.faiss"
FULL_FILE_METADATA_FILE = "full_file_metadata.pkl"
CHUNK_SIZE = 1000
BINARY_EXTENSIONS = (".png", ".jpg", ".jpeg", ".gif", ".pdf", ".exe", ".zip", ".mp4", ".mp3")

def get_github_url(file_path: str) -> str:
    relative_path = os.path.relpath(file_path, LOCAL_REPO_DIR).replace("\\", "/")
    return f"{GITHUB_REPO_URL}/blob/main/{relative_path}"

def get_local_files() -> list:
    relevant_files = []
    for root, _, files in os.walk(LOCAL_REPO_DIR):
        if ".git" in root:
            continue
        for file in files:
            if file.lower().endswith(BINARY_EXTENSIONS):
                continue
            relevant_files.append(os.path.join(root, file))
    logging.info(f"Found {len(relevant_files)} text files.")
    return relevant_files

def fetch_file_content(file_path: str) -> str:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            return f.read()
    except Exception as e:
        logging.error(f"Error reading {file_path}: {e}")
        return ""

def chunk_text(text: str) -> list:
    chunks, start, text_length = [], 0, len(text)
    while start < text_length:
        end = start + CHUNK_SIZE
        newline_index = text.rfind('\n', start, end)
        if newline_index != -1 and newline_index > start:
            end = newline_index
        chunks.append(text[start:end])
        start = end
    return chunks

def index_repository():
    start_time = time.time()
    file_paths = get_local_files()
    embedder = LocalEmbedding()
    
    index, full_file_index = None, None
    metadata, full_file_metadata = [], []
    
    for path in file_paths:
        content = fetch_file_content(path)
        if not content:
            continue

        chunks = chunk_text(content)
        try:
            embeddings = [embedder.embed(chunk) for chunk in chunks]
            full_file_embedding = embedder.embed(content)
        except Exception as e:
            logging.error(f"Embedding error in file {path}: {e}")
            continue

        if embeddings and index is None:
            vector_dim = len(embeddings[0])
            index = faiss.IndexFlatL2(vector_dim)
            full_file_index = faiss.IndexFlatL2(vector_dim)

        for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
            index.add(np.array([embedding]).astype("float32"))
            metadata.append({
                "file": os.path.relpath(path, LOCAL_REPO_DIR),
                "github_url": get_github_url(path),
                "chunk": i,
                "content": chunk
            })
        
        # Add full file embedding
        full_file_index.add(np.array([full_file_embedding]).astype("float32"))
        full_file_metadata.append({
            "file": os.path.relpath(path, LOCAL_REPO_DIR),
            "github_url": get_github_url(path),
            "content": content
        })

    if index is None:
        logging.error("No embeddings were added to the index.")
        return

    try:
        faiss.write_index(index, INDEX_FILE)
        with open(METADATA_FILE, "wb") as f:
            pickle.dump(metadata, f)

        faiss.write_index(full_file_index, FULL_FILE_INDEX_FILE)
        with open(FULL_FILE_METADATA_FILE, "wb") as f:
            pickle.dump(full_file_metadata, f)
        
        logging.info(f"Indexed {len(metadata)} chunks and {len(full_file_metadata)} full files in {time.time() - start_time:.2f} seconds.")
    except Exception as e:
        logging.error(f"Error saving index or metadata: {e}")

def retrieve_code(file_name: str):
    try:
        with open(FULL_FILE_METADATA_FILE, "rb") as f:
            full_file_metadata = pickle.load(f)
        for data in full_file_metadata:
            if file_name in data["file"]:
                return data["content"]
    except Exception as e:
        logging.error(f"Error retrieving file content: {e}")
    return "File not found."

if __name__ == "__main__":
    index_repository()
