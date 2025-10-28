FROM ubuntu:20.04

ENV TZ=Etc/UTC
ENV DEBIAN_FRONTEND=noninteractive
RUN ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone

# 安装所有必要的构建依赖（参考 tools/linux/deps.py）
RUN apt-get -y update && \
    apt-get -y install \
    tar \
    sudo \
    build-essential \
    git \
    cmake \
    curl \
    wget \
    ca-certificates \
    p7zip-full \
    autoconf2.13 \
    libtool \
    subversion \
    gzip \
    apt-transport-https \
    glib-2.0-dev \
    libglu1-mesa-dev \
    libgtk-3-dev \
    libpulse-dev \
    libasound2-dev \
    libatspi2.0-dev \
    libcups2-dev \
    libdbus-1-dev \
    libicu-dev \
    libgstreamer1.0-dev \
    libgstreamer-plugins-base1.0-dev \
    libx11-xcb-dev \
    libxcb-icccm4 \
    libxcb-image0 \
    libxcb-keysyms1 \
    libxcb-render-util0 \
    libxcb-xinerama0 \
    libxcb-xkb1 \
    libxi-dev \
    libxrender-dev \
    libxss1 \
    libncurses5 \
    libncurses6 \
    libxkbcommon-dev \
    libxkbcommon-x11-dev \
    nodejs \
    npm \
    && rm -rf /var/lib/apt/lists/*

ADD . /build_tools
WORKDIR /build_tools

RUN mkdir -p /opt/python3 && \
    tar -xzf /build_tools/tools/linux/python3.tar.gz -C /opt/python3 --strip-components=1

ENV PATH="/opt/python3/bin:${PATH}"

RUN ln -s /opt/python3/bin/python3.10 /usr/bin/python

CMD ["sh", "-c", "cd tools/linux && python3 ./automate.py"]
