# encoding: utf-8
#
# B-1: Text generation
#
# https://catalog.workshops.aws/building-with-amazon-bedrock/en-US/basic/bedrock-text
#
# Run as:
#
#     bin/streamlit run src/lab/b-1/text_lib.py --server.port 8080


import boto3, streamlit


def get_text_response(input_content):
    session = boto3.Session(profile_name='saml-pub')
    bedrock = session.client(service_name='bedrock-runtime')
    message = {
        'role': 'user',
        'content': [{'text': input_content}]
    }
    response = bedrock.converse(
        modelId='amazon.titan-tg1-large',
        messages=[message],
        inferenceConfig={
            'maxTokens': 2000,
            'temperature': 0,
            'topP': 0.9,
            'stopSequences': []
        }
    )
    return response['output']['message']['content'][0]['text']


def main():
    streamlit.set_page_config(page_title='Text to Text')
    streamlit.title('Text to Text')
    input_text = streamlit.text_area('Input text', label_visibility='collapsed')
    go_button = streamlit.button('Go', type='primary')
    if go_button:
        with streamlit.spinner('Working…'):
            response_content = get_text_response(input_text)
            streamlit.write(response_content)


if __name__ == '__main__':
    main()
