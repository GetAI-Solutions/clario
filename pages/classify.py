import streamlit as st
import numpy as np
from PIL import Image
import numpy as np
import pandas as pd
import cv2
from pyzbar import pyzbar
import replicate

import os
os.environ["REPLICATE_API_TOKEN"] = st.secrets["REPLICATE_API_TOKEN"]

if "data" not in st.session_state:
    st.session_state["data"] = pd.read_csv("data.csv")

def generate_prompt(content):
    template = f"""

    You are a friendly AI assistant to help users know more about a product. The dteails of the product are provided in the <content> tag below

    <content>{content}</content>

    Provide a summary of the product for the user

    """

    return template


def scan_barcode_from_image(image):
    image_np = np.array(image.convert('RGB'))
    barcodes = pyzbar.decode(image_np)
    for barcode in barcodes:
        x, y, w, h = barcode.rect
        barcode_data = barcode.data.decode('utf-8')
        barcode_type = barcode.type
        text = f'{barcode_data} ({barcode_type})'
        cv2.rectangle(image_np, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.putText(image_np, text, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
    return Image.fromarray(image_np), barcodes



def home():
    st.header(f"A demo of using GetAI to scan a barcode and get product information")

    st.subheader("This serves as a proof of concept and will require additional training and data for a more efficient model")

    st.subheader("To test the model, select any of the options below to select a barcode")

def clf():
    img_f = st.file_uploader(f"Upload barcode", type=["png", "jpg"])

    if img_f is not None:
        st.image(img_f, caption='Uploaded Image', use_column_width=True)
        image = Image.open(img_f)
        st.success("Image Uploaded.....")
        st.info(f"Extracting Information from the Barcode.....Please wait")

        scanned_image, barcodes = scan_barcode_from_image(image)
        st.image(scanned_image, caption='Scanned Image', use_column_width=True)
        if barcodes:
            st.write("Found barcodes:")
            for barcode in barcodes:
                st.write(f"- Data: {barcode.data.decode('utf-8')}, Type: {barcode.type}")
                return barcode.data.decode('utf-8')
        else:
            st.error("No barcode detected")
        

def real_time():
    cam_input = st.camera_input(label="Camera")
    if cam_input:
        st.image(cam_input)
        with open("cam_img.jpeg", mode='wb') as f:
            f.write(cam_input.getbuffer())
        st.info(f"Extracting Information from the Barcode.....Please wait")

        image = Image.open("cam_img.jpeg")
        scanned_image, barcodes = scan_barcode_from_image(image)
        st.image(scanned_image, caption='Scanned Image', use_column_width=True)
        if barcodes:
            st.write("Found barcodes:")
            for barcode in barcodes:
                st.write(f"- Data: {barcode.data.decode('utf-8')}, Type: {barcode.type}")
                return barcode.data.decode('utf-8')
        else:
            st.error("No barcode detected")
        

def run_selection():
    sub_sel = st.sidebar.radio("Select Option", ["Info", "Classify local Image", "Realtime Classification"])
    barcode_d = None
    if sub_sel == "Info":
        home()
    elif sub_sel == "Classify local Image":
        barcode_d = clf()
    elif sub_sel == "Realtime Classification":
        barcode_d = real_time()
    
    if barcode_d != None:
        content = st.session_state["data"][st.session_state["data"]["product_code"]== int(barcode_d)]
        st.session_state["product"] = content

        st.header(f'Identified product is: {content["product_name"].iloc[0]}')
        prompt = generate_prompt(content["details"])

        response = ""

        for event in replicate.stream("snowflake/snowflake-arctic-instruct",
                        input={"prompt": prompt,
                                "temperature": 0.2
                                }):
            response += str(event)
        
        st.write(response)
        st.info("You can now proceed to chat page to gain more information about the identified product")

st.title("Get AI Demo")

st.sidebar.title("Options")
run_selection()