# AWS Bedrock

Notes. TBD. More to come.


## AWS Login for JPL Users

First visit the [AWS CLI and BOTO with JPL Credentials](https://wiki.jpl.nasa.gov/x/a4XyGQ) page and download the JPL AWS CLI helper for your platform.

For example, for macOS, download the file `aws-login.darwin.amd64`, rename it to simply `aws-login`, and make it executable; then log in:

    aws-login --pub --region us-west-2 --profile saml-pub --username USERNAME

You'll be prompted for your JPL password as well as your RSA PIN and token code. Then choose the role `am-edrn-dev` from the menu. In the future, you can then do

    aws-login --pub --region us-west-2 --profile saml-pub --username USERNAME --last_role

to skip the menu.

👉 **Note:** The login afforded by the above command has a limited lifetime. If you ever get 

    botocore.exceptions.ClientError: An error occurred (ExpiredTokenException) when calling the ListFoundationModels operation: The security token included in the request is expired

simply re-run the `aws-login` commmand as shown above.


## Bedrock Lab

Following instructions at https://catalog.us-east-1.prod.workshops.aws/event/dashboard/en-US/workshop/prerequisites/lab-setup, the following is a variation of these steps:

```console
$ mkdir environment
$ cd environment
$ curl 'https://static.us-east-1.prod.workshops.aws/5dd5dc48-363d-4c69-9007-9e5528c5c31f/assets/workshop.zip?Key-Pair-Id=K36Q2WVO3JP7QD&Policy=eyJTdGF0ZW1lbnQiOlt7IlJlc291cmNlIjoiaHR0cHM6Ly9zdGF0aWMudXMtZWFzdC0xLnByb2Qud29ya3Nob3BzLmF3cy81ZGQ1ZGM0OC0zNjNkLTRjNjktOTAwNy05ZTU1MjhjNWMzMWYvKiIsIkNvbmRpdGlvbiI6eyJEYXRlTGVzc1RoYW4iOnsiQVdTOkVwb2NoVGltZSI6MTc0MzA4MDYzN319fV19&Signature=CnywullBOTkmlqhJbNSqqPjv~jKSeIHw27if2BeBKRujEmNUegPuUixGYMZ~11EYvARfUMIK6R6ZBQyLcsEj75jWa9y2eAzUV6VOX2gHpJ-tTxehHZZvoobqA5tBuY9ow~jN21BWHttHjcJUuyrXZ631yfM3VC4UD8Z72mlrqEv7q2Tc3jIj0XAeSpgjdcw0sb8SqSwyUeX3ZUkAM2c3~TIFVGII4C-CKoxMU9x--PgqgeRn0ZBJnI6RYAOqDrq79XjBHukhY2wMg9~q4RuB8ip5vLc8xsE01IPzK5b-cy8x4sHCPc5UOhOjNFdA0I~wc8uwXez48xVyR6qs9u4q1A__' --output workshop.zip
$ unzip workshop.zip
$ rm workshop.zip
$ cd ..
$ python3.11 -m venv .
$ bin/pip install --quiet --upgrade pip setuptools wheel build
$ bin/pip install --quiet --upgrade --requirement environment/workshop/setup/requirements.txt
```
At this point, they recommend you run

    bin/python3 environment/workshop/completed/api/bedrock_api.py 

to confirm you have access. This will fail. Modify the code such that any call to
```python
session = boto3.Session()
```
becomes
```python
session = boto3.Session(profile_name='saml-pub')
```
You can also run

    bin/python3 src/test_bedrock.py

which lists the available foundation models and then asks the `titan-text-express-v1` model what a cancer biomarker is.

### Other Bedrock Labs

The folder `src/lab` contains subfolders for each [documented Bedrock Lab](https://catalog.us-east-1.prod.workshops.aws/event/dashboard/en-US/workshop/) adapted for use at JPL. For example, the folder `src/lab/f-2` is for the [F-2 InvokeModel API lab](https://catalog.us-east-1.prod.workshops.aws/event/dashboard/en-US/workshop/foundation/bedrock-apis).

To run each of these, first login with `aws-login` as above; then use the Python virtual environment to invoke each script. For example, for the F-2 lab:

    bin/python3 src/lab/f-2/bedrock_api.py


### Lab I-1: RAG Chatbot

The retrieval-augmented generator chatbot requires some additional setup before it can be run. First, edit the file `environment/workshop/data/populate_collection.py` and change line 8 from

    session = boto3.Session()

to

    session = boto3.Session(profile_name='saml-pub')

Then run:
```console
$ cd environment/workshop/data
$ ../../../bin/python3 populate_collection.py
$ cd ../../..
```
You can then start the chat with:
```console
$ cd src/lab/i-1
$ ../../../bin/streamlit run rag_chatbot_app.py --server.port 8080
```
Your browser should automatically open to http://localhost:8080.

⚠️ **Note:** It still won't work! None of the models we have access support both "tool use" and `converse` which are apparently required for this example.


## Available Models

The JPL Bedrock contract provides the following foundation models:

- Llama 3 70B Instruct (ID: `meta.llama3-70b-instruct-v1:0`)
- Llama 3 8B Instruct (ID: `meta.llama3-8b-instruct-v1:0`)
- Llama 3.1 405B Instruct (ID: `meta.llama3-1-405b-instruct-v1:0`) — tool-capable!
- Llama 3.1 70B Instruct (ID: `meta.llama3-1-70b-instruct-v1:0`) — tool-capable!
- Llama 3.1 8B Instruct (ID: `meta.llama3-1-8b-instruct-v1:0`) — tool-capable!
- Llama 3.2 11B Instruct (ID: `meta.llama3-2-11b-instruct-v1:0`)
- Llama 3.2 1B Instruct (ID: `meta.llama3-2-1b-instruct-v1:0`)
- Llama 3.2 3B Instruct (ID: `meta.llama3-2-3b-instruct-v1:0`)
- Llama 3.2 90B Instruct (ID: `meta.llama3-2-90b-instruct-v1:0`)
- Llama 3.3 70B Instruct (ID: `meta.llama3-3-70b-instruct-v1:0`)
- Nova Lite (ID: `amazon.nova-lite-v1:0`)
- Nova Micro (ID: `amazon.nova-micro-v1:0`)
- Nova Pro (ID: `amazon.nova-pro-v1:0`)
- Rerank 1.0 (ID: `amazon.rerank-v1:0`)
- Titan Embeddings G1 - Text (ID: `amazon.titan-embed-text-v1`)
- Titan Image Generator G1 (ID: `amazon.titan-image-generator-v1`)
- Titan Image Generator G1 (ID: `amazon.titan-image-generator-v1:0`)
- Titan Image Generator G1 v2 (ID: `amazon.titan-image-generator-v2:0`)
- Titan Multimodal Embeddings G1 (ID: `amazon.titan-embed-image-v1`)
- Titan Multimodal Embeddings G1 (ID: `amazon.titan-embed-image-v1:0`)
- Titan Text Embeddings v2 (ID: `amazon.titan-embed-g1-text-02`)
- Titan Text Embeddings V2 (ID: `amazon.titan-embed-text-v2:0`)
- Titan Text G1 - Express (ID: `amazon.titan-text-express-v1`)
- Titan Text G1 - Lite (ID: `amazon.titan-text-lite-v1`)
- Titan Text Large (ID: `amazon.titan-tg1-large`)
