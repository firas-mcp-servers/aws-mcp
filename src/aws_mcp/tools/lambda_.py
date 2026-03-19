
from aws_mcp.client import get_client
from aws_mcp.utils import format_error


def register(mcp) -> None:
    @mcp.tool()
    def list_functions(profile: str = "", region: str = "") -> str:
        """List all Lambda functions."""
        try:
            client = get_client("lambda", profile or None, region or None)
            response = client.list_functions()
            functions = [
                f"{f['FunctionName']} | {f['Runtime']} | {f['LastModified']}"
                for f in response.get("Functions", [])
            ]
            return "\n".join(functions) if functions else "No functions found."
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def invoke_function(
        function_name: str, payload: str = "{}", profile: str = "", region: str = ""
    ) -> str:
        """Invoke a Lambda function with an optional JSON payload."""
        try:
            client = get_client("lambda", profile or None, region or None)
            response = client.invoke(
                FunctionName=function_name,
                Payload=payload.encode(),
            )
            result = response["Payload"].read().decode()
            status = response["StatusCode"]
            return f"Status: {status}\nResponse: {result}"
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_function_logs(
        function_name: str, limit: int = 20, profile: str = "", region: str = ""
    ) -> str:
        """Get recent CloudWatch log events for a Lambda function."""
        try:
            logs_client = get_client("logs", profile or None, region or None)
            log_group = f"/aws/lambda/{function_name}"
            streams = logs_client.describe_log_streams(
                logGroupName=log_group,
                orderBy="LastEventTime",
                descending=True,
                limit=1,
            )
            if not streams["logStreams"]:
                return "No log streams found."
            stream_name = streams["logStreams"][0]["logStreamName"]
            events = logs_client.get_log_events(
                logGroupName=log_group,
                logStreamName=stream_name,
                limit=limit,
            )
            lines = [e["message"].rstrip() for e in events.get("events", [])]
            return "\n".join(lines) if lines else "No log events found."
        except Exception as e:
            return format_error(e)
