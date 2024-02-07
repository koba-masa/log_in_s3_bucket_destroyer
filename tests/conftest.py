import os
import pytest

from models import settings
from models.aws.s3 import Client as S3Client


os.environ["ENVIRONMENT"] = "test"
settings.load_config("config/test.yaml")

@pytest.fixture(scope="function")
def upload_files():
    def _method(objects):
        s3_client = S3Client().client

        for key, body in objects.items():
            s3_client.put_object(
                Bucket="log-bucket-test",
                Key=key,
                Body=body,
            )

        return

    return _method
