from langchain_core.prompts.chat import ChatPromptTemplate


def build_chatbot_prompt() -> ChatPromptTemplate:
    system_prompt = (
        "You are an assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer "
        "the question. If you don't know the answer, say that you "
        "don't know."
        "\n\n"
        "{context}"
    )

    return ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )
    # rag_prompt=PromptTemplate(
    #     input_variables=["context", "question"],
    #     template="""
    #         Answer the following question making use of the given context.
    #         If you don't know the answer, just say you don't know.
    #
    #         -----------------
    #         Context:
    #         {context}
    #     """
    # )
    #
    # prompt = rag_prompt
    # input_variables=["context", "question"]
    #
    # return ChatPromptTemplate(
    #     input_variables=input_variables,
    #     messages=[HumanMessagePromptTemplate(prompt=prompt)]
    # )
