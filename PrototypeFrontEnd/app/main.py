import pandas as pd
import requests
import streamlit as st

from app.schemas import RetrieveQueryContextRequest, RetrieveQueryContextResponse, GetFilesRequest, GetFilesResponse

with st.sidebar:
    uploaded_files = st.file_uploader("Choose files to upload (optional)", accept_multiple_files=True)

    # Button to initiate the file upload
    if st.button("Upload Files"):
        # Requesting presigned URLs for all files first
        presigned_urls = []
        for uploaded_file in uploaded_files:
            presigned_url_response = requests.post("http://api-gateway-core-service:8000/utility-tasks/generate-presigned-url-upload",
                                                   json={"filename": uploaded_file.name})
            presigned_url = presigned_url_response.json().get("presigned_url")
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
top_n = st.number_input("Top N:", min_value=1, max_value=50, value=20)
type_filter = st.radio("Type Filter:", options=["paragraph", "div"])
document_id = st.text_input("Document ID:")

# Button to initiate the request
if st.button("Retrieve Query Context"):
    # Build the request object
    request_data = RetrieveQueryContextRequest(
        text=[query],
        query=query,
        top_n=top_n,
        type_filter=type_filter,
        document_id=document_id,
    )

    # Make the API call
    response = requests.post("http://api-gateway-core-service:8000/core-jobs/retrieve-query-context", json=request_data.model_dump())
    print(f'Request made to http://api-gateway-core-service:8000/core-jobs/retrieve-query-context with data: {request_data.model_dump()}')

    # Display the results
    response_data = RetrieveQueryContextResponse(**response.json())
    st.write("Results:")
    for entry in response_data.ranked_entries:
        st.markdown(f"- {entry}")
