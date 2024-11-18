import boto3
from pprint import pformat
import json

client = boto3.client('quicksight', region_name='us-west-2')

resp = client.describe_data_source(
    AwsAccountId='173245911106',
    DataSourceId='138545a7-9a78-48bb-a35c-82c240a7edea'
)

print(pformat(resp))


