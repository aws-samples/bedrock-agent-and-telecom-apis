import json
import random

def lambda_handler(event, context):
    print(f"Event: {event}")
    phone_number = json.loads(event['body'])['device']['phoneNumber']
    print(f"Phone Number: {phone_number}, Type {type(phone_number)}")
    
    def retrieve(phone_number):
        # Define the boundaries 
        min_lat, max_lat = 47.4979, 52.3676  # Latitude range
        min_lon, max_lon = 4.9041, 19.0402  # Longitude range
        
        # Generate random latitude and longitude within boundaries
        latitude = random.uniform(min_lat, max_lat)
        longitude = random.uniform(min_lon, max_lon)
        
        result = {
            "lastLocationTime": "2023-01-17T13:18:23.682Z",
            "area": {
                "areaType": "CIRCLE",
                "center": {
                    "latitude": latitude,
                    "longitude": longitude
                },
                "radius": 2000
            }
        }

        return result
    
    result = retrieve(phone_number)
    
    response_body = {
        "isBase64Encoded": "false",
        "statusCode": 200,
        "body": str(result)
    }
    
    print(f"Response Body {response_body}")
    return response_body
