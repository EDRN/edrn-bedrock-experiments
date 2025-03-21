# encoding: utf-8
#
# See https://catalog.us-east-1.prod.workshops.aws/event/dashboard/en-US/workshop/intermediate/bedrock-rag-chatbot

import streamlit as st
import rag_chatbot_lib as glib


def main():
    st.set_page_config(page_title='RAG Chatbot')
    st.title('RAG Chatbot')
    if 'chat_history' not in st.session_state:
        # Chat history hasn't yet been created so initialize it
        st.session_state.chat_history = []

    chat_container = st.container()
    input_text = st.chat_input('Chat with your bot here')
    if input_text:
        glib.chat_with_model(message_history=st.session_state.chat_history, new_text=input_text)

    # Re-render the chat history (Streamlit re-runs this script, so need this to preserve previous chat messages)
    for message in st.session_state.chat_history:
        with chat_container.chat_message(message.role):
            # Render a chat line for the given role, containing everything in the with block
            st.markdown(message.text)


if __name__ == '__main__':
    main()
