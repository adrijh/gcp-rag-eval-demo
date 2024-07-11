import os

from dotenv import load_dotenv

PROJECT_PATH = os.path.join(os.path.dirname(__file__), "..")
ENV_PATH = os.path.join(PROJECT_PATH, "local", ".env")

load_dotenv(ENV_PATH)

from langsmith import unit
from f_api.clients import vector_store
from f_api.utils.embeddings import build_rag_chain


@unit
def test_answer_not_null():
    rag_chain = build_rag_chain(vector_store)
    response = rag_chain.invoke({"input": "How does RAG evaluation work?"})
    assert response["answer"] is not None
