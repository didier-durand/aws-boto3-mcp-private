from mcp.server.fastmcp import FastMCP

mcp = FastMCP("aws-boto3")


@mcp.tool()
async def execute_boto3_code() -> str:
    return "foo"

@mcp.tool()
async def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b

if __name__ == "__main__":
    mcp.run()
