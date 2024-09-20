import os
import json
import requests

# Static variables configuration
API_URL = os.environ.get("API_URL")  # Fetch API URL from environment variable
max_age = 600 # Required by the Camara Location Retrieval API. Maximum Age in seconds.
timeout = 10  # Timeout in seconds to call the Camara Location Retrieval API. Adjust this value as needed

def lambda_handler(event, context):
    
    print("event:", event)
    api_path = event['apiPath']
    print("api_path:", api_path )
    action_group = event['actionGroup']
    print("action_group:", action_group)
    http_method = event['httpMethod']
    result = ''
    response_code = 200
    
    # extract value containing the phone number 
    value = event['requestBody']['content']['application/json']['properties'][0]['value']
    phone_number = value.replace("<phoneNumber>", "").replace("</phoneNumber>", "")
    print(f"Phone Number is: {phone_number}")
    device_info = {
        "phoneNumber": phone_number
    }
    
    def retrieve_location(device_info, max_age, api_url):
        request_data = {
            "device": device_info,
            "maxAge": max_age
        }

        # Call Camara Location Retrieval API and extract the location data.
        resp = requests.post(f"{api_url}", json=request_data, timeout=timeout)   
        response = json.loads(resp.text.replace("'","\""))
        print(f"Response {response}")
        resp.raise_for_status()
        location_data = response
    
        print(f"Coordinates:  {location_data}")
        return location_data
    
    # Handle API paths
    if api_path == '/retrieve':
        if not API_URL:
            result = "API URL not configured"
            response_code = 500
        else:
            try:
                result = retrieve_location(device_info, max_age, API_URL)
            except requests.exceptions.RequestException as e:
                result = str(e)
                response_code = 500
    else:
        response_code = 404
        result = f"Unrecognized api path: {action_group}::{api_path}"
        result = retrieve_location(device_info,max_age, API_URL)
    
    # Create output structure as defined in the Location Retrieval Open API document.
    response_body = {
        'application/json': {
            'body': result
        }
    }    
    
    action_response = {
        'actionGroup': action_group,
        'apiPath': api_path,
        'httpMethod': http_method,
        'httpStatusCode': response_code,
        'responseBody': response_body
    }

    api_response = {'messageVersion': '1.0', 'response': action_response}
    return api_response