from datetime import datetime, timedelta, timezone
from typing import Any, Dict, List

from . import Base
from models import settings
from models.aws.s3 import Client as S3Client


class LogInS3BucketDestroyer(Base):
    TIMEZONE_JST = timezone(timedelta(hours=+9))

    def __init__(self, event: Any, context: Any) -> None:
        super().__init__(event, context)
        self.s3_client = S3Client()

    def execute(self) -> Dict[str, Any]:
        for config in settings.SETTINGS["logs"]:
            bucket = config["bucket"]
            prefix = config["prefix"]
            retention = int(config["retention"])

            delete_files = self.get_objects(bucket, prefix, retention)
            self.logger.info(
                f"bucket: {bucket}, prefix: {prefix}, retention: {retention}, delete_files: {len(delete_files)}"
            )
            self.logger.debug(delete_files)

            if len(delete_files) > 0:
                self.s3_client.delete_objects(bucket, delete_files)

        return {}

    def get_objects(self, bucket: str, prefix: str, retention: int) -> List[str]:
        results = []

        retention_date = datetime.now(self.TIMEZONE_JST) - timedelta(days=retention)
        self.logger.debug(retention_date)

        objects = self.s3_client.list_object_v2(bucket, prefix)
        for object in objects:
            key = object["Key"]
            is_deletable = object["LastModified"] < retention_date
            self.logger.debug(f"{key} / {object['LastModified']} / {is_deletable}")

            if is_deletable:
                results.append(key)

        return results


def lambda_handler(event: Any, context: Any) -> Dict[str, Any]:
    return LogInS3BucketDestroyer(event, context).execute()
