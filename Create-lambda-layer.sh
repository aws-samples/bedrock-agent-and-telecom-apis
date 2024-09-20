#!/usr/bin/bash

# bash script to create, in AWS CloudShell, a lambda layer for the location-retrieval.py lambda function (this function needs the "requests" python package)

# Pre-requirement: 
# 	
# Upload in the S3 bucket "s3://customer-agent-with-camara-api-${AWS_ACCOUNT_ID}/bedrock-agent-and-telecom-apis/" the git repo /Lambda-functions/LocationRetrieval-TelcoAPI/ directory with the location-retrieval.py file
# 
# Access AWS CloudShell:
#		Log in to the AWS Management Console.
#		Click on CloudShell icon 
# 		Upload the Create-lambda-layer.sh file (Go to "Actions" and Select "Upload file")
# 	
# 		To run the script use the command "sudo chmod +x ./Create-lambda-layer.sh && ./Create-lambda-layer.sh"


# optional install an updated python version
# sudo amazon-linux-extras install python3.12 -

AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)


mkdir my_lambda_layer
cd my_lambda_layer

#python -m venv venv
#source venv/bin/activate

#mkdir python
#cd python

pip install requests -t .

rm -rf *dist-info

#cd ..

aws s3 cp s3://customer-agent-with-camara-api-${AWS_ACCOUNT_ID}/bedrock-agent-and-telecom-apis/Lambda-functions/LocationRetrieval-TelcoAPI/location-retrieval.py ./lambda_function.py

#cp ../Lambda-functions/LocationRetrieval-TelcoAPI/location-retrieval.py ./lambda_function.py

zip -r my_lambda_layer.zip ./


aws s3 cp my_lambda_layer.zip s3://customer-agent-with-camara-api-${AWS_ACCOUNT_ID}/

cd ..

rm -r my_lambda_layer

echo "After this script execution is completed you have the my_lambda_layer.zip file available in the s3://customer-agent-with-camara-api-${AWS_ACCOUNT_ID}/bedrock-agent-and-telecom-apis/ S3 bucket"


mkdir Parcel_Status
cd Parcel_Status
aws s3 cp s3://customer-agent-with-camara-api-${AWS_ACCOUNT_ID}/bedrock-agent-and-telecom-apis/Lambda-functions/ParcelStatus-DB/Parcel_Status_api.py ./lambda_function.py
zip -r Parcel_Status_api.zip ./ 
aws s3 cp Parcel_Status_api.zip s3://customer-agent-with-camara-api-${AWS_ACCOUNT_ID}/
cd .. 
rm -r Parcel_Status

mkdir Place-Search-AWS-Location
cd Place-Search-AWS-Location
aws s3 cp s3://customer-agent-with-camara-api-${AWS_ACCOUNT_ID}/bedrock-agent-and-telecom-apis/Lambda-functions/PlaceSearch-AWS/Place-Search-AWS-Location.py ./lambda_function.py
zip -r Place-Search-AWS-Location.zip ./ 
aws s3 cp Place-Search-AWS-Location.zip s3://customer-agent-with-camara-api-${AWS_ACCOUNT_ID}/
cd .. 
rm -r Place-Search-AWS-Location


mkdir Camara_API_External
cd Camara_API_External
aws s3 cp s3://customer-agent-with-camara-api-${AWS_ACCOUNT_ID}/bedrock-agent-and-telecom-apis/Dummy_Camara/Lambda-Function/Camara_API_External.py ./lambda_function.py
zip -r Camara_API_External.zip ./ 
aws s3 cp Camara_API_External.zip s3://customer-agent-with-camara-api-${AWS_ACCOUNT_ID}/
cd .. 
rm -r Camara_API_External

# Now in the s3://customer-agent-with-camara-api-${AWS_ACCOUNT_ID}/ S3 bucket
# we have the three zip file with python code for the three lamdba function 
# /Lambda-functions/ParcelStatus-DB/Parcel_Status_api.py -> Parcel_Status_api.zip
# /Lambda-functions/PlaceSearch-AWS/Place-Search-AWS-Location.py-> Place-Search-AWS-Location.zip
# /Dummy_Camara/Lambda-Function/Camara_API_External.py -> Camara_API_External.zip


AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

aws s3 cp openAPI-spec/ParcelStatus-API.json s3://customer-agent-with-camara-api-${AWS_ACCOUNT_ID}/
aws s3 cp openAPI-spec/Place-Search-AWS-Location-API.json s3://customer-agent-with-camara-api-${AWS_ACCOUNT_ID}/
aws s3 cp openAPI-spec/location-retrieval.yaml s3://customer-agent-with-camara-api-${AWS_ACCOUNT_ID}/
aws s3 cp Lambda-functions/ParcelStatus-DB/Sqlite-db/file.sqli s3://customer-agent-with-camara-api-${AWS_ACCOUNT_ID}/
