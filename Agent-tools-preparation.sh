#!/usr/bin/bash


# 1/ Clone a git and go in the Cloudformation directory
# git clone <git_repo_url>
# cd <repo_name>/Cloudformation

# or aws s3 cp  s3://customer-agent-with-camara-api-${AWS_ACCOUNT_ID}/bedrock-agent-and-telecom-apis/ ./bedrock-agent-and-telecom-apis --recursive

cd Cloudformation
#  Go to the us-west-2 AWS region
aws configure set region us-west-2


# Go to the Cloudformation directory and launch the 2-1-CF-simulated-camara-API.yaml CloudFormation template
aws cloudformation create-stack \
  --stack-name simulated-camara-API \
  --template-body file://2-1-CF-simulated-camara-API.yaml \
  --capabilities CAPABILITY_IAM

# Wait for the simulated-camara-API stack to be created
while true; do
  STACK_STATUS=$(aws cloudformation describe-stacks --stack-name simulated-camara-API --query 'Stacks[0].StackStatus' --output text)
  if [ "$STACK_STATUS" == "CREATE_COMPLETE" ]; then
    break
  elif [ "$STACK_STATUS" == "CREATE_FAILED" ]; then
    echo "Stack creation failed. Exiting."
    exit 1
  else
    echo "Waiting for stack creation to complete..."
    sleep 10
  fi
done

# Retrieve the stack name of the simulated-camara-API stack
CAMARA_API_STACK_NAME=$(aws cloudformation describe-stacks --stack-name simulated-camara-API --query 'Stacks[0].StackName' --output text)

# Launch the 2-2-CF-location-retrieval.yaml CloudFormation template
aws cloudformation create-stack \
  --stack-name location-retrieval \
  --template-body file://2-2-CF-location-retrieval.yaml \
  --parameters ParameterKey=CamaraAPIExternalStackName,ParameterValue=$CAMARA_API_STACK_NAME \
  --capabilities CAPABILITY_IAM

# Launch the 3-CF-Parcel-status.yaml CloudFormation template
aws cloudformation create-stack \
  --stack-name Parcel-status \
  --template-body file://3-CF-Parcel-status.yaml \
  --capabilities CAPABILITY_IAM

# Launch the 4-CF-Place-Search-AWS-Location.yaml CloudFormation template
aws cloudformation create-stack \
  --stack-name Place-Search-AWS-Location \
  --template-body file://4-CF-Place-Search-AWS-Location.yaml \
  --capabilities CAPABILITY_IAM
  
