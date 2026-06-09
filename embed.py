from ingest import load_and_chunk
import chromadb
from sentence_transformers import SentenceTransformer

# Load your chunks from the ingestion pipeline
chunks = load_and_chunk("documents/CleveReviews.txt")

# Load the embedding model (downloads once, cached after)
model = SentenceTransformer("all-MiniLM-L6-v2")

# Set up ChromaDB — stores everything locally in a folder called "chroma_db"
client = chromadb.PersistentClient(path="chroma_db")
collection = client.get_or_create_collection(name="dining_reviews")

# Embed each chunk and add to ChromaDB
texts = [chunk["text"] for chunk in chunks]
sources = [chunk["source"] for chunk in chunks]
ids = [f"chunk_{i}" for i in range(len(chunks))]
embeddings = model.encode(texts).tolist()

collection.add(
    documents=texts,
    embeddings=embeddings,
    metadatas=[{"source": s} for s in sources],
    ids=ids
)

print(f"Stored {len(chunks)} chunks in ChromaDB")

# Retrieval function
def retrieve(query, k=4):
    query_embedding = model.encode([query]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=k
    )
    chunks_out = []
    for text, metadata, distance in zip(
        results["documents"][0],
        results["metadatas"][0],
        results["distances"][0]
    ):
        chunks_out.append({
            "text": text,
            "source": metadata["source"],
            "distance": round(distance, 3)
        })
    return chunks_out

# Test retrieval with 3 sample queries
if __name__ == "__main__":
    test_queries = [
        "What do students say about vegetarian options?",
        "How is the atmosphere and environment?",
        "Are the prices good for the amount of food you get?"
    ]

    for query in test_queries:
        print(f"\nQuery: {query}")
        print("-" * 50)
        results = retrieve(query)
        for r in results:
            print(f"Distance: {r['distance']}")
            print(r['text'][:200])
            print()