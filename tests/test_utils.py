import botocore.exceptions
import pytest

from aws_mcp.utils import format_error


def test_format_error_client_error():
    error_response = {"Error": {"Code": "NoSuchBucket", "Message": "The bucket does not exist"}}
    e = botocore.exceptions.ClientError(error_response, "ListObjects")
    result = format_error(e)
    assert "NoSuchBucket" in result
    assert "does not exist" in result


def test_format_error_generic():
    e = ValueError("something went wrong")
    result = format_error(e)
    assert "ValueError" in result
    assert "something went wrong" in result


def test_format_error_returns_string():
    e = RuntimeError("boom")
    result = format_error(e)
    assert isinstance(result, str)
