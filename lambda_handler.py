import os
import sys
from typing import Any, Dict

for path in ["log_in_s3_bucket_destroyer"]:
    sys.path.append(os.path.join(os.path.dirname(__file__), path))

from log_in_s3_bucket_destroyer import LogInS3BucketDestroyer  # noqa: E402


def lambda_handler(event: Any, context: Any) -> Dict[str, Any]:
    return LogInS3BucketDestroyer(event, context).execute()
