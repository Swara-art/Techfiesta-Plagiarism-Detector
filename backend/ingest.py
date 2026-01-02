from sentence_transformers import SentenceTransformer
from app.db.chroma_collections import get_collection

# Load embedding model
model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

# Get Chroma collection
collection = get_collection("student_text")

# Test sentences
sentences = [
    "Artificial intelligence is transforming education.",
    "Machine learning models require large datasets."
]

# Create embeddings
embeddings = model.encode(sentences).tolist()

# Insert into Chroma
collection.add(
    documents=sentences,
    embeddings=embeddings,
    metadatas=[
        {"source": "seed_data", "assignment_id": "TEST"},
        {"source": "seed_data", "assignment_id": "TEST"}
    ],
    ids=["seed-1", "seed-2"]
)

print("✅ Seed data inserted into Chroma")
