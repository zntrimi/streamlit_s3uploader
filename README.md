# S3 File Uploader

A Streamlit application that allows users to upload files to AWS S3 and get public URLs for those files.

## Features

- Drag and drop file upload
- Automatic unique filename generation
- Public URL generation
- Copy to clipboard functionality
- User-friendly interface

## Prerequisites

- Python 3.7+
- AWS Account with S3 access
- AWS S3 bucket with public access enabled

## Setup

1. Clone this repository
2. Install the required packages:
   ```bash
   pip install -r requirements.txt
   ```
3. Configure your AWS credentials in the `.env` file:
   - AWS_ACCESS_KEY_ID
   - AWS_SECRET_ACCESS_KEY
   - AWS_DEFAULT_REGION
   - S3_BUCKET_NAME

## Running the Application

To run the application, use the following command:

```bash
streamlit run app.py
```

## Security Note

Make sure to:
1. Never commit your `.env` file to version control
2. Use appropriate IAM permissions for your AWS credentials
3. Configure your S3 bucket's CORS settings if needed
4. Consider implementing file size limits and type restrictions

## License

MIT License # file2s3-streamlit
# streamlit_s3uploader
