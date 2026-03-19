import json

from aws_mcp.client import get_client
from aws_mcp.utils import format_error


def register(mcp) -> None:
    @mcp.tool()
    def list_users(profile: str = "", region: str = "") -> str:
        """List all IAM users."""
        try:
            client = get_client("iam", profile or None, region or None)
            response = client.list_users()
            users = [
                f"{u['UserName']} | {u['UserId']} | {u['CreateDate'].strftime('%Y-%m-%d')}"
                for u in response.get("Users", [])
            ]
            return "\n".join(users) if users else "No users found."
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def list_roles(profile: str = "", region: str = "") -> str:
        """List all IAM roles."""
        try:
            client = get_client("iam", profile or None, region or None)
            response = client.list_roles()
            roles = [
                f"{r['RoleName']} | {r['RoleId']} | {r['CreateDate'].strftime('%Y-%m-%d')}"
                for r in response.get("Roles", [])
            ]
            return "\n".join(roles) if roles else "No roles found."
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def get_policy(policy_arn: str, profile: str = "", region: str = "") -> str:
        """Get details of an IAM policy by ARN."""
        try:
            client = get_client("iam", profile or None, region or None)
            policy = client.get_policy(PolicyArn=policy_arn)["Policy"]
            version = client.get_policy_version(
                PolicyArn=policy_arn,
                VersionId=policy["DefaultVersionId"],
            )["PolicyVersion"]
            doc = json.dumps(version["Document"], indent=2)
            lines = [
                f"Name:        {policy['PolicyName']}",
                f"ARN:         {policy['Arn']}",
                f"Description: {policy.get('Description', 'N/A')}",
                f"Version:     {policy['DefaultVersionId']}",
                "",
                "Document:",
                doc,
            ]
            return "\n".join(lines)
        except Exception as e:
            return format_error(e)
