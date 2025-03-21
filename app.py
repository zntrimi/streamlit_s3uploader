import streamlit as st
import boto3
import os
from dotenv import load_dotenv
import uuid
from datetime import datetime

# Load environment variables
load_dotenv()

# Configure AWS credentials
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_DEFAULT_REGION')
)

# Set page config
st.set_page_config(
    page_title="S3 File Uploader",
    page_icon="📤",
    layout="wide"
)

# Title and description
st.title("📤 S3 File Uploader")
st.markdown("""
This app allows you to upload files to AWS S3 and get their URLs.
Simply drag and drop your files or click the upload button below.
""")

# File naming options
st.subheader("File Naming Options")
naming_option = st.radio(
    "Choose how to name your files:",
    ["Use original filename", "Use random filename", "Custom filename"]
)

# File uploader with multiple files support
uploaded_files = st.file_uploader(
    "Choose files to upload",
    type=None,
    accept_multiple_files=True
)

if uploaded_files:
    # Display selected files
    st.subheader("Selected Files")
    for file in uploaded_files:
        st.write(f"- {file.name} ({file.size / 1024:.1f} KB)")

    # Custom filename prefix (if custom naming is selected)
    custom_prefix = ""
    if naming_option == "Custom filename":
        custom_prefix = st.text_input("Enter filename prefix (without extension):")
        if not custom_prefix:
            st.warning("Please enter a filename prefix")
            custom_prefix = None

    # Upload button
    if st.button("Upload Files", type="primary"):
        uploaded_urls = []
        
        for uploaded_file in uploaded_files:
            try:
                file_extension = os.path.splitext(uploaded_file.name)[1]
                
                # Generate filename based on selected option
                if naming_option == "Use original filename":
                    filename = uploaded_file.name
                elif naming_option == "Use random filename":
                    filename = f"{uuid.uuid4()}{file_extension}"
                else:  # Custom filename
                    if custom_prefix:
                        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                        filename = f"{custom_prefix}_{timestamp}{file_extension}"
                    else:
                        continue
                
                # Upload file to S3 in the randfile directory
                bucket_name = os.getenv('S3_BUCKET_NAME')
                s3_path = f"randfile/{filename}"
                
                # Upload without ACL
                s3_client.upload_fileobj(
                    uploaded_file,
                    bucket_name,
                    s3_path
                )
                
                # Generate URL
                url = f"https://{bucket_name}.s3.{os.getenv('AWS_DEFAULT_REGION')}.amazonaws.com/{s3_path}"
                uploaded_urls.append((uploaded_file.name, url))
                
            except Exception as e:
                st.error(f"Error uploading {uploaded_file.name}: {str(e)}")
        
        if uploaded_urls:
            st.success(f"Successfully uploaded {len(uploaded_urls)} file(s)! 🎉")
            
            # Display URLs in a table
            st.subheader("Uploaded Files and URLs")
            for original_name, url in uploaded_urls:
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.write(original_name)
                with col2:
                    st.code(url, language=None)
                    if st.button(f"Copy URL for {original_name}", key=f"copy_{original_name}"):
                        st.write("URL copied to clipboard!")

# Add some helpful information
with st.expander("ℹ️ How to use"):
    st.markdown("""
    1. Select one or more files using the upload button above
    2. Choose how you want to name your files:
       - Use original filename: Keeps the original file names
       - Use random filename: Generates random UUIDs for the file names
       - Custom filename: Enter a prefix for your files (timestamp will be added automatically)
    3. Click the "Upload Files" button
    4. Copy the generated URLs
    5. Share the URLs with others to access your files
    """)

# Footer
st.markdown("---")
st.markdown("Made with ❤️ using Streamlit and AWS S3") 