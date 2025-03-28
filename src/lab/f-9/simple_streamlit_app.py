# encoding: utf-8
#
# F-9: Streamlit
#
# https://catalog.workshops.aws/building-with-amazon-bedrock/en-US/foundation/streamlit-intro
#
# Run as:
#
#     bin/streamlit run src/lab/f-9/simple_streamlit_app.py --server.port 8080


import streamlit


def main():
    streamlit.set_page_config(page_title='Streamlit Demo')  # HTML title
    streamlit.title('Streamlit Demo')  # page title
    color_text = streamlit.text_input("What's your favorite color?")  # display a text box
    go_button = streamlit.button('Go', type='primary')  # display a primary button
    if go_button:  # code in this if block will be run when the button is clicked
        streamlit.write(f'I like {color_text} too!')  # display the response content


if __name__ == '__main__':
    main()
