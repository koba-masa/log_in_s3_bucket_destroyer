import pytest
from datetime import datetime, timedelta, timezone

from log_in_s3_bucket_destroyer import LogInS3BucketDestroyer


TIMEZONE_JST = timezone(timedelta(hours=+9))

@pytest.mark.parametrize(
    [
        "mock_data",
        "expected",
    ],
    [
        pytest.param(
            [
                {"Key": "logs/sample1.log", "LastModified": datetime.now(TIMEZONE_JST) - timedelta(days=0)},
                {"Key": "logs/sample2.log", "LastModified": datetime.now(TIMEZONE_JST) - timedelta(days=1)},
                {"Key": "logs/sample3.log", "LastModified": datetime.now(TIMEZONE_JST) - timedelta(days=2)},
                {"Key": "logs/sample4.log", "LastModified": datetime.now(TIMEZONE_JST) - timedelta(days=3)},
            ],
            [
                "logs/sample2.log",
                "logs/sample3.log",
                "logs/sample4.log",
            ],
        ),
    ]
)
def test_execute(mocker, upload_files, mock_data, expected):
    instance = LogInS3BucketDestroyer({}, {})
    instance.s3_client = mocker.Mock()
    instance.s3_client.list_object_v2.return_value = mock_data
    instance.s3_client.delete_objects.return_value = None

    instance.execute()

    instance.s3_client.delete_objects.assert_called_once_with("log-bucket-test", expected)


@pytest.mark.parametrize(
    [
        "retention",
        "mock_data",
        "expected_results",
    ],
    [
        pytest.param(
            30,
            [
                {"Key": "logs/sample1.log", "LastModified": datetime.now(TIMEZONE_JST) - timedelta(days=0)},
                {"Key": "logs/sample2.log", "LastModified": datetime.now(TIMEZONE_JST) - timedelta(days=1)},
                {"Key": "logs/sample3.log", "LastModified": datetime.now(TIMEZONE_JST) - timedelta(days=2)},
                {"Key": "logs/sample4.log", "LastModified": datetime.now(TIMEZONE_JST) - timedelta(days=3)},
            ],
            [
            ],
        ),
        pytest.param(
            1,
            [
                {"Key": "logs/sample1.log", "LastModified": datetime.now(TIMEZONE_JST) - timedelta(days=0)},
                {"Key": "logs/sample2.log", "LastModified": datetime.now(TIMEZONE_JST) - timedelta(days=1)},
                {"Key": "logs/sample3.log", "LastModified": datetime.now(TIMEZONE_JST) - timedelta(days=2)},
                {"Key": "logs/sample4.log", "LastModified": datetime.now(TIMEZONE_JST) - timedelta(days=3)},
            ],
            [
                "logs/sample2.log",
                "logs/sample3.log",
                "logs/sample4.log",
            ],
        ),
        pytest.param(
            2,
            [
                {"Key": "logs/sample1.log", "LastModified": datetime.now(TIMEZONE_JST) - timedelta(days=0)},
                {"Key": "logs/sample2.log", "LastModified": datetime.now(TIMEZONE_JST) - timedelta(days=1)},
                {"Key": "logs/sample3.log", "LastModified": datetime.now(TIMEZONE_JST) - timedelta(days=2)},
                {"Key": "logs/sample4.log", "LastModified": datetime.now(TIMEZONE_JST) - timedelta(days=3)},
            ],
            [
                "logs/sample3.log",
                "logs/sample4.log",
            ],
        )
    ]
)
def test_get_objects(mocker, retention, mock_data, expected_results):
    instance = LogInS3BucketDestroyer({}, {})
    instance.s3_client = mocker.Mock()
    instance.s3_client.list_object_v2.return_value = mock_data

    results = instance.get_objects("log-bucket-test", "logs/", retention)

    assert results == expected_results
