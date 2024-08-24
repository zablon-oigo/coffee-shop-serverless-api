import json
import boto3
import os

dynamo_db = boto3.client('dynamodb')
table_name = os.environ['COFFEE_ORDERS_TABLE']

def lambda_handler(event, context):
    try:
        params = {
            'TableName': table_name
        }
        response = dynamo_db.scan(**params)
        return {
            'statusCode': 200,
            'body': json.dumps(response['Items'])
        }
    except Exception as error:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': f'Could not retrieve orders: {str(error)}'
            })
        }
