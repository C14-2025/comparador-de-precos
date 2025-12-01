FROM jenkins/jenkins:lts

ARG PYTHON_VERSION=Python-3.12.3

USER root

RUN apt-get update
RUN apt-get install -y wget
RUN apt-get update && apt-get install -y \
python3 \
python3-pip \
# Add any other required packages here, e.g., git, curl, build-essential
&& rm -rf /var/lib/apt/lists/*
RUN apt-get clean

USER jenkins