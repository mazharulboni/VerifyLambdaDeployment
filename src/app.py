import json
import boto3
from botocore.exceptions import ClientError

# Create a Lambda client
lambda_client = boto3.client('lambda')


def lambda_handler(event, context):
    list_of_functions = ['Function01', 'Function2']
    input_payload = {
        'key1': 'value1',
        'key2': 'value2'
    }

    for function in list_of_functions:
        response = invoke_function(function, input_payload)
        subject = 'Deployment Succeeded'.format()
        body = 'Response from {}: {}'.format(function, response)
        recipient = 'testdata.islam@gmail.com'
        send_email(subject, body, recipient)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
            # "location": ip.text.replace("\n", "")
        }),
    }


def invoke_function(function_name,input_payload ):

    # Define the input payload (if any)
    # input_payload = {
    #     'key1': 'value1',
    #     'key2': 'value2'
    # }

    # Invoke the Lambda function
    response = lambda_client.invoke(
        FunctionName=function_name,
        InvocationType='RequestResponse',  # Use 'Event' for asynchronous invocation
        Payload=json.dumps(input_payload)  # Optional: Pass input data as JSON string
    )

    # Extract and print the response
    response_payload = response['Payload'].read().decode('utf-8')
    print("Lambda Response:", response_payload)

    return  response_payload


def send_email(subject, body, recipient):
    # Create an SES client
    ses_client = boto3.client('ses', region_name='us-east-1')

    # Specify the sender's email address (must be verified in SES)
    sender = 'info@izaan.io'  # Replace with your verified email

    # Create the email message
    email_message = {
        'Subject': {'Data': subject},
        'Body': {'Text': {'Data': body}},
    }

    try:
        # Send the email
        response = ses_client.send_email(
            Source=sender,
            Destination={'ToAddresses': [recipient]},
            Message=email_message
        )

        print(f"Email sent to {recipient} with message ID: {response['MessageId']}")

    except ClientError as e:
        print(f"Email sending failed: {e.response['Error']['Message']}")

    # Example usage
    # subject = 'Hello from Amazon SES'
    # body = 'This is a test email sent using Amazon SES.'
    # recipient = 'abcd@gmail.com'