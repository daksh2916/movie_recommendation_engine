from fastapi import HTTPException
import pinecone, os
from pinecone import Pinecone, ServerlessSpec

# Create a Pinecone client instance
pc = Pinecone(
    api_key="pcsk_2GAsiz_3bdcQBwRNcpEaAKddukkmKpNxsRrYUoakMNNQbrTcGCccnwHdudWrSb3Aj4S2hn",
)

# Index configuration
INDEX_NAME = "user-embeddings"
DIMENSION = 384  # adjust to your embedding dimension

# Check if index exists
if INDEX_NAME not in pc.list_indexes().names():
    pc.create_index(
        name=INDEX_NAME,
        dimension=DIMENSION,
        metric="cosine",
        spec=ServerlessSpec(
            cloud="aws",  # or gcp depending on your environment
            region=os.getenv("PINECONE_ENV")  # e.g., "aped-4627-b74a"
        )
    )

# Connect to the index
index = pc.Index(INDEX_NAME)

# Optional: Health check function
def vector_db_status():
    try:
        stats = index.describe_index_stats()
        return {
            "status": "connected",
            "dimension": stats["dimension"],
            "total_vectors": stats["total_vector_count"],
            "namespaces": list(stats["namespaces"].keys())
        }
    except Exception as e:
        return {"status": "error", "detail": str(e)}