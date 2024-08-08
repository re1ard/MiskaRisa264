#this file to use only linux env's

from subprocess import call as sCall
from subprocess import DEVNULL
import os, sys

def check():
    try:
        if sCall(f"ffmpeg -version".split(), stdin=DEVNULL, stdout=DEVNULL, stderr=DEVNULL) != 0:
            print("Cannot find ffmpeg, features must be disabled")
            return False
        else:
            print("Enabled ffmpeg features!")
            return True
    except Exception as e:
        print("cannot find ffmpeg", e)
        return False


def convertAviToAny(source_file, out_format, print_statuses = False):
    print(f"Start convertion to {out_format}")
    sCall(f"ffmpeg -y -i {source_file} {source_file}.{out_format}".split(), stdin=None if print_statuses else DEVNULL, stdout=None if print_statuses else DEVNULL, stderr=None if print_statuses else DEVNULL)
    if os.path.exists(f"{source_file}.{out_format}"):
        print("convert to other format success")
        os.remove(source_file)
    else:
        print("in process convert trubles convert")
        sys.exit(2)

import argparse
parser = argparse.ArgumentParser()
parser.add_argument("file")
parser.add_argument("--out-format", type=str, default="avi", help = "output video file type")
parser.add_argument("--show-convertion", action="store_true", help = "show ffmpeg cenvertion statuses")
parser.add_argument("--check-ffmpeg", action="store_true")
args = parser.parse_args()

if args.check_ffmpeg:
    sys.exit(0 if check() else 1)

if check():
    convertAviToAny(args.file, args.out_format, args.show_convertion)
else:
    print("ffmpeg is not installed")
    sys.exit(1)