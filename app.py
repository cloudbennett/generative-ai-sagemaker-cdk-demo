#!/usr/bin/env python3
import aws_cdk as cdk

from stack.generative_ai_vpc_network_stack import GenerativeAiVpcNetworkStack
from stack.generative_ai_demo_web_stack import GenerativeAiDemoWebStack

import boto3

region_name = boto3.Session().region_name
env={"region": region_name}

#Text to Image model parameters
TXT2IMG_MODEL_ID = "model-txt2img-stabilityai-stable-diffusion-v2-1-base"
TXT2IMG_INFERENCE_INSTANCE_TYPE = "ml.g4dn.4xlarge" 
TXT2IMG_MODEL_TASK_TYPE = "txt2img"


app = cdk.App()

network_stack = GenerativeAiVpcNetworkStack(app, "GenerativeAiVpcNetworkStack", env=env)
GenerativeAiDemoWebStack(app, "GenerativeAiDemoWebStack", vpc=network_stack.vpc, env=env)


app.synth()
