import requests
import streamlit as st

from f_app.config import CHAT_ENDPOINT


class SemanticSearchPage:
    def __init__(self) -> None:
        st.header("Chat with GPT with your own RAG")

        self.__init_message_history()
        self.__build_chatbot()


    def __init_message_history(self) -> None:
        if "messages" not in st.session_state:
            st.session_state["messages"] = []

    def __build_chatbot(self) -> None:

        for message in st.session_state["messages"]:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        if prompt := st.chat_input("Enter your question here.."):
            st.session_state["messages"].append({"role": "user", "content": prompt})

            with st.chat_message("user"):
                st.markdown(prompt)

            with st.chat_message("assistant"):
                response = requests.post(
                    CHAT_ENDPOINT,
                    json={"prompt": prompt},
                    timeout=30,
                ).json()

                st.session_state["messages"].append({"role": "assistant", "content": response["message"]})
                st.write(response["message"])

if __name__ == "__main__":
    SemanticSearchPage()
