# Agents for Amazon Bedrock and Telecom API

## Introduction  
We create an AI-based customer chatbot by using the capabilities of Agents for Amazon Bedrock, Telco Camara API, and GenAI's advanced natural language processing (NLP). We define an Agent in Amazon Bedrock, indicate how to integrate it by calling Telecom Networks API, and interact with other Amazon services such as Amazon Location service.

We use an example scenario with one specific Telco API and Amazon Location to show the building blocks of the solution (GenAI agent interacting with both Telco API and AWS services). The combination of Telecom APIs, AWS services, and GenAI techniques powered by Amazon Bedrock presents an opportunity for innovation. This enables creating customer care applications for different industries and businesses, offering possibilities for customization and personalization.

**Note**: This git repository and the related blog is an example starter project designed to provide a demonstration and basis for builders to create their own solutions. It should not be considered Production-ready. The code should be modified for production use, for example, by including input format validation and more sophisticated error handling.  Moreover, when invoking in production the actual Telco Camara API, that is here simulated through an Amazon API GW and AWS Lambda implementation, a proper authorisation mechanism must be implemented according to the API Telco Operator security rules.
   
This repository is intended to accompany an AWS blog that is in the process of being published.

###  Example scenario and solution overview

We use a logistics company's customer service bot as an example scenario.

A logistics company aims to revolutionize the customer experience by developing a GenAI-powered customer agent application. The solution provides real-time updates on the status and location of ordered parcels, ensuring transparency and convenience for customers.

The system determines whether the parcel is in the "last-mile" status or is still traversing the "long-mile" path. If the system detects the parcel is in the last-mile delivery stage, the logistics company integrates with a Telecom Camara Location Retrieval API. This API allows the application to find the courier's location by using a mobile SIM number, for example, one associated with the driver or the vehicle. By leveraging this technology, the system can pinpoint the precise location of the parcel in the last leg of the journey.

Additionally, the logistics company incorporates Amazon Location services. The application displays the address to locate the package and allow customers to organize for the delivery.

## Solution walkthrough and implementation steps 

The following steps describe the solution workflow: 

- **Step a)	Create the APIs and tools for the Agent** using the following:

    -	An OpenAPI schema JSON format to describe the API, its invocation, and a detailed description of the provided functions (to enable the Agent to select the right APIs for the required action).

    -  A Python-based AWS Lambda function contains the business logic needed to perform API calls.

    As described in the “Example scenario and solution overview” section, we implement three APIs and Lambda functions: 
    1.	A Lambda function that can simulate an interaction with an Internal IT system to determine the parcel status and to provide the courier SIM number.
    1.  A Lambda function that can simulate a Camara Location Retrieval API toward a Telco operator to localize the courier’s position (GPS coordinates) by using the previously indicated SIM number.
    1. A Lambda function that can call the Amazon Location in AWS to obtain the current address to locate the parcel. 


- **Step b)	Create the agent with Amazon Bedrock**

- **Step c)	Configure the Agent** with  the necessary components:

     - Select the preferred Foundation model (FM) from the broad Amazon Bedrock model choice.

    - Provide a high-level description of the expected Agent functionality (how to interact with the end users and what tasks to perform).

    - Associate the Agent with the available action groups (API calls defined in Step a) that the Agent can use to break down customer requests into tasks and fulfill them

- **Step d)	Test and deploy your agent created with Amazon Bedrock**

## Repository Structure
This git repository is structured with directories that includes all instructions and artifacts required to implement this use case. It containes:

* _/BedrockAgent_: the prompt to instruct Bedrock Agent.
* _/CloudFormation_: the Cloudformation templates to deploy the pre-requirements and the tools for Amazon Bedrock Agent.
* _/Dummy_Camara_: the lambda function and instructions to create an API to simulate the Location Retrieval API.
* _/Lambda-functions_: lambda functions and test events for the tools used by Amazon Bedrock Agents
* _/openAPI-spec_: the definition of the tools for Amazon Bedrock Agents in the format of OpenAPI specification.  

## Prerequisites

To implement this solution, you need the following prerequisites:


