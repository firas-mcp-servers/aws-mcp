from datetime import UTC, datetime, timedelta

from aws_mcp.client import get_client
from aws_mcp.utils import format_error


def register(mcp) -> None:
    @mcp.tool()
    def get_metrics(
        namespace: str,
        metric_name: str,
        hours: int = 1,
        profile: str = "",
        region: str = "",
    ) -> str:
        """Get CloudWatch metric statistics for the past N hours."""
        try:
            client = get_client("cloudwatch", profile or None, region or None)
            end = datetime.now(UTC)
            start = end - timedelta(hours=hours)
            response = client.get_metric_statistics(
                Namespace=namespace,
                MetricName=metric_name,
                StartTime=start,
                EndTime=end,
                Period=300,
                Statistics=["Average", "Maximum"],
            )
            datapoints = sorted(response.get("Datapoints", []), key=lambda x: x["Timestamp"])
            if not datapoints:
                return "No datapoints found."
            lines = [
                f"{dp['Timestamp']} | avg={dp['Average']:.2f} | max={dp['Maximum']:.2f}"
                for dp in datapoints
            ]
            return "\n".join(lines)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def list_alarms(profile: str = "", region: str = "") -> str:
        """List all CloudWatch alarms and their state."""
        try:
            client = get_client("cloudwatch", profile or None, region or None)
            response = client.describe_alarms()
            alarms = [
                f"{a['AlarmName']} | {a['StateValue']} | {a.get('AlarmDescription', '')}"
                for a in response.get("MetricAlarms", [])
            ]
            return "\n".join(alarms) if alarms else "No alarms found."
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_log_events(
        log_group: str,
        log_stream: str,
        limit: int = 50,
        profile: str = "",
        region: str = "",
    ) -> str:
        """Get log events from a CloudWatch log stream."""
        try:
            client = get_client("logs", profile or None, region or None)
            response = client.get_log_events(
                logGroupName=log_group,
                logStreamName=log_stream,
                limit=limit,
            )
            lines = [e["message"].rstrip() for e in response.get("events", [])]
            return "\n".join(lines) if lines else "No log events found."
        except Exception as e:
            return format_error(e)
