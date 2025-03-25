# encoding: utf-8
#
# Lab F-6: Tool use
#
# https://catalog.workshops.aws/building-with-amazon-bedrock/en-US/foundation/tool-use

import boto3, json, math, sys


_tool_list = [{
    'toolSpec': {
        'name': 'cosine',
        'description': 'Calculate the cosine of x.',
        'inputSchema': {
            'json': {
                'type': 'object',
                'properties': {
                    'x': {
                        'type': 'number',
                        'description': 'The number to pass to the function.'
                    }
                },
                'required': ['x']
            }
        }
    }
}]

# Tool-capable Models
# -------------------
#
# The only tool-capable models we have access to are (as of 2025-03-25):
#
# - meta.llama3-1-405b-instruct-v1:0
# - meta.llama3-1-70b-instruct-v1:0
# - meta.llama3-1-8b-instruct-v1:0

_model_id = 'meta.llama3-1-405b-instruct-v1:0'


def try_model(bedrock):
    message_list = []
    initial_message = {
        'role': 'user',
        'content': [{'text': 'What is the cosine of 7?'}]
    }
    message_list.append(initial_message)
    response = bedrock.converse(
        modelId=_model_id,
        messages=message_list,
        inferenceConfig={'maxTokens': 2000, 'temperature': 0},
        toolConfig={'tools': _tool_list},
        system=[{'text': 'You must only do math by using a tool.'}]
    )
    response_message = response['output']['message']

    # Show the response which should include a `toolUse` block
    print(json.dumps(response_message, indent=4))
    message_list.append(response_message)

    # Now call a function based on `toolUse`
    response_content_blocks, follow_up_content_blocks = response_message['content'], []
    for content_block in response_content_blocks:
        if 'toolUse' in content_block:
            tool_use_block = content_block['toolUse']
            tool_use_name = tool_use_block['name']
            print(f'🔧 Using tool {tool_use_name}', file=sys.stderr)
            if tool_use_name == 'cosine':
                tool_result_value = math.cos(float(tool_use_block['input']['x']))
                print(f'Tool result: {tool_result_value}')
                follow_up_content_blocks.append({
                    'toolResult': {
                        'toolUseId': tool_use_block['toolUseId'],
                        'content': [{'json': {'result': tool_result_value}}]
                    }
                })
        elif 'text' in content_block:
            print(content_block['text'])
    if len(follow_up_content_blocks) > 0:
        follow_up_message = {'role': 'user', 'content': follow_up_content_blocks}
        message_list.append(follow_up_message)
        response = bedrock.converse(
            modelId=_model_id,
            messages=message_list,
            inferenceConfig={'maxTokens': 2000, 'temperature': 0},
            toolConfig={'tools': _tool_list},
            system=[{'text': 'You must only do math by using a tool.'}]
        )
        response_message = response['output']['message']
        print(json.dumps(response_message, indent=4))
        message_list.append(response_message)  # If we were to continue the conversation


def main():
    session = boto3.Session(profile_name='saml-pub')
    bedrock = session.client(service_name='bedrock-runtime')
    try_model(bedrock)


if __name__ == '__main__':
    main()
