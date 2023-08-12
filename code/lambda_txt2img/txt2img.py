import json
import boto3
import random

runtime = boto3.client('runtime.sagemaker')


def lambda_handler(event, context):
    body = json.loads(event['body'])
    prompt = body.get("prompt", {"text": "random test image"})
    endpoint_name = body.get("endpoint_name", "sdxl-1-0-jumpstart-2023-08-04-18-07-23-561")
    seed = random.randint(1, 100)
    if body.get("seed"):
        seed = body.get("seed")
    steps = body.get("steps", 50)
    width = body.get("width", 1024)
    height = body.get("height", 1024)
    cfg_scale = body.get("cfg_scale", 7)
    samples = body.get("samples", 1)
    style_preset = body.get("style_preset", "enhance")

    print(prompt)
    prompt_payload = {
        "steps": steps,
        "width": width,
        "height": height,
        "cfg_scale": cfg_scale,
        "samples": samples,
        "style_preset": style_preset,
        "seed": seed,
        "text_prompts": prompt
    }
    prompt_payload_json = json.dumps(prompt_payload)
    print(prompt_payload_json)
    response = runtime.invoke_endpoint(EndpointName=endpoint_name,
                                            Body=prompt_payload_json,
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