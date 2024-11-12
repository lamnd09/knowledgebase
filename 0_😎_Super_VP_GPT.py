import boto3
import streamlit as st
from dotenv import load_dotenv
import os
import json
from streamlit_extras.app_logo import add_logo

# Load environment variables from .env file
load_dotenv()


# Access AWS credentials and region
aws_access_key_id = os.getenv("aws_access_key_id")
aws_secret_access_key = os.getenv("aws_secret_access_key")
region_name = os.getenv("region_name")
model_id = os.getenv("MODEL_ID")  # Set this to Claude's ARN

st.set_page_config(layout="wide")
st.sidebar.image("logo.png")  # Adjust width as needed

st.subheader('Ask Super VP GPT any question!', divider='rainbow')

# Use a unique key for chat history on this page
if 'chat_history_vp' not in st.session_state:
    st.session_state.chat_history_vp = []

for message in st.session_state.chat_history_vp:
    with st.chat_message(message['role']):
        st.markdown(message['text'])

# Set up the Bedrock client
bedrockClient = boto3.client('bedrock-runtime', 
                             aws_access_key_id=aws_access_key_id,
                             aws_secret_access_key=aws_secret_access_key,
                             region_name=region_name)

def getAnswers(question):
    payload = {
        "modelId": model_id,
        "contentType": "application/json",
        "accept": "application/json",
        "body": json.dumps({
            "anthropic_version": "bedrock-2023-05-31",
            "max_tokens": 1000,
            "messages": [
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": question
                        }
                    ]
                }
            ]
        })
    }

    # Call Bedrock model
    response = bedrockClient.invoke_model(
        modelId=payload["modelId"],
        contentType=payload["contentType"],
        accept=payload["accept"],
        body=payload["body"]
    )

    # Read and parse the StreamingBody response
    response_body = response['body'].read().decode('utf-8')
    response_payload = json.loads(response_body)

    # Extract and return the text from the response content
    if 'content' in response_payload and len(response_payload['content']) > 0:
        return response_payload['content'][0]['text']
    else:
        return "Error: No valid content found in model response."

questions = st.chat_input('Enter your questions here...')
if questions:
    with st.chat_message('user'):
        st.markdown(questions)
    st.session_state.chat_history_vp.append({"role": 'user', "text": questions})

    response_text = getAnswers(questions)

    with st.chat_message('assistant'):
        st.markdown(response_text)
    st.session_state.chat_history_vp.append({"role": 'assistant', "text": response_text})

    # Indicate no context or document source as it’s not being used here
    # st.markdown(f"<span style='color:red'>No Context Retrieved</span>", unsafe_allow_html=True)
