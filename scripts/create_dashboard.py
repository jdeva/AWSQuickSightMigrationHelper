import boto3
from pprint import pformat
import argparse
import json

'''
This script creates a new dashboard within QuickSight.
For detailed explanation of the parameters, refer: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/create_dashboard.html
Note: Ensure active credentials before executing this script. Save the dashboard ARN for future references; this will be printed in console.

Args:
    target_account_id (str): The AWS account ID of the target environment (e.g., prod).
    region_name (str): The AWS region where QuickSight is deployed.
    dashboard_id (str): The ID of the dashboard. The ID must be unique per AWS account.
    dashboard_name (str): The name of the dashboard. A readable name to identify the dashboard.
    dashboard_version (str): The version number of the dashboard. This should be 1 everytime a new dashboard is created.
    source_account_template_arn (str): The ARN of the template to be used for the dashboard.
    dataset_references_file_path (str): The path to the dataset references file.


Return:
    Dashboard ARN (str): The ARN of the dashboard created.

Execution:
    python create_dashboard.py --target-account-id 123456789012 --region-name us-west-2 --dashboard-id my-dashboard-id --dashboard-name "My Dashboard" --dashboard-version 1 \
    --source-account-template-arn "arn:aws:quicksight:us-west-2:123456789012:template/my-template" --dataset-references-file-path "./target_dataset_references.json"
'''


parser = argparse.ArgumentParser(description='Create a new QuickSight Dashboard')
parser.add_argument('--target-account-id', '-t', type=str, required=True,
                    help='The AWS account ID of the target environment (e.g., prod)')
parser.add_argument('--region-name', '-r', type=str, required=True,
                    help='The AWS region where QuickSight is deployed')
parser.add_argument('--dashboard-id', '-i', type=str, required=True,
                    help='The ID of the dashboard. The ID must be unique per AWS account.')
parser.add_argument('--dashboard-name', '-n', type=str, required=True,
                    help='The name of the dashboard. A readable name to identify the dashboard.')
parser.add_argument('--dashboard-version', '-v', type=str, required=True,
                    help='The version number of the dashboard. This should be 1 everytime a new dashboard is created.')
parser.add_argument('--source-account-template-arn', '-s', type=str, required=True,
                    help='The ARN of the template to be used for the dashboard.')
parser.add_argument('--dataset-references-file-path', '-f', type=str, required=True,
                    help='JSON file containing dataset references.')

args = parser.parse_args()

target_account_id = args.target_account_id
region_name = args.region_name
dashboard_id = args.dashboard_id
dashboard_name = args.dashboard_name
dashboard_version = args.dashboard_version
source_account_template_arn = args.source_account_template_arn
dataset_references_file_path = args.dataset_references_file_path

print(f'Creating dashboard {dashboard_id} in account {target_account_id} using template {source_account_template_arn}')

dataset_references = None
with open(dataset_references_file_path) as dataset_references_file:
    dataset_references = json.load(dataset_references_file)
    print(f'Dataset references are \n {pformat(dataset_references)}')

client = boto3.client('quicksight', region_name=region_name)

response = client.create_dashboard(
    AwsAccountId=target_account_id,
    DashboardId=dashboard_id,
    Name=dashboard_name,
    SourceEntity={
        "SourceTemplate": {
            'DataSetReferences': dataset_references,
            "Arn": source_account_template_arn
        }
    },
    VersionDescription=dashboard_version
)

print(pformat(response))
