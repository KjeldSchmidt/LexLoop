import os


class MetaBase:
    host = "http://localhost:7894"
    region = "eu-central-1"
    aws_access_key_id = os.environ.get("AWS_ACCESS_KEY_ID", "testFake")
    aws_secret_access_key = os.environ.get("AWS_SECRET_ACCESS_KEY", "testFake")
