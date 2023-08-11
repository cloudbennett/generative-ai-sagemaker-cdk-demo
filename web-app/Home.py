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

from PIL import Image
image = Image.open("./sagemaker.png")
st.image(image, width=200)

version = os.environ.get("WEB_VERSION", "0.1")

st.header(f"Generative AI Hackathon Demo (Version)")
st.markdown("Generative AI demo using Stable DiffusionXL 1.0")

text_prompts = st.text_area("Input Image description:")
negative_prompt = st.text_area("Input negative prompt description")
seed_value=st.text_input("Enter seed value:")


StylePreset = st.selectbox(
    'Select a style preset from the list',
    ['cinematic','anime','comic-book','digital-art','fantasy-art','modeling-compound','neon-punk','origami','3d-model','analog-film']
    )
with st.spinner("Retrieving configurations..."):

        
        api_endpoint = " https://6d8u4vdrz4.execute-api.us-east-1.amazonaws.com/prod"
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