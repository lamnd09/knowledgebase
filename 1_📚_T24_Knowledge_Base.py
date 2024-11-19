import boto3
import streamlit as st
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

# Access AWS credentials and region
aws_access_key_id = os.getenv("aws_access_key_id")
aws_secret_access_key = os.getenv("aws_secret_access_key")
region_name = os.getenv("region_name")

knowledgebase_id = os.getenv("KNOWLEDGEBASE_ID")
model_id = os.getenv("MODEL_ID")

st.set_page_config(layout="wide")
st.sidebar.image("logo.png")  # Adjust width as needed
st.subheader('ITS3 - T24 Knowledge Assistant', divider='rainbow')


# Use a unique key for chat history on this page
if 'chat_history_assistant' not in st.session_state:
    st.session_state.chat_history_assistant = []

for message in st.session_state.chat_history_assistant:
    with st.chat_message(message['role']):
        st.markdown(message['text'])

bedrockClient = boto3.client('bedrock-agent-runtime', 
                             aws_access_key_id=aws_access_key_id,
                             aws_secret_access_key=aws_secret_access_key,
                             region_name=region_name)

def getAnswers(questions):
    knowledgeBaseResponse = bedrockClient.retrieve_and_generate(
        input={'text': questions},
        retrieveAndGenerateConfiguration={
            'knowledgeBaseConfiguration': {
                'knowledgeBaseId': knowledgebase_id,
                'modelArn': model_id
            },
            'type': 'KNOWLEDGE_BASE'
        })
    return knowledgeBaseResponse



# Display the logo at the top of the page
# Display the logo at the top of the sidebar
#st.add_logo("logo.png", width=100)  # Adjust the width as needed

questions = st.chat_input('Enter your questions here...')
if questions:
    with st.chat_message('user'):
        st.markdown(questions)
    st.session_state.chat_history_assistant.append({"role": 'user', "text": questions})

    response = getAnswers(questions)
    answer = response['output']['text']

    with st.chat_message('assistant'):
        st.markdown(answer)
    st.session_state.chat_history_assistant.append({"role": 'assistant', "text": answer})

    # Check if citations exist and contain references
    if response.get('citations') and len(response['citations']) > 0 and \
       response['citations'][0].get('retrievedReferences') and len(response['citations'][0]['retrievedReferences']) > 0:
        context = response['citations'][0]['retrievedReferences'][0]['content']['text']
        doc_url = response['citations'][0]['retrievedReferences'][0]['location']['s3Location']['uri']
        
        # Show context and document source
        st.markdown(f"<span style='color:#FFDA33'>Context used: </span>{context}", unsafe_allow_html=True)
        st.markdown(f"<span style='color:#FFDA33'>Source Document: </span>{doc_url}", unsafe_allow_html=True)
    else:
        st.markdown(f"<span style='color:red'>No Context</span>", unsafe_allow_html=True)
