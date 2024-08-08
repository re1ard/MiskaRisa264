import struct, sys
if 8 * struct.calcsize("P") != 32:
    print("Converter work only with 32-bit python")
    sys.exit(32)

import os
dll = os.path.abspath('H264Play.dll')
print(f"H264Play.dll path: {dll}")

import ctypes as c
from ctypes import wintypes as c_windows
from ctypes import CFUNCTYPE as c_callback
l = c.cdll.LoadLibrary(dll)

print("Readed DLL SDK Version", l.H264_PLAY_GetSdkVersion())

##only use this part in windows
from subprocess import call as sCall
from subprocess import DEVNULL
import os, sys

def check():
    try:
        if sCall(f"ffmpeg -version", stdin=DEVNULL, stdout=DEVNULL, stderr=DEVNULL) != 0:
            print("Cannot find ffmpeg, features must be disabled")
            return False
        else:
            print("Enabled ffmpeg features!")
            return True
    except:
        return False

FFMPEG = check()

def convertAviToAny(source_file, out_format, print_statuses = False):
    print(f"Start convertion to {out_format}")
    sCall(f"ffmpeg -y -i \"{source_file}\" \"{source_file}.{out_format}\"", stdin=None if print_statuses else DEVNULL, stdout=None if print_statuses else DEVNULL, stderr=None if print_statuses else DEVNULL)
    if os.path.exists(f"{source_file}.{out_format}"):
        print("convert to other format success")
        os.remove(source_file)
    else:
        print("in process convert trubles convert")
        sys.exit(2)
##end

@c_callback(None, c_windows.DWORD, c_windows.DWORD, c.c_long)
def coverPosCallback(CurrentPos, TotoalPos, dwUser):
    pass
    #print(CurrentPos, TotoalPos, dwUser)
    #if CurrentPos == TotoalPos:
    #    print("@")

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("input", default="test.h264", help="full path to files, aka: \"C:\\Users\\user\\test.h264\"")
parser.add_argument("--stream-type", type = int, default=2, help="""
Default value is 2. See leaked H264Play.h in project for more info, contains this:
enum ENCODE_TYPE
{
	StreamTypeEmpty = 0,
	StreamTypeH264 = 2,
	StreamTypeJpeg = 3,
	StreamTypeGeneral = 4,
	StreamTypePCM8 = 7,
	StreamTypeStd = 8
};
""")
parser.add_argument("--out-format", type=str, default="avi", help = "output video file type")
parser.add_argument("--show-convertion", action="store_true", help = "show ffmpeg cenvertion statuses")
args = parser.parse_args()
output = f"{args.input}.avi"

print("Input file path:", args.input)
print("Output file path", output)

l.H264_PLAY_ConvertFile(
    args.input.encode(), 
    output.encode(), 
    args.stream_type, 
    coverPosCallback, 
    0)

from time import sleep

check_exists_fails = 10
check_output_complete = 100
last_size = -1
while True:
    if (check_exists_fails == 0):
        print("Output file not be created")
        sys.exit(1)

    sleep(0.1)
    if os.path.exists(output):
        if os.path.getsize(output) == last_size:
            print("completed!", check_exists_fails, check_output_complete)
            if args.out_format.lower() != "avi":
                if FFMPEG:
                    convertAviToAny(output, args.out_format, args.show_convertion)
                    sys.exit(0)
                else:
                    print("cannot find ffmpeg, save only original file")
                    sys.exit(0)
            else:
                print("not need convert file")
                sys.exit(0)
        else:
            last_size = os.path.getsize(output)
            check_output_complete -= 1
    else:
        check_exists_fails -= 1

