import pytest
from typing import List
from models.aws.s3 import Client


def test_init() -> None:
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
def test_list_object_v2(
    prefix: str, max_per_page: int, expected_results: List[str]
) -> None:
    instance = Client()
    results = instance.list_object_v2("log-bucket-test", prefix, max_per_page)

    assert [result["Key"] for result in results] == expected_results
