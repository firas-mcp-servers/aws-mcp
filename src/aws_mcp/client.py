import boto3


def get_client(service: str, profile: str | None = None, region: str | None = None):
    """Create a boto3 client for the given AWS service."""
    session = boto3.Session(profile_name=profile, region_name=region)
    return session.client(service)  # type: ignore[call-overload]
