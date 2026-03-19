from aws_mcp.client import get_client
from aws_mcp.utils import format_error


def register(mcp) -> None:
    @mcp.tool()
    def list_instances(profile: str = "", region: str = "") -> str:
        """List all EC2 instances with their state and type."""
        try:
            client = get_client("ec2", profile or None, region or None)
            response = client.describe_instances()
            instances = []
            for reservation in response["Reservations"]:
                for inst in reservation["Instances"]:
                    name = next(
                        (t["Value"] for t in inst.get("Tags", []) if t["Key"] == "Name"), "—"
                    )
                    instances.append(
                        f"{inst['InstanceId']} | {inst['InstanceType']} | "
                        f"{inst['State']['Name']} | {name}"
                    )
            return "\n".join(instances) if instances else "No instances found."
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def start_instance(instance_id: str, profile: str = "", region: str = "") -> str:
        """Start an EC2 instance by ID."""
        try:
            client = get_client("ec2", profile or None, region or None)
            client.start_instances(InstanceIds=[instance_id])
            return f"Started instance {instance_id}."
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def stop_instance(instance_id: str, profile: str = "", region: str = "") -> str:
        """Stop an EC2 instance by ID."""
        try:
            client = get_client("ec2", profile or None, region or None)
            client.stop_instances(InstanceIds=[instance_id])
            return f"Stopped instance {instance_id}."
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def describe_instance(instance_id: str, profile: str = "", region: str = "") -> str:
        """Describe a specific EC2 instance."""
        try:
            client = get_client("ec2", profile or None, region or None)
            response = client.describe_instances(InstanceIds=[instance_id])
            inst = response["Reservations"][0]["Instances"][0]
            lines = [
                f"ID:           {inst['InstanceId']}",
                f"Type:         {inst['InstanceType']}",
                f"State:        {inst['State']['Name']}",
                f"AMI:          {inst['ImageId']}",
                f"Public IP:    {inst.get('PublicIpAddress', 'N/A')}",
                f"Private IP:   {inst.get('PrivateIpAddress', 'N/A')}",
                f"Launch time:  {inst['LaunchTime']}",
            ]
            return "\n".join(lines)
        except Exception as e:
            return format_error(e)
