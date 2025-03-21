# encoding: utf-8
#
# Lab F-2: InvokeModel API
#
# See https://catalog.us-east-1.prod.workshops.aws/event/dashboard/en-US/workshop/foundation/bedrock-apis


import json, boto3


def main():
    session = boto3.Session(profile_name='saml-pub')
    bedrock = session.client(service_name='bedrock-runtime')
    bedrock_model_id = 'amazon.titan-text-express-v1'
    prompt = "What's the largest city in New Hampshire?"
    body = json.dumps({
        'inputText': prompt,
        'textGenerationConfig': {
            'temperature': 0,
            'topP': 0.5,
            'maxTokenCount': 1024,
            'stopSequences': []
        }
    })
    response = bedrock.invoke_model(
        body=body, modelId=bedrock_model_id, accept='application/json', contentType='application/json'
    )
    response_body = json.loads(response.get('body').read())
    response_text = response_body['results'][0]['outputText']
    print(response_text)  # Manchester, allegedly


if __name__ == '__main__':
    main()
