import os
import json
import boto3
from botocore.exceptions import ClientError

INDEX_NAME = os.environ.get('INDEX_NAME')

def lambda_handler(event, context):
    try:
        api_path = event['apiPath']
        action_group = event['actionGroup']
        http_method = event['httpMethod']
        lat, long = extract_coordinates(event)
        result, response_code = handle_api_path(api_path, action_group, lat, long)
        response_body = construct_response_body(result)
        action_response = construct_action_response(action_group, api_path, http_method, response_code, response_body)
        api_response = construct_api_response(action_response)
    except Exception as e:
        api_response = handle_error(event, e)

    return api_response

def extract_coordinates(event):
    lat = float(event["requestBody"]["content"]["application/json"]["properties"][0]["value"])
    long = float(event["requestBody"]["content"]["application/json"]["properties"][1]["value"])
    return lat, long

def handle_api_path(api_path, action_group, lat, long):
    if api_path == '/revGeocode':
        result = reverse_geocode(lat, long)
        response_code = 200
    else:
        response_code = 404
        result = f"Unrecognized api path: {action_group}::{api_path}"

    return result, response_code

def reverse_geocode(lat, long):
    location_client = boto3.client("location")
    try:
        response = location_client.search_place_index_for_position(
            IndexName=INDEX_NAME,
            Position=[long, lat]
        )
        result = response['Results'][0]['Place']['Label']
    except (ClientError, IndexError) as e:
        print(f"Error during reverse geocoding: {e}")
        result = "Error during reverse geocoding"

    return result

def construct_response_body(result):
    return {
        'application/json': {
            'body': result
        }
    }

def construct_action_response(action_group, api_path, http_method, response_code, response_body):
    return {
        'actionGroup': action_group,
        'apiPath': api_path,
        'httpMethod': http_method,
        'httpStatusCode': response_code,
        'responseBody': response_body
    }

def construct_api_response(action_response):
    return {'messageVersion': '1.0', 'response': action_response}

def handle_error(event, error):
    print(f"Caught exception: {error}")
    response_code = 500
    result = "Internal Server Error"
    response_body = construct_response_body(result)
    action_response = construct_action_response(event['actionGroup'], event['apiPath'], event['httpMethod'], response_code, response_body)
    api_response = construct_api_response(action_response)

    return api_response