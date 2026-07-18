from app.services.vector_store.chroma_client import ChromaClient

db = ChromaClient()

results = db.collection.get()

print("=" * 60)
print("Total Documents:", len(results["documents"]))
print("=" * 60)

paper_ids = {}

for meta in results["metadatas"]:
    pid = meta["paper_id"]

    if pid not in paper_ids:
        paper_ids[pid] = meta["paper_name"]

print("Papers stored in Chroma:\n")

for pid, name in paper_ids.items():
    print(f"{name}")
    print(f"  {pid}\n")