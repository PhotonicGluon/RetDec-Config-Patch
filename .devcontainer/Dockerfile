FROM ghcr.io/photonicgluon/retdec-docker:latest as devcontainer
USER root

# Install missing dependencies
RUN apt-get update \
    && apt-get install -y git python3-pip python3-setuptools python3-venv

# Set up virtual environment
RUN python3 -m venv /venv --prompt RetDec-Config-Patch; chmod -R +x /venv
RUN /venv/bin/pip install poetry

ENV PYTHONPATH="$PYTHONPATH:$PWD"
