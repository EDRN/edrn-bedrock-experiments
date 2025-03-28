# encoding: utf-8
#
# F-8: Embeddings
#
# https://catalog.workshops.aws/building-with-amazon-bedrock/en-US/foundation/bedrock-embedding

import json, boto3
from numpy import dot
from numpy.linalg import norm

_items = [
    'Felines, canines, and rodents',
    'Can you please tell me how to get to the bakery?',
    'Lions, tigers, and bears',
    'Chats, chiens et souris',
    '猫、犬、ネズミ',
    "Pouvez-vous s'il vous plaît me dire comment me rendre à la boulangerie?",
    'Kannst du mir bitte sagen, wie ich zur Bäckerei komme?',
    'パン屋への行き方を教えてください',
    'パン屋への道順を知りたい',
    'Can you please tell me how to get to the stadium?',
    'I need directions to the bread shop',
    'Cats, dogs, and mice',
]


class EmbedItem:
    def __init__(self, text):
        self.text = text
        self.embedding = get_embedding(text)


class ComparisonResult:
    def __init__(self, text, similarity):
        self.text = text
        self.similarity = similarity


def get_embedding(text):
    session = boto3.Session(profile_name='saml-pub')
    bedrock = session.client(service_name='bedrock-runtime')
    
    response = bedrock.invoke_model(
        body=json.dumps({'inputText': text}), 
        modelId='amazon.titan-embed-text-v2:0', 
        accept='application/json',
        contentType='application/json'
    )
    
    response_body = json.loads(response['body'].read())
    return response_body['embedding']


def calculate_similarity(a, b):
    '''See Cosine Similarity: https://en.wikipedia.org/wiki/Cosine_similarity'''
    return dot(a, b) / (norm(a) * norm(b))


def main():
    items = []
    for i in _items:
        items.append(EmbedItem(i))
    for e1 in items:
        print(f'Closest matches for «{e1.text}»')
        print('——————')
        cosine_comparisons = []
        for e2 in items:
            similarity_score = calculate_similarity(e1.embedding, e2.embedding)
            cosine_comparisons.append(ComparisonResult(e2.text, similarity_score))
        cosine_comparisons.sort(key=lambda x: x.similarity, reverse=True)
        for c in cosine_comparisons:
            print(f'{c.similarity:.6f}\t{c.text}')
        print()


if __name__ == '__main__':
    main()
