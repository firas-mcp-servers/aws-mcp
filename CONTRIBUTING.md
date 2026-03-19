# Contributing to AWS MCP Server

Thank you for your interest in contributing. This document explains how to set up the project locally, add new tools, and submit changes.

## Development Setup

1. **Fork and clone the repository**

   ```bash
   git clone https://github.com/<your-username>/aws-mcp.git
   cd aws-mcp
   ```

2. **Install dependencies**

   ```bash
   poetry install
   ```

3. **Run the test suite**

   ```bash
   poetry run pytest
   ```

## How to Add a New Tool

The project follows a one-module-per-service pattern under `src/aws_mcp/tools/`. Each module exposes a single `register(mcp)` function.

1. **Choose or create the right module.** If adding a tool for an existing service (e.g., EC2), open `src/aws_mcp/tools/ec2.py`. For a new service, create `src/aws_mcp/tools/<service>.py` and call its `register` function in `src/aws_mcp/server.py`.

2. **Define the tool inside `register(mcp)`** and decorate it with `@mcp.tool()`:

   ```python
   def register(mcp):
       @mcp.tool()
       def my_new_tool(param: str, region: str = "us-east-1") -> str:
           """One-sentence description shown to the model."""
           try:
               client = get_client("ec2", region=region)
               result = client.some_api_call(Param=param)
               return str(result)
           except Exception as e:
               return format_error(e)
   ```

3. **Return a plain string.** Never return `None` or raise from a tool.

4. **Wrap all logic in `try/except Exception as e: return format_error(e)`.** Import `format_error` from `aws_mcp.utils`.

5. **Write a unit test** in `tests/test_<service>.py` using `unittest.mock.patch` to mock the boto3 client.

## PR Requirements

- All existing unit tests must pass (`poetry run pytest tests/ --ignore=tests/test_integration.py`)
- New unit tests required for all new or changed tools
- `poetry run ruff check src/` must exit with no errors
- `poetry run mypy src/` must exit with no errors
- `CHANGELOG.md` updated under `[Unreleased]`

## Code Style

- **Linter:** [Ruff](https://docs.astral.sh/ruff/) — run `poetry run ruff check src/` before committing
- **Line length:** 100 characters
- **Type annotations:** All public functions must have full type annotations
- **Docstrings:** Every `@mcp.tool()`-decorated function must have a one-sentence docstring
- **Imports:** Absolute imports only; no wildcard imports
- **No secrets in code:** Never hard-code AWS credentials, account IDs, or ARNs
