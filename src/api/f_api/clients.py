from openai import OpenAI

from f_api.utils.embeddings import build_embeddings_model
from f_api.utils.search import build_search_store

openai = OpenAI()
embeddings = build_embeddings_model()
vector_store = build_search_store(embeddings)
