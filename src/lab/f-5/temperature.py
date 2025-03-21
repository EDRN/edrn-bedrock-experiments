# encoding: utf-8
#
# https://catalog.us-east-1.prod.workshops.aws/event/dashboard/en-US/workshop/foundation/bedrock-temperature
#
# Example:
#
#     bin/python src/lab/f-5/temperature.py 0.2 Create a haiku about an arduous journey

import boto3, argparse

_model = 'amazon.titan-text-express-v1'


def get_text_response(input_content, temperature):
    session = boto3.Session(profile_name='saml-pub')
    bedrock = session.client(service_name='bedrock-runtime')
    
    message = {
        'role': 'user',
        'content': [{'text': input_content}]
    }
    response = bedrock.converse(
        modelId=_model,
        messages=[message],
        inferenceConfig={
            'maxTokens': 2000,
            'temperature': temperature,
            'topP': 0.9,
            'stopSequences': []
        },
    )
    return response['output']['message']['content'][0]['text']


def main():
    parser = argparse.ArgumentParser(description='Lab F-5: Controlling response variability')
    parser.add_argument('temperature', type=float, help='Temperature')
    parser.add_argument('input', nargs='+', help='Inputs to the model')
    args = parser.parse_args()
    print(get_text_response(' '.join(args.input), args.temperature))


if __name__ == '__main__':
    main()
