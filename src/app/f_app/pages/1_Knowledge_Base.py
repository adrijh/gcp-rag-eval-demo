import requests
import streamlit as st
from google.cloud import storage
from langchain_core.documents import Document
from streamlit.runtime.uploaded_file_manager import UploadedFile

from f_app import config as cfg


def transform_files_to_documents(
    uploaded_files: list[UploadedFile],
) -> list[Document]:
    documents = []
    for uploaded_file in uploaded_files:
        content = uploaded_file.read().decode("utf-8")
        doc = Document(page_content=content, metadata={"filename": uploaded_file.name})
        documents.append(doc)

    return documents



def upload_document_blob(file: UploadedFile) -> tuple[str, str]:
    storage_client = storage.Client()
    dest_blob_name = f"docs/{file.name}"

    bucket = storage_client.bucket(cfg.GCP_BUCKET_NAME)

    blob = bucket.blob(dest_blob_name)

    blob.upload_from_file(file)

    return cfg.GCP_BUCKET_NAME, dest_blob_name

class KnowledgeBasePage:
    def __init__(self) -> None:
        # st.header("RAG Parameters")
        # self.chunk_size = st.slider("Chunk Size", min_value=500, max_value=2000, value=1000)
        # self.chunk_overlap = st.slider("Chunk Overlap", min_value=0, max_value=100, value=25)

        st.header("Upload Files")

        upload_files = st.file_uploader(
            label="text_file_uploader",
            type=("txt", "md", "pdf"),
            accept_multiple_files=True,
            label_visibility="collapsed",
        )

        if st.button("Load", type="primary", use_container_width=True):
            result = ""
            if not upload_files:
                st.error("No files were included for upload.")
            else:
                self.__load_button_impl(upload_files)

            st.text_area(
                label="Retrieved document",
                value=result,
                height=640,
                key="transcription",
            )

    def __load_button_impl(self, upload_files: list[UploadedFile]) -> None:
        for file in upload_files:
            bucket_name, blob_name = upload_document_blob(file)
            requests.post(
                url=cfg.DOC_ENDPOINT,
                json={
                    "bucket_name": bucket_name,
                    "blob_name": blob_name
                },
                timeout=30,
            )


if __name__ == "__main__":
    KnowledgeBasePage()
