# encoding: utf-8
#
# https://catalog.workshops.aws/building-with-amazon-bedrock/en-US/foundation/bedrock-inference-parameters
#
# Example:
#
#     bin/python src/lab/f-4/params.py amazon.titan-text-express-v1 Write a charming limerick

import boto3, argparse


def get_text_response(model, input_content):
    session = boto3.Session(profile_name='saml-pub')
    bedrock = session.client(service_name='bedrock-runtime')
    
    message = {
        'role': 'user',
        'content': [{'text': input_content}]
    }
    response = bedrock.converse(
        modelId=model,
        messages=[message],
        inferenceConfig={
            'maxTokens': 2000,
            'temperature': 0,
            'topP': 0.9,
            'stopSequences': []
        },
    )
    return response['output']['message']['content'][0]['text']


def main():
    parser = argparse.ArgumentParser(description='Lab F-4: Inference Parameters')
    parser.add_argument('model', help='Model ID')
    parser.add_argument('input', nargs='+', help='Inputs to the model')
    args = parser.parse_args()
    print(get_text_response(args.model, ' '.join(args.input)))


if __name__ == '__main__':
    main()
