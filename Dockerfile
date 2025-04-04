# docker run -p 7860:7860 -e MISTRAL_API_KEY=$MISTRAL_API_KEY -e OWL_USERNAME=$OWL_USERNAME -e OWL_PASSWORD=$OWL_PASSWORD --name owl didierdurand/owl:ubuntu-latest

FROM ubuntu:24.04
SHELL ["/bin/bash", "-c"]

ARG PYTHON_VERSION="3.12"

# install headers, tools & utilities + Python
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

# hadolint ignore=SC1091
RUN python${PYTHON_VERSION} -m venv ".venv" \
    && source ".venv/bin/activate" \
    && python${PYTHON_VERSION} -m pip install --upgrade --no-cache-dir -r requirements.txt

# setup runtime env vars
ENV PYTHON_VERSION=${PYTHON_VERSION}

EXPOSE 7591

# bash -c  "printenv && source /app/owl/.venv/bin/activate && python3.12 webapp.py"
CMD ["bash", "-c", "printenv 2>&1 | tee -a webapp.log && source /app/owl/.venv/bin/activate && python${PYTHON_VERSION} webapp.py 2>&1 | tee -a webapp.log  || sleep infinity"]