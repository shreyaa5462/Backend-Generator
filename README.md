
An AI-powered platform that converts Software Requirement Documents (SRDs) into FastAPI backend applications using LLMs.

Tech Stack
Python
FastAPI
LangChain
LangGraph
Groq LLM
RAG
ChromaDB
PostgreSQL
Docker
Features
SRD document upload
Requirement analysis
Backend blueprint generation
Model and schema generation
CRUD generation
Database layer generation
API generation
Main application generation
RAG-based contextual retrieval
Docker configuration generation
Workflow
SRD
 ↓
Requirement Analysis
 ↓
Blueprint
 ↓
Models
 ↓
Schemas
 ↓
CRUD
 ↓
Database
 ↓
APIs
 ↓
Main Application
 ↓
Generated Backend


Run Locally
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --port 8001

Open Swagger:

http://127.0.0.1:8001/docs
Docker
docker build -t ai-backend-generator .
docker run --env-file .env -p 8001:8001 ai-backend-generator
Author

Shreya Singh
