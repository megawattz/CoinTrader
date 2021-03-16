from ubuntu:21.04

RUN apt-get update && DEBIAN_FRONTEND=noninteractive apt-get install -y \
    less \
    jq \
    vim \
    curl \
    ngrep \
    strace \
    apt-file \
    python3 \
    python3-pip

RUN pip3 install \
    python-binance \
    cbpro

RUN DEBIAN_FRONTEND=noninteractive apt-get install -y \
    ipython3 \
    python3-cmd2 \
    python3-pprintpp

RUN pip3 install \
    etherscan \
    pythonql

ENV PATH=${PATH}:/app/bin

WORKDIR /app
