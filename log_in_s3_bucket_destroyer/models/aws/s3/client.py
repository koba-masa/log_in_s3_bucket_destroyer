import boto3
from models import settings
from typing import Any, Dict, List

from models.aws import Base


class Client(Base):
    def __init__(self) -> None:
        super().__init__()
        self.client = boto3.client(
            "s3",
            aws_access_key_id=settings.SETTINGS["aws_access_key"],
            aws_secret_access_key=settings.SETTINGS["aws_secret_access_key"],
            endpoint_url=self.endpoint_url(),
        )

    def list_object_v2(
        self, bucket: str, prefix: str, max_per_page: int = 1000
    ) -> List[Dict[str, Any]]:
        results = []

        response = self.client.list_objects_v2(
            Bucket=bucket,
            Prefix=prefix,
            MaxKeys=max_per_page,
        )

        if "Contents" in response:
            results = response["Contents"]

        while response["IsTruncated"]:
            continuation_token = response["NextContinuationToken"]

            response = self.client.list_objects_v2(
                Bucket=bucket,
                Prefix=prefix,
                MaxKeys=max_per_page,
                ContinuationToken=continuation_token,
            )

            if "Contents" in response:
                results.extend(response["Contents"])

        return results
