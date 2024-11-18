import boto3
from pprint import pformat
import argparse

'''
This script updates the published version of a dashboard.
For detailed explanation of the parameters, refer: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/update_dashboard_published_version.html
Note: Ensure active credentials before executing this script. Save the dashboard ARN for future references; this will be printed in console.

Args:
    target_account_id (str): The AWS account ID of the QuickSight analysis.
    region_name (str): The AWS region where QuickSight is deployed.
    dashboard_id (str): The ID of the analysis.
    dashboard_version (int): The version of the dashboard to be made live.

Return:
    prints the dashboard details on the console

Execution
    python publish_dashboard.py --target-account-id 123456789012 --region-name us-west-2 --dashboard-id my-dashboard-id --dashboard-version 2
'''

parser = argparse.ArgumentParser(description='Update the published version of a QuickSight dashboard')
parser.add_argument('--target-account-id', '-t', type=str, required=True,
                    help='The AWS account ID of the QuickSight dashboard')
parser.add_argument('--region-name', '-r', type=str, required=True,
                    help='The AWS region where QuickSight is deployed')
parser.add_argument('--dashboard-id', '-i', type=str, required=True,
                    help='The ID of the dashboard')
parser.add_argument('--dashboard-version', '-v', type=int, required=True,
                    help='The version of the dashboard to be made live')

args = parser.parse_args()

target_account_id = args.target_account_id
region_name = args.region_name
dashboard_id = args.dashboard_id
dashboard_version = args.dashboard_version

client = boto3.client('quicksight', region_name=region_name)

response = client.update_dashboard_published_version(
    AwsAccountId=target_account_id,
    DashboardId=dashboard_id,
    VersionNumber=dashboard_version
)

print(pformat(response))
