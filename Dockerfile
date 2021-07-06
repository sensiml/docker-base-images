FROM ubuntu:latest
LABEL Author="Justin Moore <justin.moore@sensiml.com>"
LABEL Description="Base Image for setting up SensiML docker runners"

RUN apt-get update -qq && apt-get install -y \
  build-essential \
  wget \
  git git-lfs dos2unix \
  python3 \
  python3-pip \
  vim \
  jq \
  zip > /dev/null \
  && rm -rf /var/lib/apt/lists/* \
  && mkdir /build \
  && ln -s /usr/bin/python3 /usr/bin/python \
  && pip3 install --no-cache-dir awscli \
  && apt-get clean \
  && rm -rf /var/lib/apt/lists/*
