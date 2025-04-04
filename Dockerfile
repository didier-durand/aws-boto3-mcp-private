# docker run -p 7591:7591 --name boto3-mcp didierdurand/boto3-mcp:ubuntu24.04-latest

FROM ubuntu:24.04
SHELL ["/bin/bash", "-c"]

ARG PYTHON_VERSION="3.12"

# install tools & utilities + Python
# hadolint ignore=DL3008
RUN apt-get update -y \
    && apt-get upgrade -y  \
    && apt-get install -y --no-install-recommends curl wget findutils which grep sed git patch unzip \
    && apt-get install -y --no-install-recommends python${PYTHON_VERSION} python${PYTHON_VERSION}-venv python${PYTHON_VERSION}-dev  \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# create the owl dir
WORKDIR "/app/boto3-mcp"

# copy files from build image
COPY  "README.md" .
COPY  "requirements.txt" .
COPY  "src/" .

# hadolint ignore=SC1091
RUN python${PYTHON_VERSION} -m venv ".venv" \
    && source ".venv/bin/activate" \
    && python${PYTHON_VERSION} -m pip install --upgrade --no-cache-dir -r requirements.txt

RUN curl -fsSL https://deno.land/install.sh | sh && ln -s /root/.deno/bin/deno /usr/local/bin/deno

# setup runtime env vars
ENV PYTHON_VERSION=${PYTHON_VERSION}

EXPOSE 7591

# bash -c  "printenv && source /app/owl/.venv/bin/activate && python3.12 webapp.py"
# CMD ["bash", "-c", "printenv 2>&1 | tee -a boto3-mcp.log && source /app/boto3-mcp/.venv/bin/activate && python${PYTHON_VERSION} boto3_fastapi_server.py 2>&1 | tee -a boto3-mcp.log  || sleep infinity"]
CMD ["bash", "-c", "printenv 2>&1 ; sleep infinity"]