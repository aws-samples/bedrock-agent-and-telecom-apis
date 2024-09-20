import os
import json
import tempfile
import boto3
import sqlite3
from botocore.exceptions import ClientError

def lambda_handler(event, context):
    try:
        # Extract tracking number from input event
        track_number = event["requestBody"]["content"]["application/json"]["properties"][0]["value"]

        # Connect to database
        s3 = boto3.client('s3')
        sts_client = boto3.client('sts')

        # Get the AWS account ID
        account_id = sts_client.get_caller_identity()['Account']

        # Construct the S3 bucket name using the account ID
        s3_bucket_name = f'customer-agent-with-camara-api-{account_id}'
        bucket = s3_bucket_name
        db_name = 'file.sqli'

        # Create a secure temporary file
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            local_db = temp_file.name

        # Download the database file from S3
        try:
            s3.download_file(Bucket=bucket, Key=db_name, Filename=local_db)
        except ClientError as e:
            return handle_error(event, e)

        # Query the database
        conn = sqlite3.connect(local_db)
        cursor = conn.cursor()

        if event['apiPath'] == '/ParcelStatus':
            cursor.execute("SELECT courier_phone_number FROM parcels WHERE tracking_number = ? AND last_mile_status = 1", (track_number,))
            result = cursor.fetchone()

            if result:
                response_code = 200
                result = result[0]
            else:
                response_code = 404
                result = "Unrecognized tracking number"

        else:
            response_code = 404
            result = f"Unrecognized api path: {event['actionGroup']}::{event['apiPath']}"

        response_body = {
            'application/json': {
                'body': result
            }
        }

        # Construct response
        action_response = {
            'actionGroup': event['actionGroup'],
            'apiPath': event['apiPath'],
            'httpMethod': event['httpMethod'],
            'httpStatusCode': response_code,
            'responseBody': response_body
        }

        api_response = {'messageVersion': '1.0', 'response': action_response}

    except Exception as e:
        return handle_error(event, e)

    finally:
        # Clean up the temporary file
        if os.path.exists(local_db):
            os.remove(local_db)

    return api_response

def handle_error(event, error):
    print(f"Caught exception: {error}")
    response_code = 500
    result = "Internal Server Error"

    response_body = {
        'application/json': {
            'body': result
        }
    }

    action_response = {
        'actionGroup': event['actionGroup'],
        'apiPath': event['apiPath'],
        'httpMethod': event['httpMethod'],
        'httpStatusCode': response_code,
        'responseBody': response_body
    }

    api_response = {'messageVersion': '1.0', 'response': action_response}

    return api_response