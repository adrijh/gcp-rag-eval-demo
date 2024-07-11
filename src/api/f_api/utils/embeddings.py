from langchain.retrievers import ContextualCompressionRetriever
from langchain.retrievers.document_compressors import CohereRerank
from langchain.retrievers.multi_query import LineListOutputParser, MultiQueryRetriever
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableSerializable, Runnable
from langchain_core.vectorstores import VectorStore
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain.chains.retrieval import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain

from f_api import config as cfg
from f_api.utils.prompts import build_chatbot_prompt


# def build_rag_chain(vector_store: VectorStore) -> RunnableSerializable:
#     def format_docs(docs: list[Document]) -> str:
#         return "\n".join([doc.page_content for doc in docs])
#
#     llm = ChatOpenAI(model=cfg.CHAT_MODEL)
#     retriever = build_retriever(vector_store=vector_store)
#
#     prompt = build_chatbot_prompt()
#
#     return (
#         {"context": retriever | format_docs, "input": RunnablePassthrough()}
#         | prompt
#         | llm
#         | StrOutputParser()
#     )

def build_rag_chain(vector_store: VectorStore) -> Runnable:
    llm = ChatOpenAI(model=cfg.CHAT_MODEL)
    retriever = build_retriever(vector_store=vector_store)
    prompt = build_chatbot_prompt()

    qa_chain = create_stuff_documents_chain(llm, prompt)
    return create_retrieval_chain(retriever, qa_chain)

def build_embeddings_model() -> Embeddings:
    return OpenAIEmbeddings(
        model=cfg.EMBEDDING_MODEL,
    )

def build_reranking_retriever(
    base_retriever: MultiQueryRetriever,
) -> ContextualCompressionRetriever:
    compressor = CohereRerank()
    return ContextualCompressionRetriever(
        base_compressor=compressor,
        base_retriever=base_retriever,
    )

def build_retriever(vector_store: VectorStore) -> ContextualCompressionRetriever:
    llm_aug = ChatOpenAI(model=cfg.QUERY_EXPANSION_MODEL, temperature=0)
    prompt = get_query_expansion_prompt()
    llm_chain = prompt | llm_aug | LineListOutputParser()

    aug_retriever = MultiQueryRetriever(
        retriever=vector_store.as_retriever(),
        llm_chain=llm_chain, # type: ignore
        parser_key="lines",
    )

    return build_reranking_retriever(aug_retriever)


def get_query_expansion_prompt() -> PromptTemplate:
    return PromptTemplate.from_template(
        """You are an expert at converting user questions into database queries. \
        Perform query expansion. If there are multiple common ways of phrasing a user question \
        or common synonyms for key words in the question, make sure to return multiple versions \
        of the query with the different phrasings.

        If there are acronyms or words you are not familiar with, do not try to rephrase them.

        Return at least 3 versions of the question. Provide these alternative questions \
        separated by newlines.

        Original question: {question}
        """
    )
