from aws_mcp.client import get_client
from aws_mcp.utils import format_error


def register(mcp) -> None:
    @mcp.tool()
    def list_databases(profile: str = "", region: str = "") -> str:
        """List all RDS database instances."""
        try:
            client = get_client("rds", profile or None, region or None)
            response = client.describe_db_instances()
            dbs = [
                f"{db['DBInstanceIdentifier']} | {db['DBInstanceClass']} | "
                f"{db['Engine']} | {db['DBInstanceStatus']}"
                for db in response.get("DBInstances", [])
            ]
            return "\n".join(dbs) if dbs else "No databases found."
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def describe_db(db_instance_id: str, profile: str = "", region: str = "") -> str:
        """Describe a specific RDS database instance."""
        try:
            client = get_client("rds", profile or None, region or None)
            response = client.describe_db_instances(DBInstanceIdentifier=db_instance_id)
            db = response["DBInstances"][0]
            lines = [
                f"ID:          {db['DBInstanceIdentifier']}",
                f"Class:       {db['DBInstanceClass']}",
                f"Engine:      {db['Engine']} {db.get('EngineVersion', '')}",
                f"Status:      {db['DBInstanceStatus']}",
                f"Endpoint:    {db.get('Endpoint', {}).get('Address', 'N/A')}",
                f"Port:        {db.get('Endpoint', {}).get('Port', 'N/A')}",
                f"Multi-AZ:    {db.get('MultiAZ', False)}",
                f"Storage:     {db.get('AllocatedStorage', 'N/A')} GB",
            ]
            return "\n".join(lines)
        except Exception as e:
            return format_error(e)

    @mcp.tool()
    def create_snapshot(
        db_instance_id: str, snapshot_id: str, profile: str = "", region: str = ""
    ) -> str:
        """Create a manual snapshot of an RDS database instance."""
        try:
            client = get_client("rds", profile or None, region or None)
            response = client.create_db_snapshot(
                DBInstanceIdentifier=db_instance_id,
                DBSnapshotIdentifier=snapshot_id,
            )
            snap = response["DBSnapshot"]
            return f"Snapshot {snap['DBSnapshotIdentifier']} creation started. Status: {snap['Status']}"
        except Exception as e:
            return format_error(e)
