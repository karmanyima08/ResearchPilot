from app.services.vector_store.chroma_client import ChromaClient

db = ChromaClient()

results = db.collection.get(
    where={
        "paper_id": "e4fc4916-9fc8-4dbb-a067-9d31009e1fa6"
    }
)

print("Found:", len(results["documents"]))