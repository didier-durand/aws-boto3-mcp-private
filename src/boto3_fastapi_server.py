import uvicorn
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse

from boto3_mcp_server import MCP_SERVER_NAME

MCP_HOST = "127.0.0.1"
MCP_PORT = 5000
fastapi_server = FastAPI()

@fastapi_server.get("/", response_class=PlainTextResponse)
async def get_root():
    return MCP_SERVER_NAME

@fastapi_server.post("execute", response_class=PlainTextResponse)
async def post_execute():
    return MCP_SERVER_NAME

if __name__ == "__main__":
    uvicorn.run(app="boto3_fastapi_server:fastapi_server", host=MCP_HOST, port=MCP_PORT, reload=True)
