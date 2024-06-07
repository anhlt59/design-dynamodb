#!/usr/local/bin/python
import json
import sys

import boto3
from botocore.exceptions import ClientError

sys.stdout.write("Configuring dynamodb\n")
sys.stdout.write("===================\n")
sys.stdout.write("Creating table ...\n")

resource = boto3.resource("dynamodb", region_name="us-east-1", endpoint_url="http://localhost:4566")
with open("/etc/localstack/init/ready.d/schema.json") as f:
    schema = json.load(f)

try:
    table = resource.create_table(**schema)
    table.wait_until_exists()
except ClientError as error:
    sys.stdout.write(f"Got an error: {error}\n")
    sys.exit(1)
else:
    sys.stdout.write(f"Table {schema['TableName']} has been created!!!\n")
