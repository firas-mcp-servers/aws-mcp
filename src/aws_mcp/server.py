import click
from mcp.server.fastmcp import FastMCP

from aws_mcp.tools import cloudwatch, ec2, iam, lambda_, rds, s3


def _create_server(port: int = 8000) -> FastMCP:
    mcp = FastMCP("aws-mcp", port=port)
    ec2.register(mcp)
    s3.register(mcp)
    lambda_.register(mcp)
    rds.register(mcp)
    cloudwatch.register(mcp)
    iam.register(mcp)
    return mcp


@click.command()
@click.option("--transport", default="stdio", type=click.Choice(["stdio", "sse"]), help="Transport mode")
@click.option("--port", default=8000, help="Port for SSE mode")
def main(transport: str, port: int) -> None:
    """AWS MCP Server — manage your cloud infrastructure through Claude."""
    mcp = _create_server(port=port)
    mcp.run(transport=transport)  # type: ignore[arg-type]


if __name__ == "__main__":
    main()
