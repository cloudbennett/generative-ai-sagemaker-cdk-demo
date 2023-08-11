import json
import boto3

runtime = boto3.client('runtime.sagemaker')


def lambda_handler(event, context):
    body = json.loads(event['body'])
    prompt = body['prompt']
    endpoint_name = body['endpoint_name']

    prompt_payload = {
        "text_prompts": [
        {
            "text": prompt,
            "weight": 1
        }
    ]}
    response = runtime.invoke_endpoint(EndpointName=endpoint_name,
                                            Body=json.dumps(prompt_payload),
                                            ContentType='application/json')
    response_body = json.loads(response['Body'].read())
    generated_image = response_body["artifacts"][0]["base64"]

    message = {"prompt": prompt, 'image': generated_image}
    return {
        "statusCode": 200,
        "body": json.dumps(message),
        "headers": {
            "Content-Type": "application/json"
        }
    }