
"""
A simple in-memory vector store for demonstration.
We keep all vectors in a global list, then compute
cosine similarity (or dot product) at query time.
"""

import numpy as np

# We'll store everything in a module-level list so that multiple
# runs of the server won't require re-indexing unless you kill the process.
GLOBAL_VECTORS = []

class VectorStore:
    def upsert(self, embedding, metadata):
        """
        Insert the embedding + metadata into our global in-memory list.
        embedding is expected to be a list of floats.
        """
        GLOBAL_VECTORS.append((embedding, metadata))

    def query(self, embedding, top_k=5):
        """
        Query the global in-memory store for the most similar embeddings.
        We use cosine similarity to rank.
        Return a list of dicts: [{"score": float, "metadata": {...}}, ...]
        """
        if not GLOBAL_VECTORS:
            return []

        embedding_array = np.array(embedding)
        results = []
        for stored_embedding, meta in GLOBAL_VECTORS:
            stored_array = np.array(stored_embedding)
            # compute cosine similarity
            dot_product = np.dot(embedding_array, stored_array)
            norm_query = np.linalg.norm(embedding_array)
            norm_stored = np.linalg.norm(stored_array)
            if norm_query == 0 or norm_stored == 0:
                similarity = 0.0
            else:
                similarity = dot_product / (norm_query * norm_stored)

            results.append({"score": float(similarity), "metadata": meta})

        # sort by descending score
        results.sort(key=lambda x: x["score"], reverse=True)
        return results[:top_k]
