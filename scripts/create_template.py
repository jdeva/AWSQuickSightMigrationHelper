import boto3
from pprint import pformat
import argparse
import json

'''
This script creates a new dashboard template within QuickSight.
For detailed explanation of the parameters, refer: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/create_template.html
Note: Ensure active credentials before executing this script. Save the template ARN for future references; this will be printed in console.

Args:
    source_account_id (str): The AWS account ID of the source environment (e.g., prod).
    region_name (str): The AWS region where QuickSight is deployed.
    template_id (str): The ID of the template. The ID must be unique per AWS account.
    template_name (str): The name of the template. A readable name to identify the template.
    template_version (str): The version number of the template. This should be 1 everytime a template is created.
    dataset_references_file_path (str): The path to the dataset references file.
    source_analysis_arn (str): The ARN of the analysis to be copied.

Return:
    Template ARN (str): The ARN of the template created.

Execution:
    python create_template.py --source-account-id 123456789012 --region-name us-west-2 --template-id my-template-id --template-name "My Template" \
    --template-version 1 --dataset-references-file-path "./source_dataset_references.json" --source-analysis-arn "arn:aws:quicksight:us-west-2:123456789012:analysis/my-analysis"

Post creation steps:
    1. Ensure template is in CREATION_SUCCESSFUL state.
        aws quicksight describe-template --aws-account-id target_account_id --template-id "your_template_id"
    2. Prepare a json file TemplatePermissions.json in the root of the current directory, with permissions for the template. Content as below.
        [
          {
            "Principal": "arn:aws:iam::target_account_id:root",
            "Actions": ["quicksight:UpdateTemplatePermissions","quicksight:DescribeTemplate", "quicksight:PassDataSet"]
          }
        ]
    3. Grant permissions to the template.
        aws quicksight update-template-permissions --aws-account-id source_account_id --template-id "your_template_id" --grant-permissions file://./TemplatePermissions.json --region region_name               
'''

parser = argparse.ArgumentParser(description='Create a new QuickSight Dashboard Template')
parser.add_argument('--source-account-id', '-s', type=str, required=True,
                    help='The AWS account ID of the source environment (e.g., prod)')
parser.add_argument('--region-name', '-r', type=str, required=True,
                    help='The AWS region where QuickSight is deployed')
parser.add_argument('--template-id', '-i', type=str, required=True,
                    help='The ID of the template. The ID must be unique per AWS account.')
parser.add_argument('--template-name', '-n', type=str, required=True,
                    help='The name of the template. A readable name to identify the template.')
parser.add_argument('--template-version', '-v', type=str, required=True,
                    help='The version number of the template. This should be 1 everytime a template is created.')
parser.add_argument('--dataset-references-file-path', '-f', type=str, required=True,
                    help='JSON file containing dataset references.')
parser.add_argument('--source-analysis-arn', '-a', type=str, required=True,
                    help='The ARN of the analysis to be copied.')

args = parser.parse_args()

source_account_id = args.source_account_id
region_name = args.region_name
template_id = args.template_id
template_name = args.template_name
template_version = args.template_version
dataset_references_file_path = args.dataset_references_file_path
source_analysis_arn = args.source_analysis_arn

print(f'Creating template with id {template_id} for analysis {source_analysis_arn}')

dataset_references = None
with open(dataset_references_file_path) as dataset_references_file:
    dataset_references = json.load(dataset_references_file)
    print(f'Dataset references are \n {pformat(dataset_references)}')

client = boto3.client('quicksight', region_name=region_name)

response = client.create_template(
    AwsAccountId=source_account_id,
    TemplateId=template_id,
    Name=template_name,
    SourceEntity={
        'SourceAnalysis': {
            'Arn': source_analysis_arn,
            'DataSetReferences': dataset_references
        },
    },
    VersionDescription=template_version
)

print(pformat(response))
