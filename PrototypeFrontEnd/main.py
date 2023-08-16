import streamlit as st
import requests
from pydantic import BaseModel
from typing import List


class RetrieveQueryContextRequest(BaseModel):
    text: List[str]
    query: str
    top_n: int = 20
    type_filter: str = "div"
    document_id: str = None


class RetrieveQueryContextResponse(BaseModel):
    ranked_entries: List[str]


# Upload multiple files
uploaded_files = st.file_uploader("Choose files to upload (optional)", accept_multiple_files=True)
for uploaded_file in uploaded_files:
    # Request a presigned URL for each uploaded file
    presigned_url_response = requests.post("http://localhost:8000/utility-jobs/get-presigned-url-upload", json={"filename": uploaded_file.name})
    presigned_url = presigned_url_response.json().get("presigned_url")

    # Upload the file to the presigned URL
    requests.put(presigned_url, data=uploaded_file.read())
    st.success(f"File {uploaded_file.name} uploaded successfully")

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
    response = requests.post("http://localhost:8000/core-jobs/retrieve-query-context", json=request_data.dict())

    # Display the results
    response_data = RetrieveQueryContextResponse(**response.json())
    st.write("Results:")
    for entry in response_data.ranked_entries:
        st.markdown(f"- {entry}")
