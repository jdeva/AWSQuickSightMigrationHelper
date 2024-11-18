import boto3
from pprint import pformat
import json
import argparse

'''
This script creates a new data set within QuickSight.
For detailed explanation of the parameters, refer: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/create_data_set.html
Note: Ensure active credentials before executing this script. If you have new and existing datasets to be migrated, update the old and create the new datasets separately.

Args:
    target_account_id (str): The AWS account ID of the target environment (e.g., prod).
    region_name (str): The AWS region where QuickSight is deployed.
    data_set_list (str []): The IDs of the data sets that needs to be migrated. The result has to be a list of string.
    data_source_arn (str): The ARN of the data source that is used to create the data set.

Return:
    None

Execution:
    python create_data_set.py --target-account-id 123456789012 --region-name us-west-2 --data-set-list dataset1 dataset2 dataset3 --data-source-arn "arn:aws:quicksight:us-west-2:123456789012:datasource/my-data-source"
'''

parser = argparse.ArgumentParser(description='Create a new QuickSight Data Set')
parser.add_argument('--target-account-id', '-t', type=str, required=True,
                    help='The AWS account ID of the target environment (e.g., prod)')
parser.add_argument('--region-name', '-r', type=str, required=True,
                    help='The AWS region where QuickSight is deployed')
parser.add_argument('--data-set-list', '-d', nargs='+', type=str, required=True,
                    help='The IDs of the data sets that needs to be migrated seperated by a white space')
parser.add_argument('--data-source-arn', '-s', type=str, required=True,
                    help='The ARN of the data source that is used to create the data set.')

args = parser.parse_args()

target_account_id = args.target_account_id
region_name = args.region_name
data_set_list = args.data_set_list
data_source_arn = args.data_source_arn

client = boto3.client('quicksight', region_name=region_name)

print(f'DataSet IDs received are {pformat(data_set_list)}')

for data_set_id in data_set_list:
    try:
        with open(f'qs_extracts/{data_set_id}_dataset.json') as dataset_file:
            dataset_json = json.load(dataset_file)

            physical_table_map = dataset_json['PhysicalTableMap']
            _keys = list(physical_table_map.keys())[:200]

            array_length = len(_keys)
            for i in range(array_length):
                try:
                    physical_table_map[_keys[i]]['CustomSql']['DataSourceArn'] = data_source_arn
                except Exception as e:
                    physical_table_map[_keys[i]]['RelationalTable']['DataSourceArn'] = data_source_arn

            with open(f'qs_extracts/{data_set_id}_dataset_permissions.json') as dataset_perm_file:
                dataset_perm_file_json = json.load(dataset_perm_file)
            response = client.create_data_set(
                AwsAccountId=target_account_id,
                DataSetId=data_set_id,
                Name=dataset_json['Name'],
                PhysicalTableMap=dataset_json['PhysicalTableMap'],
                LogicalTableMap=dataset_json['LogicalTableMap'],
                ImportMode=dataset_json['ImportMode'],
                DataSetUsageConfiguration=dataset_json['DataSetUsageConfiguration'],
            )
            print(pformat(response))

    except Exception as e:
        print(f'Error while migrating dataset {data_set_id}', e)
