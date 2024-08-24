import json
import boto3
import uuid
import os 
dynamo_db = boto3.resource('dynamodb')
table_name = os.environ['COFFEE_ORDERS_TABLE']
table = dynamo_db.Table(table_name)

def lambda_handler(event, context):
    try:
        request_body = json.loads(event['body'])
        customer_name = request_body.get('customer_name')
        coffee_blend = request_body.get('coffee_blend')
        order_id = str(uuid.uuid4())
        params = {
            'TableName': table_name,
            'Item': {
                'OrderId': order_id,
                'CustomerName': customer_name,
                'CoffeeBlend': coffee_blend,
                'OrderStatus': 'Pending'
            }
        }
        table.put_item(Item=params['Item'])
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Order created successfully!',
                'OrderId': order_id
            })
        }
    except Exception as error:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': f'Could not create order: {str(error)}'
            })
        }
