from langchain_core.embeddings import Embeddings
from langchain_core.vectorstores import VectorStore
from langchain_google_vertexai import (
    VectorSearchVectorStore,
)

from f_api import config as cfg


def build_search_store(embeddings: Embeddings) -> VectorStore:
    return VectorSearchVectorStore.from_components(
        project_id=cfg.GCP_PROJECT_ID,
        region=cfg.GCP_REGION,
        gcs_bucket_name=cfg.GCP_BUCKET_NAME,
        index_id=cfg.GCP_INDEX_ID,
        endpoint_id=cfg.GCP_INDEX_ENDPOINT_ID,
        embedding=embeddings,
        stream_update=True,
    )
