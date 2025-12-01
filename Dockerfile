FROM jenkins/jenkins:lts

ARG PYTHON_VERSION=Python-3.12.3

USER root

RUN apt-get update
RUN apt-get install -y wget

RUN wget --no-verbose -O /tmp/Python-3.12.3.tgz https://www.python.org/ftp/python/3.12.3/Python-3.12.3.tgz
RUN tar xzf /tmp/${PYTHON_VERSION}-bin.tar.gz -C /opt/

RUN apt-get clean

USER jenkins