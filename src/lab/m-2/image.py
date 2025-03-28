# encoding: utf-8
#
# B-2: Image generation
#
# https://catalog.workshops.aws/building-with-amazon-bedrock/en-US/basic/bedrock-image
#
# Run as:
#
#     bin/streamlit run src/lab/m-2/image.py --server.port 8080


from io import BytesIO
from random import randint
import boto3, json, base64, streamlit


def get_titan_response_image(response):
    response = json.loads(response.get('body').read())
    images = response.get('images')
    image_data = base64.b64decode(images[0])
    return BytesIO(image_data)


def get_titan_image_generation_request_body(prompt, negative_prompt=None):
    body = {
        'taskType': 'TEXT_IMAGE',
        'textToImageParams': {'text': prompt},
        'imageGenerationConfig': {
            'numberOfImages': 1,
            'quality': 'premium',
            'height': 512,
            'width': 512,
            'cfgScale': 8.0,
            'seed': randint(0, 100000)
        }
    }
    if negative_prompt:
        body['textToImageParams']['negativeText'] = negative_prompt
    return json.dumps(body)


def get_image_from_model(prompt_content, negative_prompt=None):
    session = boto3.Session(profile_name='saml-pub')
    bedrock = session.client(service_name='bedrock-runtime')
    body = get_titan_image_generation_request_body(prompt_content, negative_prompt=negative_prompt)
    response = bedrock.invoke_model(
        body=body, modelId='amazon.titan-image-generator-v2:0',
        contentType='application/json', accept='application/json'
    )
    output = get_titan_response_image(response)
    return output


def main():
    streamlit.set_page_config(layout='wide', page_title='Image Generation')
    streamlit.title('Image Generation')
    col1, col2 = streamlit.columns(2)
    with col1:
        streamlit.subheader('Image parameters')
        prompt_text = streamlit.text_area('What you want to see in the image:', height=100, help='The prompt text')
        negative_prompt = streamlit.text_input('What should not be in the image:', help='The negative prompt')
        generate_button = streamlit.button('Generate', type='primary')
    with col2:
        streamlit.subheader('Result')
        if generate_button:
            with streamlit.spinner('Drawing…'):
                generated_image = get_image_from_model(prompt_text, negative_prompt)
                streamlit.image(generated_image)


if __name__ == '__main__':
    main()
