import uvicorn
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

from boto3_mcp_server import MCP_SERVER_NAME

MCP_HOST = "127.0.0.1"
MCP_PORT = 5000

MCP_HELLO_WORLD = "Hello from aws boto3 MCP server!"
server = FastAPI()


@server.get("/", response_class=PlainTextResponse)
async def get_root():
    return MCP_SERVER_NAME

if __name__ == "__main__":
    uvicorn.run("boto3_mcp_server:server", host=MCP_HOST, port=MCP_PORT, reload=True)
