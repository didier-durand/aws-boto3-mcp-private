from mcp import types
from mcp.server.fastmcp import FastMCP

# https://medium.com/@cstroliadavis/building-mcp-servers-536969d27809

server = FastMCP("aws-boto3")

@server.list_prompts()
async def handle_list_prompts() -> list[types.Prompt]:
    return [
        types.Prompt(
            name="example-prompt",
            description="An example prompt template",
            arguments=[
                types.PromptArgument(
                    name="arg1", description="Example argument", required=True
                )
            ],
        )
    ]


@server.tool()
async def execute_boto3_code() -> str:
    return "foo"


@server.tool()
async def add(a: int, b: int) -> int:
    """Add two numbers"""
    return a + b


if __name__ == "__main__":
    server.run()
