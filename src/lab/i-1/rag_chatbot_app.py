# encoding: utf-8
#
# See https://catalog.us-east-1.prod.workshops.aws/event/dashboard/en-US/workshop/intermediate/bedrock-rag-chatbot

import streamlit
import rag_chatbot_lib


def main():
    streamlit.set_page_config(page_title='RAG Chatbot')
    streamlit.title('RAG Chatbot')
    if 'chat_history' not in streamlit.session_state:
        # Chat history hasn't yet been created so initialize it
        streamlit.session_state.chat_history = []

    chat_container = streamlit.container()
    input_text = streamlit.chat_input('Chat with your bot here')
    if input_text:
        rag_chatbot_lib.chat_with_model(message_history=streamlit.session_state.chat_history, new_text=input_text)

    # Re-render the chat history (Streamlit re-runs this script, so need this to preserve previous chat messages)
    for message in streamlit.session_state.chat_history:
        with chat_container.chat_message(message.role):
            # Render a chat line for the given role, containing everything in the with block
            streamlit.markdown(message.text)


if __name__ == '__main__':
    main()
