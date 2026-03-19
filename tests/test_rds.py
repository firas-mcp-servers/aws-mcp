from unittest.mock import MagicMock, patch

from aws_mcp.tools.rds import register


def make_mcp():
    tools = {}

    class MockMCP:
        def tool(self):
            def decorator(fn):
                tools[fn.__name__] = fn
                return fn
            return decorator

    return MockMCP(), tools


def test_list_databases():
    mcp, tools = make_mcp()
    register(mcp)

    with patch("aws_mcp.tools.rds.get_client") as mock_get_client:
        mock_client = MagicMock()
        mock_client.describe_db_instances.return_value = {
            "DBInstances": [
                {
                    "DBInstanceIdentifier": "mydb",
                    "DBInstanceClass": "db.t3.micro",
                    "Engine": "mysql",
                    "DBInstanceStatus": "available",
                }
            ]
        }
        mock_get_client.return_value = mock_client

        result = tools["list_databases"]()
        assert "mydb" in result
        assert "db.t3.micro" in result
        assert "mysql" in result
        assert "available" in result


def test_list_databases_empty():
    mcp, tools = make_mcp()
    register(mcp)

    with patch("aws_mcp.tools.rds.get_client") as mock_get_client:
        mock_client = MagicMock()
        mock_client.describe_db_instances.return_value = {"DBInstances": []}
        mock_get_client.return_value = mock_client

        result = tools["list_databases"]()
        assert "No databases" in result


def test_describe_db():
    mcp, tools = make_mcp()
    register(mcp)

    with patch("aws_mcp.tools.rds.get_client") as mock_get_client:
        mock_client = MagicMock()
        mock_client.describe_db_instances.return_value = {
            "DBInstances": [
                {
                    "DBInstanceIdentifier": "mydb",
                    "DBInstanceClass": "db.t3.micro",
                    "Engine": "postgres",
                    "EngineVersion": "15.3",
                    "DBInstanceStatus": "available",
                    "Endpoint": {"Address": "mydb.cluster.us-east-1.rds.amazonaws.com", "Port": 5432},
                    "MultiAZ": False,
                    "AllocatedStorage": 20,
                }
            ]
        }
        mock_get_client.return_value = mock_client

        result = tools["describe_db"]("mydb")
        assert "mydb" in result
        assert "postgres" in result
        assert "5432" in result
        assert "20" in result


def test_create_snapshot():
    mcp, tools = make_mcp()
    register(mcp)

    with patch("aws_mcp.tools.rds.get_client") as mock_get_client:
        mock_client = MagicMock()
        mock_client.create_db_snapshot.return_value = {
            "DBSnapshot": {
                "DBSnapshotIdentifier": "mydb-snap-1",
                "Status": "creating",
            }
        }
        mock_get_client.return_value = mock_client

        result = tools["create_snapshot"]("mydb", "mydb-snap-1")
        assert "mydb-snap-1" in result
        assert "creating" in result


def test_rds_error_handling():
    mcp, tools = make_mcp()
    register(mcp)

    with patch("aws_mcp.tools.rds.get_client") as mock_get_client:
        mock_get_client.side_effect = Exception("access denied")

        result = tools["list_databases"]()
        assert "Error" in result
