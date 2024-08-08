#!/bin/bash
wine /opt/win32-python/python.exe h264_converter.py $1 && \
python3 ffmpeg.py "$1.avi" --out-format mp4