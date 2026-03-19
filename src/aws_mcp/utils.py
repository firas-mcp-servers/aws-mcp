import botocore.exceptions


def format_error(e: Exception) -> str:
    """Return a readable error string from any exception."""
    if isinstance(e, botocore.exceptions.ClientError):
        code = e.response["Error"]["Code"]
        message = e.response["Error"]["Message"]
        return f"AWS error [{code}]: {message}"
    return f"Error: {type(e).__name__}: {e}"
