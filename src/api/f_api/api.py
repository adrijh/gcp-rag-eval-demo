from fastapi import BackgroundTasks, FastAPI
from fastapi.responses import JSONResponse
from langchain_core.documents.base import Document
from langchain_google_community import GCSFileLoader
from pydantic import BaseModel

from f_api.clients import embeddings, vector_store
from f_api.utils.chat import chat_pipeline
from f_api.utils.documents import insert_document_to_vectorstore
from f_api.utils.ragas import build_documents_tests

app = FastAPI()

class DocRequest(BaseModel): # type: ignore
    bucket_name: str
    blob_name: str

class ChatRequest(BaseModel): # type: ignore
    prompt: str


@app.post("/doc") # type: ignore
async def ingest_document(request: DocRequest, background_tasks: BackgroundTasks) -> JSONResponse:
    documents = load_document_from_blob(
        bucket_name=request.bucket_name,
        blob_name=request.blob_name,
    )

    insert_document_to_vectorstore(
        vector_store=vector_store,
        embeddings=embeddings,
        documents=documents,
    )

    # background_tasks.add_task(build_documents_tests, documents=documents)

    return JSONResponse(status_code=200, content={"detail": "Success"})

@app.post("/chat") # type: ignore
async def chat(request: ChatRequest) -> JSONResponse:
    return chat_pipeline(
        vector_store=vector_store,
        prompt=request.prompt,
    )

def load_document_from_blob(bucket_name: str, blob_name: str) -> list[Document]:
    loader = GCSFileLoader(
        project_name="practicas-cloud-syntonize",
        bucket=bucket_name,
        blob=blob_name,
    )

    return loader.load()
