import boto3
from pprint import pformat
import json
import os
import argparse

'''
This script fetches all datasets from a dashboard in QuickSight. 
For detailed explanation of the parameters, refer: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_data_set.html
Note: Ensure active credentials before executing this script.
Account: Source

Args:
    source_account_id (str): The AWS account ID of the source environment (e.g., dev).
    region_name (str): The AWS region where QuickSight is deployed.
    data_set_list (str []): The IDs of the data sets that needs to be migrated. The result has to be a list of string.

Returns:
    Saves 2 files per dataset in a self created folder called qs_extracts.
    The first file is the dataset information itself and the second file is the dataset permission information.

Execution:
    python get_data_sets.py --source-account-id 123456789012 --region-name us-west-2 --data-set-list dataset1 dataset2 dataset3
'''

parser = argparse.ArgumentParser(description='Fetch all datasets from a QuickSight dashboard')
parser.add_argument('--source-account-id', '-s', type=str, required=True,
                    help='The AWS account ID of the source environment (e.g., dev)')
parser.add_argument('--region-name', '-r', type=str, required=True,
                    help='The AWS region where QuickSight is deployed')
parser.add_argument('--data-set-list', '-d', nargs='+', type=str, required=True,
                    help='The IDs of the data sets that needs to be migrated, seperated by a white space')

args = parser.parse_args()

source_account_id = args.source_account_id
region_name = args.region_name
data_set_list = args.data_set_list

next_token = None
client = boto3.client('quicksight', region_name=region_name)

print(f'DataSet IDs received are {pformat(data_set_list)}')

for data_set_id in data_set_list:
    resp = client.describe_data_set(
        AwsAccountId=source_account_id,
        DataSetId=data_set_id
    )
    dataset = resp['DataSet']
    print(pformat(dataset))
    # Create the folder if it doesn't exist
    os.makedirs('qs_extracts', exist_ok=True)
    with open(f'qs_extracts/{data_set_id}_dataset.json', 'w', encoding='utf-8') as f:
        json.dump(dataset, f, ensure_ascii=False, indent=4, default=str)

    resp = client.describe_data_set_permissions(
        AwsAccountId=source_account_id,
        DataSetId=data_set_id
    )
    permissions = resp['Permissions']
    with open(f'qs_extracts/{data_set_id}_dataset_permissions.json', 'w', encoding='utf-8') as f:
        json.dump(permissions, f, ensure_ascii=False, indent=4, default=str)
    print(pformat(permissions))
