import os
import boto3
from botocore.config import Config  # Make sure Config is imported!
from botocore.exceptions import NoCredentialsError, ClientError
from fastapi import HTTPException, status
from dotenv import load_dotenv
load_dotenv()
# 1. Fetch the environment variables first
AWS_REGION = os.getenv("AWS_REGION", "ap-southeast-2")
BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME", "foodsnapai-image-bucket")

# 2. Define the S3 Config explicitly for Signature Version 4
s3_config = Config(
    region_name=AWS_REGION,
    signature_version="s3v4"
)

# 3. Initialize the S3 client WITH the config attached
s3_client = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=AWS_REGION,
    config=s3_config  # <-- THIS WAS MISSING
)

def upload_file_to_s3(file_obj, bucket_name: str, object_name: str, content_type: str) -> str:
    """
    Uploads a file object directly to an S3 bucket and returns its public URL.
    """
    print("from upload file to s3 function")
    try:
        s3_client.upload_fileobj(
            file_obj,
            bucket_name,
            object_name,
            ExtraArgs={"ContentType": content_type}
        )
        
        # Construct the file URL (Sydney format matches standard virtual-host addressing)
        file_url = f"https://{bucket_name}.s3.{AWS_REGION}.amazonaws.com/{object_name}"
        return file_url

    except (NoCredentialsError, ClientError) as e:
        print(f"AWS S3 Upload Error: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AWS S3 Upload Error: {str(e)}"
        )