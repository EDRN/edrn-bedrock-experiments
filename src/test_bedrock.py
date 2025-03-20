# encoding: utf-8

import json, boto3, sys
from pprint import pprint


def main():
    # Note: you must use the JPL `aws-login` executable first and establish the profile
    # named `saml-pub`.
    session = boto3.Session(profile_name='saml-pub')

    # Start a session with the service `bedrock`
    #
    # We'll use that to list all the foundation models
    bedrock = session.client(service_name='bedrock')
    print('🤖 Foundation Models (note: may not have permission to use most of these)')
    response = bedrock.list_foundation_models()
    names = [i['modelName'] for i in response['modelSummaries']]
    print(', '.join(names))

    # Start a session with the service named `bedrock-runtime`
    #
    # We'll use that to interact with a text generationm model `titan-text-express` to get
    # a definition of a cancer biomarker.
    bedrock_runtme = session.client(service_name='bedrock-runtime')
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
