FROM ubuntu:latest

COPY / /home

WORKDIR /home 

RUN apt update && \
    apt install -y python3.8 python3.8-dev python3-pip && \
    python3.8 setup.py install
