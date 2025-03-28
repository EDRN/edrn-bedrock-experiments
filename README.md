# Amazon Bedrock

[Amazon Bedrock](https://aws.amazon.com/bedrock/) is an AWS-provided service for generative AI. It supports a number of foundation models all of which can be accessed through a single API and web interface. This makes it possible to experiment with and evaluate different foundation models for specific use cases and select the best one for the application.

JPL has provided access to Bedrock. See "Available Models" below for a list of the enabled models.

The [Early Detection Research Network](https://edrn.nci.nih.gov/) (EDRN) is a cooperative project of JPL and the National Cancer Institute that we're using as a test case for Bedrock. EDRN has a large amount of data (cancer biomarkers, research protocols, thousands of publications, for example) that make it ideal for Bedrock experimentation.


## AWS Login for JPL Users

To use Bedrock at JPL, you need to authenticate. To do so, first visit the [AWS CLI and BOTO with JPL Credentials page](https://wiki.jpl.nasa.gov/x/a4XyGQ) and download the JPL AWS CLI helper for your platform.

For example, for macOS, download the file `aws-login.darwin.amd64`, rename it to simply `aws-login`, and make it executable; then log in:

    aws-login --pub --region us-west-2 --profile saml-pub --username USERNAME

You'll be prompted for your JPL password as well as your RSA PIN and token code. Then choose a role from the menu. For EDRN, that's `am-edrn-dev`. In the future, you can then do

    aws-login --pub --region us-west-2 --profile saml-pub --username USERNAME --last_role

to skip the menu.

👉 **Note:** The login afforded by the above command has a limited lifetime. If you ever get something like

    botocore.exceptions.ClientError: An error occurred (ExpiredTokenException) when calling the ListFoundationModels operation: The security token included in the request is expired

simply re-run the `aws-login` commmand as shown above.


## Bedrock Lab

AWS provides a series of "labs" that teach the core concepts of Bedrock. [Getting started with Bedrock](https://catalog.workshops.aws/building-with-amazon-bedrock/en-US/prerequisites/lab-setup) is simple enough, however here are specific commands in brief that you can follow along with to set up your "lab environment":
```console
$ mkdir environment
$ cd environment
$ curl \
    'https://static.us-east-1.prod.workshops.aws/public/5dd5dc48-363d-4c69-9007-9e5528c5c31f/assets/workshop.zip' \
    --output workshop.zip
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
$ mdkir data
$ mv environment/workshop/data/chroma data
```
You can then start the chat with:

    bin/streamlit run rag_chatbot_app.py --server.port 8080

Your browser should automatically open to http://localhost:8080. Questions related to AWS Bedrock should indicate "tool use" in the console log and an answer from the Bedrock FAQ that's in the `data/chroma` database. Questions not-related to AWS Bedrock will use the foundation model.


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
