from unittest.mock import MagicMock, patch

import pytest

from aws_mcp.tools.s3 import register


def make_mcp():
    tools = {}

    class MockMCP:
        def tool(self):
            def decorator(fn):
                tools[fn.__name__] = fn
                return fn
            return decorator

    return MockMCP(), tools


def test_list_buckets():
    mcp, tools = make_mcp()
    register(mcp)

    with patch("aws_mcp.tools.s3.get_client") as mock_get_client:
        mock_client = MagicMock()
        mock_client.list_buckets.return_value = {
            "Buckets": [{"Name": "my-bucket"}, {"Name": "another-bucket"}]
        }
        mock_get_client.return_value = mock_client

        result = tools["list_buckets"]()
        assert "my-bucket" in result
        assert "another-bucket" in result


def test_list_buckets_empty():
    mcp, tools = make_mcp()
    register(mcp)

    with patch("aws_mcp.tools.s3.get_client") as mock_get_client:
        mock_client = MagicMock()
        mock_client.list_buckets.return_value = {"Buckets": []}
        mock_get_client.return_value = mock_client

        result = tools["list_buckets"]()
        assert "No buckets" in result


def test_list_objects():
    mcp, tools = make_mcp()
    register(mcp)

    with patch("aws_mcp.tools.s3.get_client") as mock_get_client:
        mock_client = MagicMock()
        mock_client.list_objects_v2.return_value = {
            "Contents": [{"Key": "folder/file.txt"}, {"Key": "other.json"}]
        }
        mock_get_client.return_value = mock_client

        result = tools["list_objects"]("my-bucket")
        assert "folder/file.txt" in result
        assert "other.json" in result


def test_upload_file():
    mcp, tools = make_mcp()
    register(mcp)

    with patch("aws_mcp.tools.s3.get_client") as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        result = tools["upload_file"]("/tmp/test.txt", "my-bucket", "uploads/test.txt")
        assert "my-bucket" in result
        mock_client.upload_file.assert_called_once_with("/tmp/test.txt", "my-bucket", "uploads/test.txt")


def test_download_file():
    mcp, tools = make_mcp()
    register(mcp)

    with patch("aws_mcp.tools.s3.get_client") as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        result = tools["download_file"]("my-bucket", "file.txt", "/tmp/file.txt")
        assert "my-bucket" in result
        mock_client.download_file.assert_called_once_with("my-bucket", "file.txt", "/tmp/file.txt")


def test_delete_object():
    mcp, tools = make_mcp()
    register(mcp)

    with patch("aws_mcp.tools.s3.get_client") as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        result = tools["delete_object"]("my-bucket", "file.txt")
        assert "my-bucket" in result
        mock_client.delete_object.assert_called_once_with(Bucket="my-bucket", Key="file.txt")


def test_s3_error_handling():
    mcp, tools = make_mcp()
    register(mcp)

    with patch("aws_mcp.tools.s3.get_client") as mock_get_client:
        mock_get_client.side_effect = Exception("access denied")

        result = tools["list_buckets"]()
        assert "Error" in result
