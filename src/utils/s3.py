import os
from tempfile import NamedTemporaryFile
from typing import List

import boto3
from botocore.config import Config
from fastapi import UploadFile

from src.schemas.basic import UploadedFile

# Check if using MinIO or AWS S3
IS_MINIO = os.getenv('S3_PROVIDER', 'aws').lower() == 'minio'
S3_ENDPOINT_URL = os.getenv('S3_ENDPOINT_URL')  # e.g., 'http://localhost:9000' for MinIO

ACCESS_KEY_NAME = "AWS_ACCESS_KEY_ID" if not IS_MINIO else "MINIO_ROOT_USER"
SECRET_KEY_NAME = "AWS_SECRET_ACCESS_KEY" if not IS_MINIO else "MINIO_ROOT_PASSWORD"

MINIO_DNS_URL = os.getenv('MINIO_DNS_URL')

# Configure S3 client with support for both AWS S3 and MinIO
s3_config = {
    'aws_access_key_id': os.getenv(ACCESS_KEY_NAME),
    'aws_secret_access_key': os.getenv(SECRET_KEY_NAME),
    'config': Config(s3={"use_accelerate_endpoint": False})
}

# Add endpoint URL for MinIO or custom S3-compatible services
if S3_ENDPOINT_URL:
    s3_config['endpoint_url'] = S3_ENDPOINT_URL

# Only add region for AWS S3 (MinIO doesn't require it)
if not IS_MINIO:
    s3_config['region_name'] = os.getenv('AWS_REGION')

s3 = boto3.client('s3', **s3_config)


def s3_url_to_cloudfront(url):
    # Only apply CloudFront transformation for AWS S3
    if IS_MINIO or not os.getenv('AWS_CLOUDFRONT_DOMAIN'):
        return url
    s3_domain = f"{os.getenv('AWS_S3_BUCKET')}.s3.{os.getenv('AWS_REGION')}.amazonaws.com"
    return url.replace(s3_domain, os.getenv('AWS_CLOUDFRONT_DOMAIN'))


def upload_local_to_s3(local_path, s3_path, content_type):
    """
    Upload a local file to S3 or MinIO.

    Args:
        local_path: Path to the local file
        s3_path: Destination path in the S3/MinIO bucket
        content_type: MIME type of the file

    Returns:
        Public URL of the uploaded file (CloudFront URL for AWS, direct URL for MinIO)
    """
    bucket_name = str(os.environ.get('AWS_S3_BUCKET'))
    s3.upload_file(local_path, bucket_name, s3_path, ExtraArgs={'ContentType': content_type})

    # Generate appropriate URL based on provider
    if IS_MINIO and MINIO_DNS_URL:
        # MinIO URL format
        public_url = f"{MINIO_DNS_URL}/{bucket_name}/{s3_path}"
    else:
        # AWS S3 URL format
        public_url = f"https://{bucket_name}.s3.{os.getenv('AWS_REGION')}.amazonaws.com/{s3_path}"

    return s3_url_to_cloudfront(public_url)


def save_upload_files_locally(files: List[UploadFile] | UploadFile) -> List[UploadedFile]:
    if not isinstance(files, list):
        files = [files]

    entries = []

    for file in files:
        file_extension = file.filename.split(".")[-1]

        with NamedTemporaryFile(delete=False, suffix=f".{file_extension}") as temp_file:
            file_content = file.file.read()
            temp_file.write(file_content)
            temp_file.flush()

        entries.append(
            UploadedFile(
                path=temp_file.name,
                original_file_name=file.filename,
                extension=file_extension,
                content_type=file.content_type
            )
        )

    return entries
