#https://www.python.org/ftp/python/3.12.3/python-3.12.3-embed-win32.zip
FROM ubuntu:22.04

RUN dpkg --add-architecture i386 \
    && apt-get update \
    && apt-get install -y ffmpeg wget unzip python3 \
    && mkdir -pm755 /etc/apt/keyrings \
    && wget -O /etc/apt/keyrings/winehq-archive.key https://dl.winehq.org/wine-builds/winehq.key \
    && wget -NP /etc/apt/sources.list.d/ https://dl.winehq.org/wine-builds/ubuntu/dists/jammy/winehq-jammy.sources \
    && apt-get update && apt-get install -y winehq-stable \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /opt/win32-python && cd /opt/win32-python \
    && wget https://www.python.org/ftp/python/3.12.3/python-3.12.3-embed-win32.zip \
    && unzip python-3.12.3-embed-win32.zip \
    && rm python-3.12.3-embed-win32.zip 

RUN echo "wine test open python" \
    && cd /opt/win32-python \
    && wine python.exe --version

RUN mkdir /app
WORKDIR /app
COPY * ./

RUN wine /opt/win32-python/python.exe h264_converter.py --help
RUN python3 ffmpeg.py /dev/null --check-ffmpeg

ENTRYPOINT [ "tail", "-f", "/dev/null" ]
