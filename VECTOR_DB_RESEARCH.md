# Vector Database Research and Selection

## Requirement
The internship instructions require research into suitable vector databases and
selection of an option that fits the project's chatbot/retrieval architecture.

## Options considered

### ChromaDB
- Python-friendly and easy to integrate.
- Supports persistent local storage.
- Supports similarity/semantic retrieval.
- Suitable for a small student project.

### FAISS
- Fast vector similarity search library.
- Excellent for local experimentation.
- More of a library for similarity search than a complete database service.

### Pinecone
- Managed cloud vector database.
- Useful for scalable production retrieval systems.
- Adds external-service setup compared with a local student project.

## Selected option: ChromaDB

ChromaDB is selected as an optional semantic-retrieval layer. SQLite remains the
source of truth for structured student CRUD because SQL is appropriate for exact
records such as ID, branch, year, email and other fields.

The project keeps ChromaDB isolated in `app/ai/vector_db.py`. This avoids forcing
vector search into ordinary CRUD operations while leaving a clear integration point
for future semantic/RAG retrieval.

## Selection factors
- Ease of integration
- Similarity search support
- Development complexity
- Local development convenience
- Ability to persist vector data
- Compatibility with the chatbot/retrieval architecture
