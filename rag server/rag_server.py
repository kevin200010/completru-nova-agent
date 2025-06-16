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

    documents = results.get("documents", [[]])[0]  # Extract list of top docs
    if not documents:
        return {"result": "No relevant content found."}

    # Join top results into a single plain string
    response_text = "\n\n".join(documents)
    return {"result": response_text}


@app.post("/rag/upload")
async def upload_doc(file: UploadFile = File(...)):
    content = (await file.read()).decode("utf-8")
    chunks = content.split(". ")
    embeddings = embedder.encode(chunks).tolist()
    ids = [f"chunk-{i}" for i in range(len(chunks))]
    collection.add(documents=chunks, embeddings=embeddings, ids=ids)
    return {"status": "Uploaded"}