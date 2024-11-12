import boto3
import streamlit as st
from dotenv import load_dotenv
import os
import json
from PyPDF2 import PdfReader
import xml.etree.ElementTree as ET

# Load environment variables from .env file
load_dotenv()

# Set up Streamlit page
st.set_page_config(layout="wide")
st.sidebar.image("logo.png")  # Adjust width as needed

st.subheader('Ask your documents', divider='rainbow')

# Access AWS credentials and region
aws_access_key_id = os.getenv("aws_access_key_id")
aws_secret_access_key = os.getenv("aws_secret_access_key")
region_name = os.getenv("region_name")
model_id = os.getenv("MODEL_ID")  # Set this to Claude's ARN

# Set up the Bedrock client
bedrockClient = boto3.client('bedrock-runtime', 
                             aws_access_key_id=aws_access_key_id,
                             aws_secret_access_key=aws_secret_access_key,
                             region_name=region_name)

# Initialize chat history and document content in session state
if 'chat_history_doc' not in st.session_state:
    st.session_state.chat_history_doc = []
if 'document_content' not in st.session_state:
    st.session_state.document_content = ""

# Upload and process multiple documents
uploaded_files = st.file_uploader("Upload documents (PDF or XML)", type=['pdf', 'xml'], accept_multiple_files=True)
if uploaded_files:
    combined_content = ""
    for uploaded_file in uploaded_files:
        if uploaded_file.type == "application/pdf":
            # Process PDF file
            pdf_reader = PdfReader(uploaded_file)
            text_content = ""
            for page in pdf_reader.pages:
                text_content += page.extract_text() + "\n"
            combined_content += text_content
        elif uploaded_file.type == "text/xml":
            # Process XML file
            xml_tree = ET.parse(uploaded_file)
            root = xml_tree.getroot()
            xml_content = ET.tostring(root, encoding='utf-8').decode('utf-8')
            combined_content += xml_content

    # Store the combined content in the session state
    st.session_state.document_content = combined_content
    st.success("Documents content loaded for Q&A.")

# Function to generate answers based on document context
def getAnswers(question, document_content):
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
                            "text": f"Based on this document content:\n{document_content}\nAnswer this question:\n{question}"
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

# Display chat interface only if document content is available
if st.session_state.document_content:
    questions = st.chat_input("Ask a question about the uploaded documents...")
    if questions:
        with st.chat_message('user'):
            st.markdown(questions)
        st.session_state.chat_history_doc.append({"role": 'user', "text": questions})

        # Generate response based on document content
        response_text = getAnswers(questions, st.session_state.document_content)

        with st.chat_message('assistant'):
            st.markdown(response_text)
        st.session_state.chat_history_doc.append({"role": 'assistant', "text": response_text})

    # Display chat history
    for message in st.session_state.chat_history_doc:
        with st.chat_message(message['role']):
            st.markdown(message['text'])
else:
    st.info("Please upload documents to enable Q&A.")
