FROM ubuntu:20.04 as base

RUN apt-get update && apt-get -y install \
    build-essential \
    python3.8 \
    python3-pip \
    python3-pytest

RUN python3 -m pip install --upgrade pip

RUN useradd jenkins --shell /bin/bash --create-home
USER jenkins

ENV PATH="$PATH:/home/jenkins/.local/bin"