- An AWS account and access to Amazon Bedrock with Agents enabled (see [Amazon Bedrock documentation](https://docs.aws.amazon.com/bedrock/latest/userguide/bedrock-regions.html) for the supported regions and models)
- Basic knowledge of GenAI, Amazon Bedrock, AWS Lambda functions in Python, Amazon Simple Storage Service (Amazon S3), and Amazon Location service.
- An S3 bucket in your AWS account in the Region where you want to create your Bedrock Agent.
- An Amazon Location Service resource with a "Place Index" in Amazon Location Service that you want to search against.


In your AWS account, you need to have created an Amazon Location Service resource with a “Place Index” in Amazon Location Service that you want to search against. A Place Index is a graphical search engine to be specified in the API request. See the Amazon Location Service guide to review Amazon Location Service concepts and feature. In our solution we’ll use Amazon Location Service “Places search” feature to convert a latitude/longitude coordinate pair into a street address (reverse geocoding). 

 

We tested this sample with the following configuration:

- Test-Region: US West (Oregon) - us-west-2 

- Amazon Bedrock with Agents enabled and with Access to "Anthropic" - "Claude" 
    
- Amazon Location Service resource with a “Place Index” named "PlaceIndex_for_my_agent" created
    
- A S3 bucket called "customer-agent-with-camara-api-${AWS::AccountId}" created, where ${AWS::AccountId} is your AWS Account id 


Access to Amazon Bedrock foundation models isn't granted by default. You can request access, or modify access, to foundation models only by using the Amazon Bedrock console. To request model access, follow the steps at [Getting started with Amazon Bedrock](https://docs.aws.amazon.com/bedrock/latest/userguide/getting-started.html).

To create the required resources, follow the instructions in "CloudFormation Stage 1 - Pre-requirements resource creation" and "Stage 1.1 - Copy the repository to S3 and create a zip file for lambda functions" sections. 

All CloudFormation templates are available in the /Cloudformation directory of this repository.

### CloudFormation Stage 1 - Pre-requirements resource creation 

- Go to the Cloudformation console and click on "Create Stack"

- Select "Choose an existing template"

- Select "Upload a template file" and upload the file "1-CF-pre-requirement.yaml"

- Click on Next; Enter a Stack name (i.e. TelcoAPI-Agent-pre-reqs) and enter the AWS region where create resources (i.e. us-west-2)

- Click on Next, Maintain next section as default and click on Next

- Review settings and Check "I acknowledge that AWS CloudFormation might create IAM resources" and click on submit 

The Template enables Amazon Bedrock access for Claude v2.1, creates a private S3 bucket (named "customer-agent-with-camara-api-${AWS::AccountId}"), and an Amazon Location Service- Place Index using Esri (named "PlaceIndex_for_my_agent")

#### Stage 1.1 - Copy the repository to S3 and create a zip file for Lambda functions using AWS CloudShell


1. On your local PC, clone or download the repository locally:

> - Use git clone to clone the repository in a directory named "bedrock-agent-and-telecom-apis".
> - Or, download the source code as zip file and unzip it in a directory named "bedrock-agent-and-telecom-apis"

   
2.  Copy the repository directory (named "bedrock-agent-and-telecom-apis") to the created S3 bucket "s3://customer-agent-with-camara-api-${AWS_ACCOUNT_ID}/":

> - Via the AWS Console, go to the S3 console > Buckets > Select the "customer-agent-with-camara-api-${AWS_ACCOUNT_ID}" bucket > Click on Upload > Select Add Folder > Select your local "bedrock-agent-and-telecom-apis" folder where you have downloaded the repository > Click on the Upload button


3. Copy the S3 folder to your AWS CloudShell environment:


> - In the AWS Management Console, go to the AWS CloudShell service.
> - Run the following commands:


>         AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
>         aws s3 cp  s3://customer-agent-with-camara-api-${AWS_ACCOUNT_ID}/bedrock-agent-and-telecom-apis/ ./bedrock-agent-and-telecom-apis --recursive
>         cd bedrock-agent-and-telecom-apis
>         sudo chmod +x ./Create-lambda-layer.sh && ./Create-lambda-layer.sh

These commands copy the S3 bucket to your CloudShell environment and create the necessary zip files for the solution within that folder and in the S3 bucket.

Now all the pre-requirements resources and files, are prepared


## Step a) - Preparation of the tools (APIs) for the BedRock Agent 

For the implementation of the step a), to prepare the tools (APIs) for the Bedrock Agent, we provide two options. The first option is using the AWS Management Console and the second option is using an Infrastructure as Code (IaC) approach with AWS CloudFormation. 

1. For the AWS Management Console option, follow the instructions in the "**Preparation of the tools using AWS Management Console**" section 

1. For the CloudFormation option, follow the instructions in the "**Preparation of the tools using AWS CloudFormation**" section 

Then go to the "**Step b) -  Create the agent with Amazon Bedrock**" section.

### Preparation of the tools using AWS Management Console
In case you prefer to use the Console to create the tools for the Agent, please follow the steps below for each API.

#### /Location retrieval API integration in the Agent


- Lambda function: 

> - Go to the Lambda console: Click on "Create Function", Enter a function name (i.e. location-retrieval), Select the latest Python runtime and click on "create function"  
> - Go to **“Upload from”**   button on the right, Select **"Upload a file from Amazon S3"** and upload the zip file from the S3 bucket and insert "s3://customer-agent-with-camara-api-${AWS_ACCOUNT_ID}/my_lambda_layer.zip" where ${AWS_ACCOUNT_ID is your AWS AccountId (i.e. s3://customer-agent-with-camara-api-12345678902/my_lambda_layer.zip)


> - To allow the Bedrock Agent to invoke this lambda function through the defined API, configure a Resource-based policy statements with the permission for Agents for Amazon Bedrock to Invoke the lambda Function:
> 
>     -  In Configuration – Permissions - Resource-based policy statements - **Add permissions –** Select **AWS Services** – **Other** 
>             -	Statement ID: insert a unique statement ID to differentiate this statement within the policy (i.e. agentsforbedrock-telcoapi-agent-ResourcePolicy-statement)
>             -	**Principal**: bedrock.amazonaws.com
>             -	**Source ARN**: "arn:aws:bedrock:<REGION-NAME>:<Account-ID>:agent/*"
>             -	**Action**: lambda:InvokeFunction
        Click on "Save"


The Lambda function is used to invoke the external Location Retrieval API provided by the Telco company. In case you don’t have access to an actual as defined by Camara, you can simulate it using an Amazon API Gateway and a serving Lambda function. To set up this "simulated Location Retrieval API", follow the instructions available in this file "Dummy_Camara/Lambda-Function/Notes.txt"   

Check that you have correctly configured the API  endpoint as API_URL environment variable in the location-retrieval lamdba function.


To optionally test your Lambda function: 
- Select the **Test** tab near the top of the page. Configure a test event that matches how the Agent sends a request using “Lambda_TEST_EVENT_Locationretrieval.json”.
- Select the **Test** button and see the result in "Executing function” section, explore “Details” and eventually analyze logs.
In the case of a timeout error, increment the default Lambda timeout settings (Configuration Tab > General configuration > Edit > Timeout).



#### /parcelStatus API integration in the Agent

Please consider this is an example lamdba function simulating an interaction with an Internal IT system/database to determine the Parcel status and to provide the courier SIM number.
Our lambda code is backed by an in-memory SQLite database. You can use similar constructs to write to a persistent data store. Load the SQLite example database file (file.sqli) in your pre-created S3 bucket. If you want to see a csv version of this database file you can find it in 'Lambda-functions/ParcelStatus-DB/Sqlite-db/' folder (file named file.csv).


- Lambda function: 
    
> - Go to the AWS Lambda console - Create a lambda function (Parcel_Status_api) with a python runtime 
> 
> - Upload the zip file from the S3 bucket and insert "s3://customer-agent-with-camara-api-${AWS_ACCOUNT_ID}/Parcel_Status_api.zip" 
 (where ${AWS_ACCOUNT_ID is your AWS AccountId (i.e. s3://customer-agent-with-camara-api-12345678902/Parcel_Status_api.zip)

> 
> - Add the "s3-read-policy-agent-camara-api.json" permission policy to the lambda role to allow reading the database file loaded in the S3 bucket 
> 
> - Go to the **Configuration Tab**, select **Permission**, Click on the **Role name** that redirect you to the IAM console. Click on the “**Add Permission**”, create **inline policy**, select **JSON** and copy from the git repository the content of the "Lambda-functions/ParcelStatus-DB/s3-read-policy-agent-camara-api.json“ policy replacing the resource with the arn of the S3 bucket you created in the pre-requisite phase (i.e. arn:aws:s3:::customer-agent-with-camara-api-${AWS_ACCOUNT_ID}/*)
> - Click on the Next button - Enter a Policy name (i.e. S3ReadAccess) and Click on the "Create Policy" button
> 
> - Increment the default lambda timeout settings (Configuration Tab - General configuration - Edit - Timeout (i.e. 10 sec))

  
- To test your Lambda function: 

    - Click on the "Test" tab near the top of the page
    -  Configure a test event that matches how the Agent will send a request using “Lambda_TEST_EVENT_ParcelStatus.json”- 
    Click on Test - See result in "Executing function: Details" and eventually analyze logs

To allow the Bedrock Agent to invoke this lambda function through the defined API, configure a Resource-based policy statements with the permission for Agents for  Amazon Bedrock  to Invoke the lambda Function (as for the other lambda functions configuration):

- In Configuration – Permissions - Resource-based policy statements - Add permissions – Select AWS Services – Other 

    - Statement ID: insert a unique statement ID to differentiate this statement within the policy (i.e. agentsforbedrock-telcoapi-agent-ResourcePolicy-statement)
    - Principal: bedrock.amazonaws.com
    -	Source ARN: "arn:aws:bedrock:<REGION-NAME>:<Account-ID>:agent/*"
    - Action: lambda:InvokeFunction


#### /revGeocode API integration in the Agent

- Lambda function: "Place-Search-AWS-Location"

> - Create a lambda function (Place-Search-AWS-Location) with a python runtime 
> 
> - Upload the zip file from the S3 bucket and insert "s3://customer-agent-with-camara-api-${AWS_ACCOUNT_ID}/Place-Search-AWS-Location.zip" 
 (where ${AWS_ACCOUNT_ID is your AWS AccountId (i.e. s3://customer-agent-with-camara-api-12345678902/Place-Search-AWS-Location.zip)
> 
> - Add the permission policy to the Lambda function to use the geo:SearchPlaceIndexForPosition action on the Place Index resource created in the Prerequisites section. 
> 
>     - Go to the **Configuration Tab**, select **Permission**, Click on the **Role name** that redirect you to the IAM console.
>     - Click on the “**Add Permission**”, create **inline policy**, select **JSON** and copy the content of the "Lambda-functions/PlaceSearch-AWS/PlaceIndex-permission-policy-agent-camara-api.json“ policy replacing <Region>:<Account-id> with your data.
>     -  Click on the Next button, Give a policy name to the policy (i.e. LocationServiceAccess), and Click on the "Create Policy" button

To test your Lambda function: 
- Go back to the lambda console,select the Test tab. 
- Configure a test event that matches how the Agent sends a request using thr json in /Lambda-functions/PlaceSearch-AWS/Lambda_TEST_EVENT_revGeocode;
- Select the Test button and see the result in "Executing function” section, explore “Details” and eventually analyze logs.
	
In case of timeout error, Increment the default Lambda timeout settings (Configuration Tab, General configuration, Edit, Timeout).

In order to allow the Amazon Bedrock Agent to invoke this Lambda function through the defined API, configure a Resource-based policy statement with the permission for Agents for Amazon Bedrock to invoke the Lambda function (as for the other Lambda functions configuration):

- In Configuration – Permissions - Resource-based policy statements - Add permissions – Select AWS Services – Other 

    - Statement ID: insert a unique statement ID to differentiate this statement within the policy (i.e. agentsforbedrock-telcoapi-agent-ResourcePolicy-statement)
    -	Principal: bedrock.amazonaws.com
    -	Source ARN: "arn:aws:bedrock:<REGION-NAME>:<Account-ID>:agent/*"
    -	Action: lambda:InvokeFunction
 
The Amazon Location Service "Index name" must be inserted as environment variable in the lambda function, as "INDEX_NAME" variable 

    - Go to Configuration Tab > Environment variables
    - Key = INDEX_NAME and Value = PlaceIndex_for_my_agent 
    - Click on "Save Button”

Now go to section "**Step b) -  Create the agent with Amazon Bedrock**" 

### Preparation of the tools using AWS CloudFormation

In case you prefer to use an Infrastructure as Code (IaC) approach in the tools creation for the Agent, follow the next steps to deploy the AWS resources needed for the Agent, after downloading the CloudFormation YAML files from the "Cloudformation/" folder on your local PC.

If you prefer to deploy the AWS services for one tool/API at a time, follow the instructions provided in the paragraph Option A - Deploy single APIs with CloudFormation.  

If, instead, you want to perform the deployment in a single step, go directly to the paragraph "Option B - Run all the preparation steps with CloudFormation from CloudShell". 

### Option A - Deploy single APIs with CloudFormation

#### CloudFormation Stage  2 - Location Retrieval API Lamdba function creation 

##### Stage 2.1 - Simulated Camara API creation

In this step we create the lambda function (triggered by an API gateway) that simulate the Location Retrieval Camara API 

- Go to the Cloudformation console and click om "Create Stack" in the AWS region where you have created the pre-requirement resources in the previous step (i.e. us-west-2)

- Select "Upload a template file" and upload the file "2-1-CF-simulated-camara-API.yaml"

- Click on Next; Enter a Stack name (i.e. simulated-camara-API) 

- Click on Next, Maintain sections as defaults and click on Next

- Review settings and Check "I acknowledge that AWS CloudFormation might create IAM resources" and click on submit 

The Template creates a lambda function (named "Camara_API_External" and triggered by an API gateway) that simulate the Location Retrieval Camara API 

Waiting for stack creation to complete.


##### Stage 2.2 -  Location Retrieval API - Lamdba function creation 

- Go to the Cloudformation console and click om "Create Stack" in the AWS region where you have created the pre-requirement resources in the previous step (i.e. us-west-2)

- Select "Upload a template file" and upload the file "2-2-CF-location-retrieval.yaml"

- Click on Next; Enter a Stack name (i.e. location-retrieval) 
    Enter in the "CamaraAPIExternalStackName" parameter the Stack name of the cloud formation stack created in Step 2.1 (i.e. simulated-camara-API) 
	
- Click on Next, Maintain sections as defaults and click on Next

- Review settings and Check "I acknowledge that AWS CloudFormation might create IAM resources" and click on submit 

The Template creates the lambda function (named "location-retrieval") for the Amazon Bedrock Action group able to call the Location Retrieval  API 


#### CloudFormation Stage 3 - Parcel Status API - Lamdba function creation 


- Go to the Cloudformation console and click om "Create Stack" in the AWS region where you have created the pre-requirement resources in the previous step (i.e. us-west-2)

- Select "Upload a template file" and upload the file "3-CF-Parcel-status.yaml"

- Click on Next; Enter a Stack name (i.e. Parcel-status) 

- Click on Next, Maintain sections as defaults and click on Next

- Review settings and Check "I acknowledge that AWS CloudFormation might create IAM resources" and click on submit 

The Template creates the lambda function (named "Parcel_Status_api) for the Amazon Bedrock Action group able to call the Parcel Status  API

#### CloudFormation Stage  4 -  revGeocode API  - Lamdba function creation 

- Go to the Cloudformation console and click om "Create Stack" in the AWS region where you have created the pre-requirement resources in the previous step (i.e. us-west-2)

- Select "Upload a template file" and upload the file "4-CF-5-CF-Place-Search-AWS-Location.yaml.yaml"

- Click on Next; Enter a Stack name (i.e. Place-Search-AWS-Location) 

- Click on Next, Maintain sections as defaults and click on Next

- Review settings and Check "I acknowledge that AWS CloudFormation might create IAM resources" and click on submit 

The Template creates the lambda function (named "Place-Search-AWS-Location") for the Amazon Bedrock Action group able to call the revGeocode  API

#### Check the OpenAPI specification files to the S3 bucket

Check to have the following files in the S3 bucket: file.sqli, location-retrieval.yaml	my_lambda_layer.zip, ParcelStatus-API.json, Place-Search-AWS-Location-API.json

### Option B - Run all the preparation steps with CloudFormation from CloudShell 

We can use AWS Cloudshell environment to run all the cloud formation stacks using a linux script. Go to your Cloudshell console, Make sure you are in the directory of the git repo (named "bedrock-agent-and-telecom-apis" ) and start by executing the following script 

    sudo chmod +x ./Agent-tools-preparation.sh && ./Agent-tools-preparation.sh

- Wait until all the cloud formation stacks are in "CREATE_COMPLETE" Status in the CloudFormation console

- Check to have the following files in the S3 bucket (named "customer-agent-with-camara-api-${AWS::AccountId}"): file.sqli, location-retrieval.yaml	my_lambda_layer.zip, ParcelStatus-API.json, Place-Search-AWS-Location-API.json


## Step b) -  Create the agent with Amazon Bedrock 
To create an agent, open the Amazon Bedrock console and choose Agents in the left navigation pane. Then select "Create Agent".
 
This starts the agent creation workflow.
1.	Provide agent details: Give the agent a name (i.e. AnyLogistic-Agent) and description (optional) and then select “Create”
2.	In the Agent Builder page, in the “Agent resource role”  choose “Create and use a new service role”- Leave all other sessions as default and click on “Save and Exit”
3.	Now in the  Amazon Bedrock console,  choosing “Agents” in the left navigation pane, you see the created Agent in the list with a “Not prepared” Status 


## Step c) - Configure the Agent 

1.	Go to the Amazon Bedrock console and choose Agents in the left navigation pane. Select the Agent created in the first Step. Click on “Edit in Agent Builder” 
2.	In the “Select model” select a foundation model from Bedrock that fits your use case (i.e. ClaudeV2.1)
3.	In the “Instructions for the Agent”, provide an instruction to your agent in natural language. The instruction tells the agent what task it’s supposed to perform and the persona it’s supposed to assume
 In our example we provided the following instructions: “_You are an assistant of a logistic company that interact with the final user to provide the street address where the parcel is currently. Customer is supposed to provide parcel ID, while you as an assistant are provided the tools to retrieve courier phone number, mobile phone coordinates and street address”._  Different formulations of the instructions are possible, and tuning it is part of the “prompt engineering” process.

### Create Action Group

For every of our three API (/parcelStatus, /Location retrieval, /revGeocode) 

1. In the “Action groups” click on the Add button to create a new Action Group for the agent.

2.	Provide the Action Group Name (i.e. action-group-location-retrieval)  and Description (Optional). 
- In the "Action group type" Select “Define with API Schema” 
- In the "Action group invocation" section, select the "Select an existing Lambda fucntion" Option
- Choose the specific Lambda function (i.e. location-retrieval),
- In the "Action group schema" section,  Select “Select an existing API Schema” option, Click on "Browse S3" button, Select the "s3://customer-agent-with-camara-api-${AWS_ACCOUNT_ID}" S3 Bucket, Select the file with OpenAPI specification (i.e. location-retrieval.yaml), click "Choose" 
- Click on "Create" button to create the “Action Group”  

Repeat the same procedure for remaining API, using the specified values for lambda function name (i.e.Parcel_Status_api, Place-Search-AWS-Location) and the API Schema file in the S3 bucket (i.e. ParcelStatus-API.json and Place-Search-AWS-Location-API.json).

Finally  Click on “Save and exit button” in the Agent Builder page to Save the new Agent’s configuration 

Verify that the “Instructions for the Agent”, in the "Agent Details" section is filled with the instruction previously configured.

Click on “Prepare Button” to prepare the Agent (the Agent Status must be a in “Ready state” to allow a testing)

## Step d) Test and deploy your Agent created with Amazon Bedrock

 ### Test the Agent
 
1.	Check the Agent is in "Prepared" Status (otherwise in the Agent go to "Working draft" click  "Prepare")
2.	Test the Agent using the Test session ("Run" button)
    - By selecting "Show trace" for each response, a dialog box shows the reasoning technique used by the agent and the final response generated by the Foundation Model (FM) . 
3.	Try out some different prompts in "Working draft" -"Instruction for the Agent" and test the limits of the agent (Note: "prepare" the Agent after any Prompt/instruction Update)

To test the Agent, consider that in the sample SQLite database, we have inserted data for the following Parcel_ID/Tracking numbers: 225566771, 225566772, 225566773, 225566873, 225566874, 225566875. So, insert these "Parcel IDs" for your tests.

To understand how to customize the Agent orchestration prompt and the model inference parameters see https://docs.aws.amazon.com/bedrock/latest/userguide/advanced-prompts-configure.html

### Deploy your Agent
    
After successful testing, you can deploy your agent. To deploy an agent in your application, you must create an alias. Amazon Bedrock then automatically creates a version for that alias.

	
## Cleaning up

To avoid incurring future charges, delete all the created resources (S3 bucket, Amazon Location Place Index, Lambda functions, Agents for Amazon Bedrock, directories on your AWS CloudShell environment, Cloudformation stacks)


## Security

See [CONTRIBUTING](CONTRIBUTING.md#security-issue-notifications) for more information.

## License

This library is licensed under the MIT-0 License. See the LICENSE file.

