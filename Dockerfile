# docker run -p 7591:7591 --name boto3-mcp didierdurand/boto3-mcp:ubuntu24.04-latest

FROM ubuntu:24.04
SHELL ["/bin/bash", "-c"]

ARG PYTHON_VERSION="3.12"

# install tools & utilities + Python
# hadolint ignore=DL3008
RUN apt-get update -y \
    && apt-get upgrade -y  \
    && apt-get install -y --no-install-recommends curl wget findutils which grep sed git patch \
    && apt-get install -y --no-install-recommends python${PYTHON_VERSION} python${PYTHON_VERSION}-venv python${PYTHON_VERSION}-dev  \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# create the owl dir
WORKDIR "/app/boto3-mcp"

# copy files from build image
COPY  "README.md" .
COPY  "requirements.txt" .
COPY  "src/" .

RUN python${PYTHON_VERSION} -m venv ".venv" \
    && source ".venv/bin/activate" \
    && python${PYTHON_VERSION} -m pip install --upgrade --no-cache-dir -r requirements.txt

# setup runtime env vars
ENV PYTHON_VERSION=${PYTHON_VERSION}

EXPOSE 7591

# bash -c  "printenv && source /app/owl/.venv/bin/activate && python3.12 webapp.py"
CMD ["bash", "-c", "printenv 2>&1 | tee -a webapp.log && source /app/owl/.venv/bin/activate && python${PYTHON_VERSION} webapp.py 2>&1 | tee -a webapp.log  || sleep infinity"]