import boto3
from pprint import pformat
import argparse
import json

'''
This script creates a new dashboard analysis within QuickSight.
For detailed explanation of the parameters, refer: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/create_analysis.html
Note: Ensure active credentials before executing this script. Save the analysis ARN for future references; this will be printed in console.

Args:
    target_account_id (str): The AWS account ID of the target environment (e.g., prod).
    region_name (str): The AWS region where QuickSight is deployed.
    analysis_id (str): The ID of the analysis. The ID must be unique per AWS account.
    analysis_name (str): The name of the analysis. A readable name to identify the analysis.
    source_account_template_arn (str): The ARN of the template to be used for the analysis.
    dataset_references_file_path (str): The path to the dataset references file.

Return:
    Analysis ARN (str): The ARN of the analysis created.

Execution:
    python create_analysis.py --target-account-id 123456789012 --region-name us-west-2 --analysis-id my-analysis-id --analysis-name "My Analysis" \
    --source-account-template-arn "arn:aws:quicksight:us-west-2:123456789012:template/my-template" --dataset-references-file-path "./target_dataset_references.json"

'''

parser = argparse.ArgumentParser(description='Create a QuickSight Analysis')
parser.add_argument('--target-account-id', '-t', type=str, required=True,
                    help='The AWS account ID of the target environment (e.g., prod)')
parser.add_argument('--region-name', '-r', type=str, required=True,
                    help='The AWS region where QuickSight is deployed')
parser.add_argument('--analysis-id', '-i', type=str, required=True,
                    help='The ID of the analysis. The ID must be unique per AWS account.')
parser.add_argument('--analysis-name', '-n', type=str, required=True,
                    help='The name of the analysis. A readable name to identify the analysis.')
parser.add_argument('--source-account-template-arn', '-s', type=str, required=True,
                    help='The ARN of the template to be used for the analysis.')
parser.add_argument('--dataset-references-file-path', '-f', type=str, required=True,
                    help='JSON file containing dataset references.')

args = parser.parse_args()

target_account_id = args.target_account_id
region_name = args.region_name
analysis_id = args.analysis_id
analysis_name = args.analysis_name
source_account_template_arn = args.source_account_template_arn
dataset_references_file_path = args.dataset_references_file_path

client = boto3.client('quicksight', region_name=region_name)

print(f'Creating analysis {analysis_id} in account {target_account_id} using template {source_account_template_arn}')

dataset_references = None
with open(dataset_references_file_path) as dataset_references_file:
    dataset_references = json.load(dataset_references_file)
    print(f'Dataset references are \n {pformat(dataset_references)}')

response = client.create_analysis(
    AwsAccountId=target_account_id,
    AnalysisId=analysis_id,
    Name=analysis_name,
    SourceEntity={
        "SourceTemplate": {
            'DataSetReferences': dataset_references,
            "Arn": source_account_template_arn
        }
    },
)

print(pformat(response))
