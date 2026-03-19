# AWS MCP Server — Developer Guide

## Idea

MCP server for interacting with AWS services: EC2, S3, Lambda, RDS, CloudWatch, IAM — manage your cloud infrastructure through Claude.

## Planned Architecture

- `src/aws_mcp/client.py` — `boto3` session factory with profile/region support (`get_client(service)`)
- `src/aws_mcp/utils.py` — `format_error()` for consistent error responses
- `src/aws_mcp/tools/` — one module per AWS service (ec2, s3, lambda, rds, cloudwatch, iam)
- `src/aws_mcp/server.py` — MCP server entry point; calls `register(mcp)` on each tool module

Each tool module exports a single `register(mcp)` function that decorates inner functions with `@mcp.tool()`.

## Planned Tools

- `list_instances` / `start_instance` / `stop_instance` / `describe_instance`
- `list_buckets` / `upload_file` / `download_file` / `list_objects` / `delete_object`
- `list_functions` / `invoke_function` / `get_function_logs`
- `list_databases` / `describe_db` / `create_snapshot`
- `get_metrics` / `list_alarms` / `get_log_events`

## Common Commands

```bash
# Install dependencies
poetry install

# Run unit tests
poetry run pytest tests/ --ignore=tests/test_integration.py

# Run integration tests (requires AWS credentials)
poetry run pytest tests/test_integration.py -v

# Lint
poetry run ruff check src/

# Type check
poetry run mypy src/

# Run the server (stdio mode)
poetry run aws-mcp

# Run the server (SSE mode)
poetry run aws-mcp --transport sse --port 8000
```

## Adding a New Tool

1. Add the tool function inside the `register(mcp)` function of the appropriate module under `src/aws_mcp/tools/`.
2. Decorate it with `@mcp.tool()`.
3. Return a plain string (success message or formatted data).
4. Wrap the body in `try/except Exception as e: return format_error(e)`.
5. Add a unit test in `tests/test_<module>.py` using `unittest.mock`.

## Error Handling

Always use `format_error(e)` from `aws_mcp.utils`. Map `botocore.exceptions.ClientError` to readable messages.

## Transport Modes

- `stdio` (default) — subprocess managed by the MCP client
- `sse` — HTTP server at `http://0.0.0.0:<port>/sse`
