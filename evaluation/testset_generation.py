from __future__ import annotations

from langchain_core.documents import Document
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from ragas.testset.evolutions import multi_context, reasoning, simple
from ragas.testset.generator import TestDataset, TestsetGenerator


generator_llm = ChatOpenAI(model=GENERATOR_MODEL)
critic_llm = ChatOpenAI(model=CRITIC_MODEL)
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")

def prepare_documents(documents: list[Document]) -> list[Document]:
    documents_prep = documents.copy()

    for document in documents_prep:
        document.metadata['filename'] = document.metadata['source']

    return documents_prep

def generate_testset(
    documents: list[Document],
    tests_per_doc: int = 3,
) -> TestDataset:
    test_size = tests_per_doc * len(documents)

    generator = TestsetGenerator.from_langchain(
        generator_llm,
        critic_llm,
        embeddings
    )

    return generator.generate_with_langchain_docs(
        documents,
        test_size=test_size,
        distributions={
            simple: 0.5,
            reasoning: 0.25,
            multi_context: 0.25,
        },
    )

def save_testset(testset: TestDataset) -> None:
    df = testset.to_pandas()
    df.to_json(
        "testset_gpt_weider.json",
        orient="records",
        lines=True,
    )
