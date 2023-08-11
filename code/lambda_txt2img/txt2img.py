import json
import boto3
import random

runtime = boto3.client('runtime.sagemaker')


def lambda_handler(event, context):
    body = json.loads(event['body'])
    prompt = body.get("prompt", "random test image")
    endpoint_name = body.get("endpoint_name", "sdxl-1-0-jumpstart-2023-08-04-18-07-23-561")
    seed = body.get("seed", random.randint(1, 100))

    prompt_payload = {
        "seed": seed,
        "text_prompts": [{
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