import logging
import requests

def lambda_handler(event, context):
    # Get enrollment request status from FEMR central database
    logging.info("Getting enrollment requests")

    response = requests.get("http://skelechaingang-env.eba-i65amzvv.us-west-2.elasticbeanstalk.com/enrollment-status/")

    logging.info(f"Received response from fEMR central database: {response}")

    return {
        'statusCode': 200,
        'headers': {
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET',
            'Access-Control-Allow-Headers': 'Content-Type',
        },
        'body': response.text
    }
