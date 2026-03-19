
from aws_mcp.client import get_client
from aws_mcp.utils import format_error


def register(mcp) -> None:
    @mcp.tool()
    def list_buckets(profile: str = "", region: str = "") -> str:
        """List all S3 buckets."""
        try:
            client = get_client("s3", profile or None, region or None)
            response = client.list_buckets()
            buckets = [b["Name"] for b in response.get("Buckets", [])]
            return "\n".join(buckets) if buckets else "No buckets found."
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def list_objects(bucket: str, prefix: str = "", profile: str = "", region: str = "") -> str:
        """List objects in an S3 bucket with optional prefix."""
        try:
            client = get_client("s3", profile or None, region or None)
            kwargs = {"Bucket": bucket}
            if prefix:
                kwargs["Prefix"] = prefix
            response = client.list_objects_v2(**kwargs)
            objects = [obj["Key"] for obj in response.get("Contents", [])]
            return "\n".join(objects) if objects else "No objects found."
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def upload_file(local_path: str, bucket: str, key: str, profile: str = "", region: str = "") -> str:
        """Upload a local file to S3."""
        try:
            client = get_client("s3", profile or None, region or None)
            client.upload_file(local_path, bucket, key)
            return f"Uploaded {local_path} to s3://{bucket}/{key}."
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def download_file(bucket: str, key: str, local_path: str, profile: str = "", region: str = "") -> str:
        """Download a file from S3 to a local path."""
        try:
            client = get_client("s3", profile or None, region or None)
            client.download_file(bucket, key, local_path)
            return f"Downloaded s3://{bucket}/{key} to {local_path}."
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def delete_object(bucket: str, key: str, profile: str = "", region: str = "") -> str:
        """Delete an object from S3."""
        try:
            client = get_client("s3", profile or None, region or None)
            client.delete_object(Bucket=bucket, Key=key)
            return f"Deleted s3://{bucket}/{key}."
        except Exception as e:
            return format_error(e)
