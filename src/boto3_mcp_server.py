from mcp.server.fastmcp import FastMCP

mcp = FastMCP("aws-boto3")


@mcp.tool()
async def execute_boto3_code() -> str:
    pass
