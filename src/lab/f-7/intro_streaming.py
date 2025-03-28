# encoding: utf-8
#
# F-7: Streaming API
#
# https://catalog.workshops.aws/building-with-amazon-bedrock/en-US/foundation/streaming-intro
#
# To run:
#
#     bin/python3 src/lab/f-7/intro_streaming.py Tell me a story about two puppies and two kittens who became best friends

import boto3, argparse


def chunk_handler(chunk):
    '''Callback function when a chunk arrives.'''
    print(chunk, end='')


def get_streaming_response(prompt, streaming_callback):
    session = boto3.Session(profile_name='saml-pub')
    bedrock = session.client(service_name='bedrock-runtime')
    message = {
        'role': 'user',
        'content': [{'text': prompt}]
    }
    
    response = bedrock.converse_stream(
        modelId='meta.llama3-70b-instruct-v1:0',
        messages=[message],
        inferenceConfig={
            'maxTokens': 2000,
            'temperature': 0.0
        }
    )
    
    stream = response.get('stream')
    for event in stream:
        if 'contentBlockDelta' in event:
            streaming_callback(event['contentBlockDelta']['delta']['text'])


def main():
    parser = argparse.ArgumentParser(description='Lab F-7: Streaming API')
    parser.add_argument('prompt', nargs='+', help='What prompt to give to the model')
    args = parser.parse_args()
    get_streaming_response(' '.join(args.prompt), chunk_handler)
    print('\n')


if __name__ == '__main__':
    main()
