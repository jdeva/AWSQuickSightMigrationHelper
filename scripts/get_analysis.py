import boto3
from pprint import pformat
import argparse

'''
This script queries and prints information for an analysis passed.
For detailed explanation of the parameters, refer: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/describe_analysis.html
Note: Ensure active credentials before executing this script. Save the dashboard ARN for future references; this will be printed in console.

Args:
    account_id (str): The AWS account ID of the QuickSight analysis.
    region_name (str): The AWS region where QuickSight is deployed.
    analysis_id (str): The ID of the analysis.

Return:
    prints the analysis details on the console

Execution:
    python get_analysis.py --account-id 123456789012 --region-name us-west-2 --analysis-id my-analysis-id
'''

parser = argparse.ArgumentParser(description='Query and print information for a QuickSight analysis')
parser.add_argument('--account-id', '-a', type=str, required=True,
                    help='The AWS account ID of the QuickSight analysis')
parser.add_argument('--region-name', '-r', type=str, required=True,
                    help='The AWS region where QuickSight is deployed')
parser.add_argument('--analysis-id', '-i', type=str, required=True,
                    help='The ID of the analysis')

args = parser.parse_args()

account_id = args.account_id
region_name = args.region_name
analysis_id = args.analysis_id

print(f'Getting analysis {analysis_id}')

client = boto3.client('quicksight', region_name=region_name)

response = client.describe_analysis(
    AwsAccountId=account_id,
    AnalysisId=analysis_id
)
print(pformat(response))
