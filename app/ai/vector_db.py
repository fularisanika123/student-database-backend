"""Optional ChromaDB semantic-retrieval component.

SQLite remains the source of truth for structured student CRUD. ChromaDB is selected
for a separate semantic-search use case, matching the internship instruction that a
vector database should be used when appropriate to the chosen architecture.
"""
from pathlib import Path

CHROMA_PATH = Path("./chroma_data")


def get_collection():
    import chromadb

    client = chromadb.PersistentClient(path=str(CHROMA_PATH))
    return client.get_or_create_collection(name="student_profiles")


def index_student(student_id: int, document: str, metadata: dict | None = None):
    collection = get_collection()
    collection.upsert(
        ids=[str(student_id)],
        documents=[document],
        metadatas=[metadata or {}],
    )
    return True


def semantic_search(query: str, n_results: int = 3):
    collection = get_collection()
    if collection.count() == 0:
        return []
    return collection.query(query_texts=[query], n_results=n_results)
