# AWS Bedrock

Notes. TBD. More to come.


## AWS Login for JPL Users

First visit the [AWS CLI and BOTO with JPL Credentials](https://wiki.jpl.nasa.gov/x/a4XyGQ) page and download the JPL AWS CLI helper for your platform.

For example, for macOS, download the file `aws-login.darwin.amd64`, rename it to simply `aws-login`, and make it executable; then log in:

    aws-login --pub --region us-west-2 --profile saml-pub --username USERNAME

You'll be prompted for your JPL password as well as your RSA PIN and token code. Then choose the role `am-edrn-dev` from the menu. In the future, you can then do

    aws-login --pub --region us-west-2 --profile saml-pub --username USERNAME --last_role

to skip the menu.


## Bedrock Lab

Following instructions at https://catalog.us-east-1.prod.workshops.aws/event/dashboard/en-US/workshop/prerequisites/lab-setup, the following is a variation:

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
