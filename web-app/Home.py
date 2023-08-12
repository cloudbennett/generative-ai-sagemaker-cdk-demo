import streamlit as st
import os
import streamlit as st
import requests
import json
import matplotlib.pyplot as plt
import numpy as np
import time
import base64
from io import BytesIO
from configs import *


from PIL import Image
image = Image.open("./sagemaker.png")
st.image(image, width=200)

version = os.environ.get("WEB_VERSION", "0.1")

st.header("Movie Poster Generation")
st.markdown("Powered by Amazon Sagemaker using Stable DiffusionXL 1.0")

text_prompts = st.text_area("Describe your movie poster:","""movie poster with dwayne johnson with city skyline in chaos futuristic vehicle zooms  """)
negative_prompt = st.text_area("Add parameter to exclude from generated poster:","""low resolution""")
seed_value=st.text_input("Enter seed value(Numeric value to initialize picture generation):","""1""")


StylePreset = st.selectbox(
    'Select a style preset from the list',
    ['digital-art','cinematic','anime','comic-book','fantasy-art','modeling-compound','neon-punk','origami','3d-model','analog-film']
    )

with st.spinner("Retrieving configurations..."):

    all_configs_loaded = False

    while not all_configs_loaded:
        try:
            api_endpoint = get_parameter(key_txt2img_api_endpoint)
            all_configs_loaded = True
        except:
            time.sleep(5)
        
        #api_endpoint = "https://ceiapp4n72.execute-api.us-east-1.amazonaws.com/prod"
        endpoint_name = "sdxl-1-0-jumpstart-2023-08-04-18-07-23-561"


#st.button ("Generate image")

if st.button("Generate image"):
    if text_prompts == "":      
        st.error("Please enter image description!")
    else:
        with st.spinner("Wait for it..."):
            try:
                #r = requests.post(api_endpoint,json={"prompt":text_prompts,"endpoint_name":endpoint_name,"model_type":"1.0"},timeout=180)
                r = requests.post(api_endpoint,
                    json={
                    "seed": seed_value,
                    "style_preset":StylePreset,

                    "prompt": [
                        { 
                            "text": text_prompts,
                            "weight": 1
                        },
                        { 
                            "text": negative_prompt,
                            "weight": -1
                        }
                        ],
                    "endpoint_name": endpoint_name
                    }, timeout=180)

                data = r.json()
                image_array = data["image"]
                encoded_image = base64.b64decode(image_array)
                st.image(encoded_image, caption = "Movie Poster")
                

            except requests.exceptions.ConnectionError as errc:
                st.error("Error Connecting:",errc)
                
            except requests.exceptions.HTTPError as errh:
                st.error("Http Error:",errh)
                
            except requests.exceptions.Timeout as errt:
                st.error("Timeout Error:",errt)    
                
            except requests.exceptions.RequestException as err:
                st.error("OOps: Something Else",err)                
                
        st.success("Done!")
