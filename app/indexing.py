import os
import time
import faiss
import numpy as np
import pickle
from config import LocalEmbedding


GITHUB_REPO_URL = "https://github.com/vanna-ai/vanna"
LOCAL_REPO_DIR = "vanna_repo"
INDEX_FILE = "vector_index.faiss"
METADATA_FILE = "metadata.pkl"
CHUNK_SIZE = 1000  # Max characters per chunk


BINARY_EXTENSIONS = (".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".ico", 
                     ".pdf", ".exe", ".zip", ".tar", ".gz", ".rar", ".7z", 
                     ".mp4", ".mp3", ".pack", ".idx", ".rev")

def get_github_url(file_path):
    """ Convert local file path to a GitHub URL. """
    relative_path = file_path.replace(LOCAL_REPO_DIR + "/", "").replace("\\", "/")
    return f"{GITHUB_REPO_URL}/blob/main/{relative_path}"

def get_local_files():
    """ Retrieve all text files in the repository, ignoring binary files. """
    relevant_files = []
    for root, _, files in os.walk(LOCAL_REPO_DIR):
        for file in files:
            if file.endswith(BINARY_EXTENSIONS) or ".git" in root:
                continue  # Ignore binary & .git files
            full_path = os.path.join(root, file)
            relevant_files.append(full_path)
    return relevant_files

def is_binary(file_path):
    """ Check if a file is binary by reading the first few bytes. """
    try:
        with open(file_path, "rb") as f:
            return b"\0" in f.read(1024)  # If NULL byte is found, it's binary
    except Exception:
        return True  # Treat unreadable files as binary

def fetch_file_content(file_path: str) -> str:
    """ Read file content, ignoring binary files. """
    if is_binary(file_path):
        print(f"⚠️ Skipping binary file: {file_path}")
        return ""

    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return file.read()
    except UnicodeDecodeError:
        print(f"⚠️ Skipping unreadable text file: {file_path}")
        return ""
    except Exception as e:
        print(f"❌ Error reading {file_path}: {e}")
        return ""

def chunk_text(text: str) -> list:
    """ Split text into smaller chunks. """
    return [text[i:i+CHUNK_SIZE] for i in range(0, len(text), CHUNK_SIZE)]

def index_repository():
    """ Index repository with embeddings and store file URLs. """
    start_time = time.time()
    file_paths = get_local_files()
    
    embedder = LocalEmbedding()
    index = None
    metadata = []

    for path in file_paths:
        content = fetch_file_content(path)
        if not content:
            continue

        chunks = chunk_text(content)
        embeddings = [embedder.embed(chunk) for chunk in chunks]
        
        if index is None:
            index = faiss.IndexFlatL2(len(embeddings[0]))

        for i, embedding in enumerate(embeddings):
            index.add(np.array([embedding]).astype('float32'))
            metadata.append({
                "file": path.replace(LOCAL_REPO_DIR + "/", ""),
                "github_url": get_github_url(path),
                "chunk": i,
                "content": chunks[i]
            })

    faiss.write_index(index, INDEX_FILE)
    with open(METADATA_FILE, "wb") as f:
        pickle.dump(metadata, f)

    print(f"\n✅ Indexed {len(metadata)} chunks in {time.time() - start_time:.2f} seconds.")

if __name__ == "__main__":
    index_repository()
