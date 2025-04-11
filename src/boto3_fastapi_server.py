from enum import StrEnum

import uvicorn
from fastapi import FastAPI
from fastapi.responses import PlainTextResponse
from pydantic import BaseModel

from boto3_mcp_server import MCP_SERVER_NAME

MCP_HOST = "127.0.0.1"
MCP_PORT = 5000

class BackendApi(StrEnum):
    INVALID_URL = "invalid_url"
    EXECUTE_PYTHON = "execute_python"

class ExecRequest(BaseModel):
    code: str
    description: str | None = None
    aws_access_key_id: str | None = None
    aws_secret_access_key: str | None = None
fastapi_server = FastAPI()

@fastapi_server.get("/", response_class=PlainTextResponse)
async def get_root():
    return f"{MCP_SERVER_NAME}\n"

@fastapi_server.post(f"/{BackendApi.EXECUTE_PYTHON}")
async def post_execute(exec_request: ExecRequest):
    return exec_request.code

if __name__ == "__main__":
    uvicorn.run(app="boto3_fastapi_server:fastapi_server", host=MCP_HOST, port=MCP_PORT, reload=True)
