import boto3
from botocore.config import Config
from botocore.exceptions import ClientError, NoCredentialsError
from fastapi import HTTPException, status
from app.core.config import settings

_s3_config = Config(
    region_name=settings.aws_region,
    signature_version="s3v4",
)

s3_client = boto3.client(
    "s3",
    aws_access_key_id=settings.aws_access_key_id,
    aws_secret_access_key=settings.aws_secret_access_key,
    region_name=settings.aws_region,
    config=_s3_config,
)


def upload_file_to_s3(
    file_obj,
    object_name: str,
    content_type: str,
    bucket_name: str | None = None,
) -> str:
    bucket = bucket_name or settings.aws_bucket_name
    try:
        s3_client.upload_fileobj(
            file_obj,
            bucket,
            object_name,
            ExtraArgs={"ContentType": content_type},
        )
        file_url = f"https://{bucket}.s3.{settings.aws_region}.amazonaws.com/{object_name}"
        return file_url
    except (NoCredentialsError, ClientError) as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"AWS S3 Upload Error: {str(e)}",
        )


def download_file_from_s3(
    object_name: str,
    bucket_name: str | None = None,
) -> bytes:
    bucket = bucket_name or settings.aws_bucket_name
    try:
        response = s3_client.get_object(
            Bucket=bucket,
            Key=object_name,
        )
        return response["Body"].read()
    except Exception as e:
        raise RuntimeError(f"Failed to fetch image from S3: {e}")
