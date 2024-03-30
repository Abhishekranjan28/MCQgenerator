import os
import json
import traceback
import pandas as pd
import streamlit as st
from langchain.callbacks import get_openai_callback
from src.mcqgenerator.MCQGenet import generate_evaluate_chain
from src.mcqgenerator.utils import read_file, get_table_data
import requests

# URL of the file on GitHub
github_file_url = 'https://raw.githubusercontent.com/username/repository/branch/path/to/file.json'

# Fetch the file content using requests
response = requests.get(github_file_url)

if response.status_code == 200:
    # Write the content fetched from GitHub to a local file
    with open('local_file.json', 'w') as f:
        f.write(response.text)
    print("File downloaded successfully.")
else:
    print("Failed to download file from GitHub.")

# Read the downloaded JSON file
with open('local_file.json', 'r') as f:
    RESPONSE_JSON = json.load(f)

# Create a form using Streamlit
with st.form('user.inputs'):
    st.title("MCQ Generator")
    # Upload file
    uploaded_file = st.file_uploader("Upload a PDF or text file")
    # Input fields
    mcq_count = st.number_input("No of MCQS", min_value=3, max_value=50)
    subject = st.text_input("Insert subject", max_chars=20)
    tone = st.text_input("Complexity level of questions", max_chars=20, placeholder='simple')
    button = st.form_submit_button("CREATE Question")

    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("Loading..."):
            try:
                text = read_file(uploaded_file)
                # Count tokens and cost of API call
                with get_openai_callback() as cb:
                    response = generate_evaluate_chain({
                        'text': text,
                        'number': mcq_count,
                        'subject': subject,
                        'tone': tone,
                        'response_json': json.dumps(RESPONSE_JSON)
                    })
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("Error")
            else:
                print(f"Total Tokens: {cb.total_tokens}")
                print(f"Prompt Tokens: {cb.prompt_tokens}")
                print(f"Completion Tokens: {cb.completion_tokens}")
                print(f"Total Cost: {cb.total_cost}")

                if isinstance(response, dict):
                    quiz = response.get('quiz')
                    if quiz is not None:
                        table_data = get_table_data(quiz)
                        if table_data is not None:
                            df = pd.DataFrame(table_data)
                            df.index = df.index + 1
                            st.table(df)
                            st.text_area(label="Review", value=response['review'])
                        else:
                            st.write(response)
