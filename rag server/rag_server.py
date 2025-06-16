from fastapi import FastAPI, UploadFile, File
from pydantic import BaseModel
from sentence_transformers import SentenceTransformer
from chromadb import PersistentClient

app = FastAPI()
chroma_client = PersistentClient(path="./chroma_store")
collection = chroma_client.get_or_create_collection(name="rag-docs")
embedder = SentenceTransformer('all-MiniLM-L6-v2')

class Query(BaseModel):
    query: str

@app.post("/rag/query")
def rag_query(payload: Query):
    query_embedding = embedder.encode([payload.query])[0].tolist()
    results = collection.query(query_embeddings=[query_embedding], n_results=3)

    top_docs = results.get("documents", [[]])[0]  # Safely handle missing
    if not top_docs:
        return {"result": "No relevant information found."}

    # Combine all text chunks into one readable string
    response_text = "\n\n".join(doc.strip() for doc in top_docs)
    return {"result": response_text}

@app.post("/rag/upload")
async def upload_doc(file: UploadFile = File(...)):
    content = (await file.read()).decode("utf-8")
    chunks = content.split(". ")
    embeddings = embedder.encode(chunks).tolist()
    ids = [f"chunk-{i}" for i in range(len(chunks))]
    collection.add(documents=chunks, embeddings=embeddings, ids=ids)
    return {"status": "Uploaded"}