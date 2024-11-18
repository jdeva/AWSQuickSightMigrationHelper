import boto3
from pprint import pformat

'''
This script creates a data source in QuickSight. 
For detailed explanation of the parameters, refer: https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/quicksight/client/create_data_source.html
Note: Ensure active credentials before executing this script.

Args:
    target_account_id (str): The AWS account ID of the target environment (e.g., prod).
    region_name (str): The AWS region where QuickSight is deployed.
    data_source_id (str): The ID of the data source. This ID must be unique within the AWS account. Can be same as dev well
    data_source_name (str): The name of the data source. A simple name to identify the data source.
    data_source_type (str): The type of the data source.
    data_source_type_params (dict): The parameters that are associated with the data source type.
    data_source_credentials (dict): The credentials (username and password) that are associated with the data source.
Returns:
    None
'''

target_account_id = 'XXXXXXXXXXXX'
region_name = 'us-west-2'
data_source_id = 'can_be_same_as_dev_or_any_unique_id'
data_source_name = 'a_simple_name'
data_source_type = 'POSTGRESQL'
data_source_type_params = {
    'PostgreSqlParameters': {
        'Host': 'hostname',
        'Port': 5432,
        'Database': 'postgres'
    },
}
data_source_credentials = {
    'Username': 'postgres',
    'Password': 'your_password_goes_here',
}

client = boto3.client('quicksight', region_name=region_name)

response = client.create_data_source(
    AwsAccountId=target_account_id,
    DataSourceId=data_source_id,
    Name=data_source_name,
    Type=data_source_type,
    DataSourceParameters=data_source_type_params,
    Credentials={
        'CredentialPair': data_source_credentials
    },
    SslProperties={
        'DisableSsl': False
    }
)

print(pformat(response))
