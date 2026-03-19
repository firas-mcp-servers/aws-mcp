from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

from aws_mcp.tools.cloudwatch import register


def make_mcp():
    tools = {}

    class MockMCP:
        def tool(self):
            def decorator(fn):
                tools[fn.__name__] = fn
                return fn
            return decorator

    return MockMCP(), tools


def test_get_metrics():
    mcp, tools = make_mcp()
    register(mcp)

    with patch("aws_mcp.tools.cloudwatch.get_client") as mock_get_client:
        mock_client = MagicMock()
        mock_client.get_metric_statistics.return_value = {
            "Datapoints": [
                {
                    "Timestamp": datetime(2024, 1, 1, 12, 0, tzinfo=timezone.utc),
                    "Average": 45.5,
                    "Maximum": 90.0,
                }
            ]
        }
        mock_get_client.return_value = mock_client

        result = tools["get_metrics"]("AWS/EC2", "CPUUtilization")
        assert "45.50" in result
        assert "90.00" in result


def test_get_metrics_no_data():
    mcp, tools = make_mcp()
    register(mcp)

    with patch("aws_mcp.tools.cloudwatch.get_client") as mock_get_client:
        mock_client = MagicMock()
        mock_client.get_metric_statistics.return_value = {"Datapoints": []}
        mock_get_client.return_value = mock_client

        result = tools["get_metrics"]("AWS/EC2", "CPUUtilization")
        assert "No datapoints" in result


def test_list_alarms():
    mcp, tools = make_mcp()
    register(mcp)

    with patch("aws_mcp.tools.cloudwatch.get_client") as mock_get_client:
        mock_client = MagicMock()
        mock_client.describe_alarms.return_value = {
            "MetricAlarms": [
                {
                    "AlarmName": "high-cpu",
                    "StateValue": "ALARM",
                    "AlarmDescription": "CPU over 80%",
                }
            ]
        }
        mock_get_client.return_value = mock_client

        result = tools["list_alarms"]()
        assert "high-cpu" in result
        assert "ALARM" in result


def test_list_alarms_empty():
    mcp, tools = make_mcp()
    register(mcp)

    with patch("aws_mcp.tools.cloudwatch.get_client") as mock_get_client:
        mock_client = MagicMock()
        mock_client.describe_alarms.return_value = {"MetricAlarms": []}
        mock_get_client.return_value = mock_client

        result = tools["list_alarms"]()
        assert "No alarms" in result


def test_get_log_events():
    mcp, tools = make_mcp()
    register(mcp)

    with patch("aws_mcp.tools.cloudwatch.get_client") as mock_get_client:
        mock_client = MagicMock()
        mock_client.get_log_events.return_value = {
            "events": [
                {"message": "INFO Starting application\n"},
                {"message": "INFO Ready\n"},
            ]
        }
        mock_get_client.return_value = mock_client

        result = tools["get_log_events"]("/aws/app", "stream-1")
        assert "Starting application" in result
        assert "Ready" in result


def test_cloudwatch_error_handling():
    mcp, tools = make_mcp()
    register(mcp)

    with patch("aws_mcp.tools.cloudwatch.get_client") as mock_get_client:
        mock_get_client.side_effect = Exception("region not supported")

        result = tools["list_alarms"]()
        assert "Error" in result
