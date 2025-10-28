FROM ubuntu:20.04

ENV TZ=Etc/UTC
ENV DEBIAN_FRONTEND=noninteractive
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 安装 Server 构建的最小必需依赖（带重试机制）
RUN for i in 1 2 3; do \
      apt-get -y update && \
      apt-get -y install --fix-missing --no-install-recommends \
        tar \
        sudo \
        build-essential \
        git \
        cmake \
        curl \
        wget \
        ca-certificates \
        p7zip-full \
        libicu-dev \
        nodejs \
        npm \
      && break || sleep 15; \
    done && \
    rm -rf /var/lib/apt/lists/*

ADD . /build_tools
WORKDIR /build_tools

RUN mkdir -p /opt/python3 && \
    tar -xzf /build_tools/tools/linux/python3.tar.gz -C /opt/python3 --strip-components=1

ENV PATH="/opt/python3/bin:${PATH}"

RUN ln -s /opt/python3/bin/python3.10 /usr/bin/python

CMD ["sh", "-c", "cd tools/linux && python3 ./automate.py"]
