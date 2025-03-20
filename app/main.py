import json
import time
import faiss
import pickle
import numpy as np
import boto3
import os
from fastapi import FastAPI
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from config import LocalEmbedding


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


bedrock_client = boto3.client("bedrock-runtime", region_name="us-east-1")


ui_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../ui"))
app.mount("/ui", StaticFiles(directory=ui_path), name="ui")

INDEX_FILE = "vector_index.faiss"
METADATA_FILE = "metadata.pkl"

if not os.path.exists(INDEX_FILE) or not os.path.exists(METADATA_FILE):
    raise RuntimeError("❌ FAISS index or metadata file is missing. Run `indexing.py` first.")

index = faiss.read_index(INDEX_FILE)
with open(METADATA_FILE, "rb") as f:
    metadata = pickle.load(f)

class AskPayload(BaseModel):
    question: str

@app.get("/")
async def serve_home():
    """ Serve the frontend UI. """
    return FileResponse(f"{ui_path}/index.html")

def call_claude_2(prompt):
    """ Call Claude 2.0 via AWS Bedrock with properly formatted request. """
    try:
        payload = {
            "prompt": f"\n\nHuman: {prompt}\n\nAssistant:",
            "max_tokens_to_sample": 300
        }

        response = bedrock_client.invoke_model(
            modelId="anthropic.claude-v2",
            contentType="application/json",
            accept="application/json",
            body=json.dumps(payload)
        )

        result = response["body"].read().decode("utf-8")
        return json.loads(result).get("completion", "No response from model")
    
    except Exception as e:
        print(f"❌ Bedrock API Error: {e}")
        return "I'm sorry, but I encountered an error."

@app.post("/ask")
async def ask_question(payload: AskPayload):
    """ Handles file lookups and retrieval using FAISS. """
    try:
        start_time = time.time()
        embedder = LocalEmbedding()

        question = payload.question.lower()

        
        if "what are the files" in question:
            file_list = [{"file": item["file"], "url": item["github_url"]} for item in metadata]
            return JSONResponse({"files": file_list})

        if "what is the code in" in question:
            filename = question.replace("what is the code in", "").strip()
            matching_files = [item for item in metadata if filename in item["file"]]

            if matching_files:
                return JSONResponse({"file": matching_files[0]["file"], 
                                     "content": matching_files[0]["content"], 
                                     "url": matching_files[0]["github_url"]})
            else:
                return JSONResponse({"message": f"No matching file found for '{filename}'"})

       
        question_embedding = np.array([embedder.embed(payload.question)]).astype('float32')

       
        distances, indices = index.search(question_embedding, k=5)

        relevant_chunks = []
        for i, idx in enumerate(indices[0]):
            if idx == -1 or distances[0][i] > 1.0:
                continue
            relevant_chunks.append(metadata[idx])

        if not relevant_chunks:
            return JSONResponse({"answer": "No relevant information found."})

        context_str = "\n\n".join(
            [f"[File: {chunk['file']} - Chunk {chunk['chunk']}]({chunk['github_url']})\n{chunk['content']}" 
             for chunk in relevant_chunks]
        )
        user_prompt = f"Context:\n{context_str}\n\nQuestion: {payload.question}"

       
        answer_text = call_claude_2(user_prompt)

        return JSONResponse({"answer": answer_text, "references": relevant_chunks})

    except Exception as e:
        print(f"❌ API Error: {e}")
        return JSONResponse({"error": str(e)}, status_code=500)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=5500)
