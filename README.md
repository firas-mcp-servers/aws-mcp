# AWS MCP Server

![Python 3.11+](https://img.shields.io/badge/python-3.11%2B-blue) ![License: MIT](https://img.shields.io/badge/license-MIT-green) ![CI](https://img.shields.io/github/actions/workflow/status/firas-mcp-servers/aws-mcp/ci.yml?label=CI)

MCP server exposing AWS services as tools for Claude. Manage your cloud infrastructure through natural language.

## Features

- **EC2** — `list_instances`, `start_instance`, `stop_instance`, `describe_instance`
- **S3** — `list_buckets`, `upload_file`, `download_file`, `list_objects`, `delete_object`
- **Lambda** — `list_functions`, `invoke_function`, `get_function_logs`
- **RDS** — `list_databases`, `describe_db`, `create_snapshot`
- **CloudWatch** — `get_metrics`, `list_alarms`, `get_log_events`
- **IAM** — `list_users`, `list_roles`, `get_policy`

## Prerequisites

- Python 3.11+
- [Poetry](https://python-poetry.org/docs/#installation)
- AWS credentials configured (via `~/.aws/credentials`, environment variables, or IAM role)

## Installation

```bash
git clone https://github.com/firas-mcp-servers/aws-mcp.git
cd aws-mcp
poetry install
```

## Usage

### Claude Desktop (stdio transport)

Add the following to your Claude Desktop configuration file (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "aws-mcp": {
      "command": "poetry",
      "args": ["run", "aws-mcp"],
      "cwd": "/path/to/aws-mcp"
    }
  }
}
```

### SSE Mode

```bash
poetry run aws-mcp --transport sse --port 8000
```

The server will be available at `http://0.0.0.0:8000/sse`.

## Available Tools

| Service | Tool | Description |
|---|---|---|
| EC2 | `list_instances` | List all EC2 instances |
| EC2 | `start_instance` | Start an EC2 instance by ID |
| EC2 | `stop_instance` | Stop an EC2 instance by ID |
| EC2 | `describe_instance` | Get detailed info about an instance |
| S3 | `list_buckets` | List all S3 buckets |
| S3 | `upload_file` | Upload a file to a bucket |
| S3 | `download_file` | Download a file from a bucket |
| S3 | `list_objects` | List objects in a bucket |
| S3 | `delete_object` | Delete an object from a bucket |
| Lambda | `list_functions` | List all Lambda functions |
| Lambda | `invoke_function` | Invoke a Lambda function |
| Lambda | `get_function_logs` | Retrieve logs for a Lambda function |
| RDS | `list_databases` | List all RDS database instances |
| RDS | `describe_db` | Get detailed info about a database |
| RDS | `create_snapshot` | Create a snapshot of a database |
| CloudWatch | `get_metrics` | Retrieve CloudWatch metrics |
| CloudWatch | `list_alarms` | List CloudWatch alarms |
| CloudWatch | `get_log_events` | Fetch log events from a log group |
| IAM | `list_users` | List all IAM users |
| IAM | `list_roles` | List all IAM roles |
| IAM | `get_policy` | Get details of an IAM policy |

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

MIT — see [LICENSE](LICENSE).
