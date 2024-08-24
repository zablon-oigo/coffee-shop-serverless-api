import json
import boto3
import os

dynamo_db = boto3.client('dynamodb')
table_name = os.environ['COFFEE_ORDERS_TABLE']

def lambda_handler(event, context):
    try:
        request_body = json.loads(event['body'])
        order_id = request_body.get('order_id')
        new_status = request_body.get('new_status')
        customer_name = request_body.get('customer_name')
        params = {
            'TableName': table_name,
            'Key': {
                'OrderId': {'S': order_id},
                'CustomerName': {'S': customer_name}
            },
            'UpdateExpression': 'SET OrderStatus = :status',
            'ExpressionAttributeValues': {
                ':status': {'S': new_status}
            }
        }
        dynamo_db.update_item(**params)
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Order status updated successfully!',
                'OrderId': order_id
            })
        }
    except Exception as error:
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': f'Could not update order: {str(error)}'
            })
        }
