
from sentence_transformers import SentenceTransformer

class LocalEmbedding:
    """
    Wraps a SentenceTransformer to embed text locally.
    """
    def __init__(self):
        # Model can be changed to "all-MiniLM-L6-v2" or another from huggingface
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def embed(self, text: str):
        """
        Returns a list of floats representing the text embedding.
        """
        # sentence-transformers returns a NumPy array
        embedding = self.model.encode(text)
        return embedding.tolist()


class LocalLLM:

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        # In practice, you'd do something like:
        # response = openai.Completion.create(
        #   prompt = system_prompt + "\n\n" + user_prompt,
        #   ...
        # )
        # return response["choices"][0]["text"]
        #
        # For demonstration, let's just return a pretend answer:
        return (
            "Here's a stub answer. (Replace with a real LLM call.)\n\n"
            f"System Prompt was: {system_prompt}\n\nUser Prompt was: {user_prompt}"
        )
