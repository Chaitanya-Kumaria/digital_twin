import os
from pathlib import Path


class SimpleTextSearch:
    """Simple text search using TF-IDF style matching - no transformers needed."""

    def __init__(self, knowledge_base_path="knowledge_base"):
        self.knowledge_base_path = knowledge_base_path
        self.documents = []
        self._load_documents()

    def _load_documents(self):
        """Load all .txt files from the knowledge base directory."""
        kb_path = Path(self.knowledge_base_path)
        if not kb_path.exists():
            kb_path.mkdir(parents=True, exist_ok=True)
            return

        for txt_file in kb_path.glob("**/*.txt"):
            try:
                with open(txt_file, "r", encoding="utf-8") as f:
                    content = f.read().strip()
                if content:
                    # Split into chunks of ~500 chars
                    chunks = self._split_text(content, chunk_size=500, overlap=50)
                    for chunk in chunks:
                        self.documents.append({
                            "content": chunk,
                            "source": str(txt_file.name)
                        })
            except Exception as e:
                print(f"Error loading {txt_file}: {e}")

    def _split_text(self, text, chunk_size=500, overlap=50):
        """Split text into overlapping chunks."""
        if len(text) <= chunk_size:
            return [text]

        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk)
            start = end - overlap
        return chunks

    def search(self, query, k=3):
        """Search documents using simple keyword matching and scoring."""
        if not self.documents:
            return []

        query_words = set(query.lower().split())
        scored_docs = []

        for doc in self.documents:
            content_lower = doc["content"].lower()
            # Score based on how many query words appear in the document
            score = 0
            for word in query_words:
                if word in content_lower:
                    score += content_lower.count(word)

            if score > 0:
                scored_docs.append((score, doc))

        # Sort by score descending and return top k
        scored_docs.sort(key=lambda x: x[0], reverse=True)
        return [doc for _, doc in scored_docs[:k]]

    def get_context(self, query, k=3):
        """Get formatted context string from search results."""
        results = self.search(query, k)
        if not results:
            return ""
        return "\n\n".join([doc["content"] for doc in results])
