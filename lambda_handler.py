import os
import sys
from typing import Any, Dict

# 外部パッケージはLayerを使用するなどして、もう少しスマートにimportする方法を検討する
for path in ["log_in_s3_bucket_destroyer", "lib"]:
    sys.path.append(os.path.join(os.path.dirname(__file__), path))

from log_in_s3_bucket_destroyer import LogInS3BucketDestroyer  # noqa: E402


def lambda_handler(event: Any, context: Any) -> Dict[str, Any]:
    return LogInS3BucketDestroyer(event, context).execute()
