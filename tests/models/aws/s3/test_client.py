import pytest
from models.aws.s3 import Client


def test_init():
    instance = Client()

    assert type(instance.client) is not None


@pytest.mark.parametrize(
    [
        "prefix",
        "max_per_page",
        "expected_results",
    ],
    [
        pytest.param(
            "logs/",
            1,
            [
                "logs/sample1.log",
                "logs/sample2.log",
                "logs/sample3.log",
                "logs/sample4.log",
            ],
        ),
        pytest.param(
            "logs/",
            4,
            [
                "logs/sample1.log",
                "logs/sample2.log",
                "logs/sample3.log",
                "logs/sample4.log",
            ],
        ),
        pytest.param(
            "logs/",
            1000,
            [
                "logs/sample1.log",
                "logs/sample2.log",
                "logs/sample3.log",
                "logs/sample4.log",
            ],
        ),
        pytest.param(
            "example/",
            1,
            [],
        ),
    ],
)
def test_list_object_v2(upload_files, prefix, max_per_page, expected_results):
    upload_files(
        {
            "logs/sample1.log": "tests/files/models/aws/s3/delete/sample.log",
            "logs/sample2.log": "tests/files/models/aws/s3/delete/sample.log",
            "logs/sample3.log": "tests/files/models/aws/s3/delete/sample.log",
            "logs/sample4.log": "tests/files/models/aws/s3/delete/sample.log",
        }
    )

    instance = Client()
    results = instance.list_object_v2("log-bucket-test", prefix, max_per_page)

    assert [result["Key"] for result in results] == expected_results


@pytest.mark.parametrize(
    [
        "delete_objects",
        "expected_results",
    ],
    [
        pytest.param(
            [
                "logs/sample1.log",
            ],
            [
                "logs/sample2.log",
                "logs/sample3.log",
                "logs/sample4.log",
            ],
        ),
        pytest.param(
            [
                "logs/sample1.log",
                "logs/sample2.log",
            ],
            [
                "logs/sample3.log",
                "logs/sample4.log",
            ],
        ),
        pytest.param(
            [
                "logs/sample1.log",
                "logs/sample2.log",
                "logs/sample3.log",
                "logs/sample4.log",
            ],
            [],
        ),
        pytest.param(
            [],
            [
                "logs/sample1.log",
                "logs/sample2.log",
                "logs/sample3.log",
                "logs/sample4.log",
            ],
        ),
    ],
)
def test_delete_objects(upload_files, delete_objects, expected_results):
    upload_files(
        {
            "logs/sample1.log": "tests/files/models/aws/s3/delete/sample.log",
            "logs/sample2.log": "tests/files/models/aws/s3/delete/sample.log",
            "logs/sample3.log": "tests/files/models/aws/s3/delete/sample.log",
            "logs/sample4.log": "tests/files/models/aws/s3/delete/sample.log",
        }
    )

    instance = Client()
    instance.delete_objects("log-bucket-test", delete_objects)

    results = instance.list_object_v2("log-bucket-test", "logs/")

    assert [result["Key"] for result in results] == expected_results
