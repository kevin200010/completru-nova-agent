Set up ChromaDB as a local vector DB using Python + FastAPI.

Ingest documents (PDF, DOCX, etc.) and embed them using a model like all-MiniLM-L6-v2.

Expose an API endpoint (e.g., /rag/query) that performs similarity search + context return.

Modify the Nova Sonic app to:

Detect toolUse with KnowledgeBaseToolSchema

Call the RAG FastAPI /query

Return the result as toolResult

🧱 PART 1: Set up RAG server with ChromaDB
🔧 1.1 Install ChromaDB & FastAPI on EC2
SSH into your EC2 instance and create a new Python virtual environment:

sudo apt update
sudo apt install python3-venv
python3 -m venv chroma_env
source chroma_env/bin/activate

Install required packages:
pip install chromadb fastapi uvicorn sentence-transformers python-multipart

📦 1.2 Create rag_server.py
🚀 1.3 Run the RAG server
uvicorn rag_server:app --host 0.0.0.0 --port 8001
Add this to a tmux session or use nohup to run it in background:


nohup uvicorn rag_server:app --host 0.0.0.0 --port 8001 &


You now have:
POST /rag/query to ask questions
POST /rag/upload to upload plain-text files

