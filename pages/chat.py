import streamlit as st
from streamlit_chat import message
import random
import replicate

def generate_chat_prompt(query, content):
    template = f"""

    You are a friendly AI assistant to help users know more about a product. The details of the product are provided in the <content> tag below

    <content>{content}</content>

    The user has askd the following question
    
    USER_QUESTION: {query}

    Answer the question as best as you can using the provided information and general knowledge

    """

    return template

if "product" not in st.session_state:
    st.error("PLEASE IDENFTIFY A PRODUCT FIRST BEFORE COMING TO CHAT")
else:
    st.header("GetAI bot - Gain Information about your product")
    st.markdown(f"Ask questions related to the identified product : {st.session_state['product']['product_name'].iloc[0]}")
    message("Hiiiiii!!, I am GetAI, your friendly assistant to answer all your questions related to your product😊 😊 😊!!!!")
    if "past" not in st.session_state:
        st.session_state['past'] = []
    if "generated" not in st.session_state:
        st.session_state["generated"] = []
    if "input_message_key" not in st.session_state:
        st.session_state["input_message_key"] = str(random.random())
    chat_container = st.container()
    user_input = st.text_input("Type your question here.", key=st.session_state["input_message_key"])
    if st.button("Send"):
        # try:
        prompt = generate_chat_prompt(user_input, st.session_state["product"]["details"])
        
        response = ""
        for event in replicate.stream("snowflake/snowflake-arctic-instruct",
                        input={"prompt": prompt,
                                "temperature": 0.2
                                }):
            response += str(event)

        st.session_state["past"].append(user_input)
        st.session_state["generated"].append(response)
        st.session_state["input_message_key"] = str(random.random())
        st.rerun()
    if st.session_state["generated"]:
            with chat_container:
                for i in range(len(st.session_state["generated"])):
                    message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")
                    message(st.session_state["generated"][i], key=str(i))
