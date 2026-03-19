from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

from aws_mcp.tools.iam import register


def make_mcp():
    tools = {}

    class MockMCP:
        def tool(self):
            def decorator(fn):
                tools[fn.__name__] = fn
                return fn
            return decorator

    return MockMCP(), tools


def test_list_users():
    mcp, tools = make_mcp()
    register(mcp)

    with patch("aws_mcp.tools.iam.get_client") as mock_get_client:
        mock_client = MagicMock()
        mock_client.list_users.return_value = {
            "Users": [
                {
                    "UserName": "alice",
                    "UserId": "AIDAXXXXXXXXXX",
                    "CreateDate": datetime(2024, 1, 15, tzinfo=timezone.utc),
                }
            ]
        }
        mock_get_client.return_value = mock_client

        result = tools["list_users"]()
        assert "alice" in result
        assert "AIDAXXXXXXXXXX" in result


def test_list_users_empty():
    mcp, tools = make_mcp()
    register(mcp)

    with patch("aws_mcp.tools.iam.get_client") as mock_get_client:
        mock_client = MagicMock()
        mock_client.list_users.return_value = {"Users": []}
        mock_get_client.return_value = mock_client

        result = tools["list_users"]()
        assert "No users" in result


def test_list_roles():
    mcp, tools = make_mcp()
    register(mcp)

    with patch("aws_mcp.tools.iam.get_client") as mock_get_client:
        mock_client = MagicMock()
        mock_client.list_roles.return_value = {
            "Roles": [
                {
                    "RoleName": "lambda-exec",
                    "RoleId": "AROAXXXXXXXXXX",
                    "CreateDate": datetime(2024, 2, 1, tzinfo=timezone.utc),
                }
            ]
        }
        mock_get_client.return_value = mock_client

        result = tools["list_roles"]()
        assert "lambda-exec" in result
        assert "AROAXXXXXXXXXX" in result


def test_get_policy():
    mcp, tools = make_mcp()
    register(mcp)

    with patch("aws_mcp.tools.iam.get_client") as mock_get_client:
        mock_client = MagicMock()
        mock_client.get_policy.return_value = {
            "Policy": {
                "PolicyName": "ReadOnlyAccess",
                "Arn": "arn:aws:iam::aws:policy/ReadOnlyAccess",
                "Description": "Provides read-only access",
                "DefaultVersionId": "v1",
            }
        }
        mock_client.get_policy_version.return_value = {
            "PolicyVersion": {
                "Document": {"Version": "2012-10-17", "Statement": [{"Effect": "Allow"}]}
            }
        }
        mock_get_client.return_value = mock_client

        result = tools["get_policy"]("arn:aws:iam::aws:policy/ReadOnlyAccess")
        assert "ReadOnlyAccess" in result
        assert "Provides read-only access" in result
        assert "2012-10-17" in result


def test_iam_error_handling():
    mcp, tools = make_mcp()
    register(mcp)

    with patch("aws_mcp.tools.iam.get_client") as mock_get_client:
        mock_get_client.side_effect = Exception("permission denied")

        result = tools["list_users"]()
        assert "Error" in result
