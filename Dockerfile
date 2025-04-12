# docker run -p 7591:7591 --name boto3-mcp didierdurand/boto3-mcp:ubuntu24.04-latest
# docker run --privileged --name dind-container -d docker:dind

ARG ROOT_IMG="docker:dind"
# ARG ROOT_IMG="alpine"

FROM ${ROOT_IMG}
SHELL ["/bin/sh", "-c"]

ARG PYTHON_VERSION="3.12"
ARG MCP_DIR="/app/boto3-mcp/"

# install tools & utilities + Python
# hadolint ignore=DL3008
RUN apk upgrade \
    && apk add bash curl wget findutils which grep sed git patch unzip  \
    && apk add python3 python3-dev py3-pip

# create the owl dir
WORKDIR ${MCP_DIR}

# copy files from build image
COPY README.md requirements.txt src/ ${MCP_DIR}

# hadolint ignore=SC1091
RUN python${PYTHON_VERSION} -m venv ".venv" \
    && source ".venv/bin/activate" \
    && python${PYTHON_VERSION} -m pip install --upgrade --no-cache-dir -r requirements.txt

# setup runtime env vars
ENV PYTHON_VERSION=${PYTHON_VERSION}

EXPOSE 7591
