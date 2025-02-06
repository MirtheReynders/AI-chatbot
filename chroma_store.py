import chromadb
from sentence_transformers import SentenceTransformer

# Initialiseer ChromaDB
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection("character_data")

# Laad embeddings model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def add_to_chroma(title, chunks):
    """Voegt gescrapete data (karakterinfo of schrijfstijl) toe aan ChromaDB."""
    for i, chunk in enumerate(chunks):
        vector = embedding_model.encode(chunk).tolist()
        doc_id = f"{title}_{i}"
        collection.add(ids=[doc_id], embeddings=[vector], documents=[chunk])

def search_chroma(query, top_k=3):
    """Zoekt relevante stukken tekst in ChromaDB en geeft een lijst van strings terug."""
    query_vector = embedding_model.encode(query).tolist()
    results = collection.query(query_embeddings=[query_vector], n_results=top_k)

    # Fix: Flatten de resultaten zodat we een lijst met strings krijgen
    documents = results["documents"] if "documents" in results else []

    # Sommige implementaties geven een lijst van lijsten terug -> Flatten
    flattened_docs = [doc if isinstance(doc, str) else " ".join(doc) for doc in documents]

    return flattened_docs  # Zorgt ervoor dat de chatbot een correcte string kan maken
