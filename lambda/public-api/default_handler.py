# By default we say 404 Not Found
def lambda_handler(event, context):
    return {
        'statusCode': 404,
        'body': 'Not Found'
    }