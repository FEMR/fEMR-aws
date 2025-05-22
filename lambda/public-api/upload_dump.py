import boto3
import base64
import os
from datetime import datetime

s3 = boto3.client('s3')
BUCKET_NAME = os.environ['BUCKET_NAME']

def lambda_handler(event, context):
    kit_id = event['pathParameters'].get('id')

    if not kit_id:
        return response(400, "Missing ID in path")
    
    body = event.get('body')
    is_base64 = event.get('isBase64Encoded', False)
    headers = event["headers"]
    content_type = headers.get('Content-Type', 'application/octet-stream') if headers else 'application/octet-stream'

    if not body:
        return response(400, "No file data provided.")

    # TODO: Authenticate the user

    file_data = base64.b64decode(body) if is_base64 else body.encode('utf-8')
    file_key = f"{kit_id}/{datetime.now().isoformat()}.sql.gz"

    s3.put_object(
        Bucket=BUCKET_NAME,
        Key=file_key,
        Body=file_data,
        ContentType=content_type
    )

    return response(200, {
        "message": "Uploaded",
        "s3_key": file_key
    })

def response(status_code, body):
    import json
    return {
        'statusCode': status_code,
        'body': json.dumps(body),
        'headers': {
            'Content-Type': 'application/json'
        }
    }
