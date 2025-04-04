import uvicorn
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

MCP_HOST = "127.0.0.1"
MCP_PORT = 5000

MCP_HELLO_WORLD = "Hello from aws boto3 MCP server!"
server = FastAPI()


@server.get("/", response_class=PlainTextResponse)
async def get_root():
    return MCP_HELLO_WORLD


@server.get("/resp1", response_class=PlainTextResponse)
async def get_root():
    return "response1"


if __name__ == "__main__":
    uvicorn.run("boto3_mcp_server:server", host=MCP_HOST, port=MCP_PORT, reload=True)
