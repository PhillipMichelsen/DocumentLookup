import pandas as pd
import requests
import streamlit as st
import re

from app.schemas import GeneratePresignedURLUploadRequest, GeneratePresignedURLUploadResponse, GetFilesRequest, GetFilesResponse, AnswerQuestionRequest, AnswerQuestionResponse

with st.sidebar:
    uploaded_files = st.file_uploader("Choose files to upload (optional)", accept_multiple_files=True)

    # Button to initiate the file upload
    if st.button("Upload Files"):
        # Requesting presigned URLs for all files first
        presigned_urls = []
        for uploaded_file in uploaded_files:
            presigned_url_response = requests.post("http://api-gateway-core-service:8000/core-jobs/generate-presigned-url-upload",
                                                   json=GeneratePresignedURLUploadRequest(filename=uploaded_file.name).model_dump())
            presigned_url = GeneratePresignedURLUploadResponse.model_validate(presigned_url_response.json()).presigned_url_upload
            presigned_urls.append((uploaded_file, presigned_url))

        # Uploading files to the presigned URLs
        for uploaded_file, presigned_url in presigned_urls:
            requests.put(presigned_url, data=uploaded_file.read())
            st.success(f"File {uploaded_file.name} uploaded successfully")

    if st.button("Get Files"):
        # Make the API call
        get_files_response = requests.post("http://api-gateway-core-service:8000/core-jobs/get-files", json=GetFilesRequest(
            document_id=['']
        ).model_dump())
        print(f'Request made to http://api-gateway-core-service:8000/core-jobs/get-files')

        response_data = GetFilesResponse.model_validate(get_files_response.json())

        files_df = pd.DataFrame({
            'Document ID': response_data.document_id,
            # 'Filename': response_data.filename,
            'File Status': response_data.file_status
        })

        files_df = files_df.sort_values(by=['Document ID'])

        # Display the table
        st.write(files_df)

query = st.text_input("Enter your query:")

# Button to initiate the request
if st.button("Get answer!"):
    # Build the request object
    request_data = AnswerQuestionRequest(
        user_query=query,
        top_n=10,
        text_type='paragraph',
        document_id='',
    )

    # Make the API call
    response = requests.post("http://api-gateway-core-service:8000/core-jobs/answer-question", json=request_data.model_dump())
    print(f'Request made to http://api-gateway-core-service:8000/core-jobs/answer-question with data: {request_data.model_dump()}')

    response_data = AnswerQuestionResponse.model_validate(response.json())

    def make_citations_blue(text):
        return re.sub(r'(\[\d+\])', r'<span style="color:#B9B4C7;">\1</span>', text)

    # Modify the response text using the function
    blue_citations_text = make_citations_blue(response_data.chat_completion)
    # Render the modified HTML in Streamlit
    st.markdown("**Response:**")
    st.markdown(blue_citations_text, unsafe_allow_html=True)

    st.markdown("**Context:**")
    for i, context in enumerate(response_data.context):
        st.markdown(f'<span style="font-size: 10px;">[{i + 1}] {context}</span>', unsafe_allow_html=True)



