from unittest.mock import MagicMock, patch

from aws_mcp.tools.lambda_ import register


def make_mcp():
    tools = {}

    class MockMCP:
        def tool(self):
            def decorator(fn):
                tools[fn.__name__] = fn
                return fn
            return decorator

    return MockMCP(), tools


def test_list_functions():
    mcp, tools = make_mcp()
    register(mcp)

    with patch("aws_mcp.tools.lambda_.get_client") as mock_get_client:
        mock_client = MagicMock()
        mock_client.list_functions.return_value = {
            "Functions": [
                {"FunctionName": "my-func", "Runtime": "python3.11", "LastModified": "2024-01-01"}
            ]
        }
        mock_get_client.return_value = mock_client

        result = tools["list_functions"]()
        assert "my-func" in result
        assert "python3.11" in result


def test_list_functions_empty():
    mcp, tools = make_mcp()
    register(mcp)

    with patch("aws_mcp.tools.lambda_.get_client") as mock_get_client:
        mock_client = MagicMock()
        mock_client.list_functions.return_value = {"Functions": []}
        mock_get_client.return_value = mock_client

        result = tools["list_functions"]()
        assert "No functions" in result


def test_invoke_function():
    mcp, tools = make_mcp()
    register(mcp)

    with patch("aws_mcp.tools.lambda_.get_client") as mock_get_client:
        mock_client = MagicMock()
        payload_mock = MagicMock()
        payload_mock.read.return_value = b'{"result": "ok"}'
        mock_client.invoke.return_value = {"StatusCode": 200, "Payload": payload_mock}
        mock_get_client.return_value = mock_client

        result = tools["invoke_function"]("my-func", '{"key": "value"}')
        assert "200" in result
        assert "ok" in result
        mock_client.invoke.assert_called_once_with(
            FunctionName="my-func", Payload=b'{"key": "value"}'
        )


def test_get_function_logs():
    mcp, tools = make_mcp()
    register(mcp)

    with patch("aws_mcp.tools.lambda_.get_client") as mock_get_client:
        mock_client = MagicMock()
        mock_client.describe_log_streams.return_value = {
            "logStreams": [{"logStreamName": "2024/01/01/[$LATEST]abc123"}]
        }
        mock_client.get_log_events.return_value = {
            "events": [
                {"message": "START RequestId: abc\n"},
                {"message": "END RequestId: abc\n"},
            ]
        }
        mock_get_client.return_value = mock_client

        result = tools["get_function_logs"]("my-func")
        assert "START" in result
        assert "END" in result


def test_get_function_logs_no_streams():
    mcp, tools = make_mcp()
    register(mcp)

    with patch("aws_mcp.tools.lambda_.get_client") as mock_get_client:
        mock_client = MagicMock()
        mock_client.describe_log_streams.return_value = {"logStreams": []}
        mock_get_client.return_value = mock_client

        result = tools["get_function_logs"]("my-func")
        assert "No log streams" in result


def test_lambda_error_handling():
    mcp, tools = make_mcp()
    register(mcp)

    with patch("aws_mcp.tools.lambda_.get_client") as mock_get_client:
        mock_get_client.side_effect = Exception("connection error")

        result = tools["list_functions"]()
        assert "Error" in result
