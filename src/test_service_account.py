# encoding: utf-8
#
# Generic Bedrock test for JPL — based on a service account with access and secret keys

import json, boto3, sys, os


def main():
    acc, sec = os.getenv('AWS_ACCESS_KEY_ID'), os.getenv('AWS_SECRET_ACCESS_KEY')
    if acc is None or sec is None:
        print('Please set both the AWS_ACCESS_KEY_ID and AWS_SECRET_ACCESS_KEY environment variables', file=sys.stderr)
        sys.exit(-1)
    region = os.getenv('AWS_DEFAULT_REGION', 'us-west-2')  # Most of JPL and EDRN use this region by default

    # First, see what foundation models are available
    bedrock = boto3.client('bedrock', aws_access_key_id=acc, aws_secret_access_key=sec, region_name=region)
    print('🤖 Foundation Models (note: may not have permission to use most of these)')
    response = bedrock.list_foundation_models()
    models = [(i['modelName'], i['modelId']) for i in response['modelSummaries']]
    for model in models:
        print(f'{model[0]} (ID: {model[1]})')

    # Next, use the Titan Text Express model to ask a simple question
    bedrock_runtme = boto3.client('bedrock-runtime', aws_access_key_id=acc, aws_secret_access_key=sec, region_name=region)
    print()
    print('🧬 What is a cancer biomarker?')
    bedrock_model_id = 'amazon.titan-text-express-v1'
    prompt = 'What is a cancer biomarker?'
    body = json.dumps({
        'inputText': prompt,
        'textGenerationConfig': {
            'temperature': 0,  
            'topP': 0.5,
            'maxTokenCount': 1024,
            'stopSequences': []
        }
    })
    response = bedrock_runtme.invoke_model(
        body=body, modelId=bedrock_model_id, accept='application/json', contentType='application/json'
    )
    response_body = json.loads(response.get('body').read())
    response_text = response_body['results'][0]['outputText']  # extract the text from the JSON response
    print(response_text)
    sys.exit(0)


if __name__ == '__main__':
    main()
