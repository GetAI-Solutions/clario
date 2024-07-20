import streamlit as st
import pandas as pd

if __name__ == "__main__":

    st.title("GetAI DEMO")

    st.session_state["data"] = pd.read_csv("data.csv")

    st.write('''.''')

st.title("How to Test Demo")
st.subheader("1. Select the classification")
st.subheader("2. Select classification method: ")
st.subheader("4. Download the selected image to device then go back to app")
st.subheader("5. Upload the just downloaded image and the model predicts")

#st.title("How to Use")
#st.subheader("1. Select what you want to classify (Livestock or Crop)")
#st.subheader("2. Select classification method: ")
#st.markdown("Classify image option: For pre-existing image already on device")
#st.markdown("Realtime-classification option: For pre-existing image already on device")
#st.subheader("3. Upload file if classify-image option was selected or take picture with camera if realtime-classification option was selected")