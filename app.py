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
    page_title="S3 ファイルアップローダー",
    page_icon="📤",
    layout="wide"
)

# Title and description
st.title("📤 S3 ファイルアップローダー")
st.markdown("""
このアプリでAWS S3にファイルをアップロードし、URLを取得できます。
ファイルをドラッグ＆ドロップするか、下のアップロードボタンをクリックしてください。
""")

# File naming options
st.subheader("ファイル名の設定")
naming_option = st.radio(
    "ファイル名の設定方法を選択してください：",
    ["元のファイル名を使用", "ランダムな名前を使用", "カスタム名を使用"]
)

# File uploader with multiple files support
uploaded_files = st.file_uploader(
    "アップロードするファイルを選択",
    type=None,
    accept_multiple_files=True
)

if uploaded_files:
    # Display selected files
    st.subheader("選択されたファイル")
    for file in uploaded_files:
        st.write(f"- {file.name} ({file.size / 1024:.1f} KB)")

    # Custom filename prefix
    custom_prefix = ""
    if naming_option == "カスタム名を使用":
        custom_prefix = st.text_input("ファイル名のプレフィックスを入力してください（拡張子なし）：")
        if not custom_prefix:
            st.warning("プレフィックスを入力してください")
            custom_prefix = None

    # Upload button
    if st.button("ファイルをアップロード", type="primary"):
        uploaded_urls = []
        
        for uploaded_file in uploaded_files:
            try:
                file_extension = os.path.splitext(uploaded_file.name)[1]
                
                # Generate filename based on selected option
                if naming_option == "元のファイル名を使用":
                    filename = uploaded_file.name
                elif naming_option == "ランダムな名前を使用":
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
            st.success(f"{len(uploaded_urls)}個のファイルのアップロードが完了しました！ 🎉")
            
            # Display URLs in a table
            st.subheader("アップロードされたファイルとURL")
            for original_name, url in uploaded_urls:
                col1, col2 = st.columns([1, 2])
                with col1:
                    st.write(original_name)
                with col2:
                    st.code(url, language=None)
                    if st.button(f"{original_name}のURLをコピー", key=f"copy_{original_name}"):
                        st.write("URLをクリップボードにコピーしました！")
