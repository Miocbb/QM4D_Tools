#!/usr/bin/python
import argparse
import os.path
import sys

parser = argparse.ArgumentParser()
parser.add_argument("f_xyz", help = "the xyz file")

args = parser.parse_args()
if os.path.isfile(args.f_xyz):
    _fInp = open("./" + args.f_xyz[0:-4], "w")

    _fInp.write("this is a test\n")
    _fInp.close()
else:
    sys.exit()


