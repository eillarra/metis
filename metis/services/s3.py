import os

import boto3
import requests
from storages.backends.s3 import S3Storage as BaseS3Storage


class S3Storage(BaseS3Storage):
    def url(self, name, parameters=None, expire=None, http_method=None):
        url = super().url(name, parameters, expire, http_method)
        bucket_url = f'{os.environ.get("S3_ENDPOINT_URL")}/{os.environ.get("S3_BUCKET_NAME")}/'
        return url.replace(bucket_url, "/media/")


def get_s3_client():
    return boto3.client(
        service_name="s3",
        endpoint_url=os.environ.get("S3_ENDPOINT_URL"),
        aws_access_key_id=os.environ.get("S3_ACCESS_KEY"),
        aws_secret_access_key=os.environ.get("S3_SECRET_KEY"),
    )


def delete_s3_object(object_key: str) -> None:
    get_s3_client().delete_object(
        Bucket=os.environ.get("S3_BUCKET_NAME"),
        Key=object_key,
    )


def get_s3_presigned_url(object_key: str, expires_in: int = 60) -> str:
    return get_s3_client().generate_presigned_url(
        ClientMethod="get_object",
        ExpiresIn=expires_in,
        Params={
            "Bucket": os.environ.get("S3_BUCKET_NAME"),
            "Key": object_key,
        },
    )


def get_s3_response(object_key: str) -> requests.Response:
    res = requests.get(url=get_s3_presigned_url(object_key, 10), stream=True)
    res.raise_for_status()
    return res
