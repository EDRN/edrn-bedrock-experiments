# encoding: utf-8
#
# Lab F-3: Converse API
#
# See https://catalog.us-east-1.prod.workshops.aws/event/dashboard/en-US/workshop/foundation/converse-api


import json, boto3


def main():
    session = boto3.Session(profile_name='saml-pub')
    bedrock = session.client(service_name='bedrock-runtime')

    message_list = []
    initial_message = {'role': 'user', 'content': [{'text': 'How are you today?'}]}
    message_list.append(initial_message)

    response = bedrock.converse(
        modelId='amazon.titan-tg1-large',
        messages=message_list,
        inferenceConfig={'maxTokens': 2000, 'temperature': 0}
    )    
    response_message = response['output']['message']
    print(json.dumps(response_message, indent=4))


if __name__ == '__main__':
    main()
