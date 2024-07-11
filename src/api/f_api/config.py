import os

GOOGLE_APPLICATION_CREDENTIALS="/Users/adrian/.config/gcloud/tf-deploy-key.json"
GCP_PROJECT_ID = os.environ["GCP_PROJECT_ID"]
GCP_REGION = os.environ["GCP_REGION"]
GCP_BUCKET_NAME = os.environ["GCP_BUCKET_NAME"]
GCP_INDEX_ID = os.environ["GCP_INDEX_ID"]
GCP_INDEX_ENDPOINT_ID = os.environ["GCP_INDEX_ENDPOINT_ID"]

EMBEDDING_MODEL = "text-embedding-ada-002"
RERANKING_MODEL = "gpt-3.5-turbo-0125"
QUERY_EXPANSION_MODEL = "gpt-3.5-turbo-0125"
CHAT_MODEL = "gpt-3.5-turbo-0125"

OPENAI_API_KEY = os.environ["OPENAI_API_KEY"]
HUGGINGFACE_TOKEN = os.environ["HUGGINGFACE_TOKEN"]
COHERE_API_KEY = os.environ["COHERE_API_KEY"]

RAGAS_GENERATOR_MODEL = "gpt-3.5-turbo-0125"
RAGAS_CRITIC_MODEL = "gpt-3.5-turbo-0125"
RAGAS_EMBEDDINGS_MODEL = "text-embedding-3-small"
