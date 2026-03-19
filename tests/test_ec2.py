from unittest.mock import MagicMock, patch

import pytest

from aws_mcp.tools.ec2 import register


def make_mcp():
    """Return a mock mcp that captures registered tools by name."""
    tools = {}

    class MockMCP:
        def tool(self):
            def decorator(fn):
                tools[fn.__name__] = fn
                return fn
            return decorator

    return MockMCP(), tools


def test_list_instances_returns_instances():
    mcp, tools = make_mcp()
    register(mcp)

    fake_response = {
        "Reservations": [
            {
                "Instances": [
                    {
                        "InstanceId": "i-1234567890abcdef0",
                        "InstanceType": "t3.micro",
                        "State": {"Name": "running"},
                        "Tags": [{"Key": "Name", "Value": "my-server"}],
                    }
                ]
            }
        ]
    }

    with patch("aws_mcp.tools.ec2.get_client") as mock_get_client:
        mock_client = MagicMock()
        mock_client.describe_instances.return_value = fake_response
        mock_get_client.return_value = mock_client

        result = tools["list_instances"]()
        assert "i-1234567890abcdef0" in result
        assert "t3.micro" in result
        assert "running" in result
        assert "my-server" in result


def test_list_instances_empty():
    mcp, tools = make_mcp()
    register(mcp)

    with patch("aws_mcp.tools.ec2.get_client") as mock_get_client:
        mock_client = MagicMock()
        mock_client.describe_instances.return_value = {"Reservations": []}
        mock_get_client.return_value = mock_client

        result = tools["list_instances"]()
        assert "No instances" in result


def test_start_instance():
    mcp, tools = make_mcp()
    register(mcp)

    with patch("aws_mcp.tools.ec2.get_client") as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        result = tools["start_instance"]("i-abc123")
        assert "i-abc123" in result
        mock_client.start_instances.assert_called_once_with(InstanceIds=["i-abc123"])


def test_stop_instance():
    mcp, tools = make_mcp()
    register(mcp)

    with patch("aws_mcp.tools.ec2.get_client") as mock_get_client:
        mock_client = MagicMock()
        mock_get_client.return_value = mock_client

        result = tools["stop_instance"]("i-abc123")
        assert "i-abc123" in result
        mock_client.stop_instances.assert_called_once_with(InstanceIds=["i-abc123"])


def test_describe_instance():
    mcp, tools = make_mcp()
    register(mcp)

    from datetime import datetime, timezone
    fake_response = {
        "Reservations": [
            {
                "Instances": [
                    {
                        "InstanceId": "i-abc123",
                        "InstanceType": "t3.micro",
                        "State": {"Name": "running"},
                        "ImageId": "ami-12345",
                        "PublicIpAddress": "1.2.3.4",
                        "PrivateIpAddress": "10.0.0.1",
                        "LaunchTime": datetime(2024, 1, 1, tzinfo=timezone.utc),
                    }
                ]
            }
        ]
    }

    with patch("aws_mcp.tools.ec2.get_client") as mock_get_client:
        mock_client = MagicMock()
        mock_client.describe_instances.return_value = fake_response
        mock_get_client.return_value = mock_client

        result = tools["describe_instance"]("i-abc123")
        assert "i-abc123" in result
        assert "t3.micro" in result
        assert "1.2.3.4" in result


def test_list_instances_error():
    mcp, tools = make_mcp()
    register(mcp)

    with patch("aws_mcp.tools.ec2.get_client") as mock_get_client:
        mock_get_client.side_effect = Exception("connection refused")

        result = tools["list_instances"]()
        assert "Error" in result
