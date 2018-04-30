#!/usr/bin/env python3
"""
Extract all the include file path for qm4d package from
the compliation database (compile_commands.json), which
can be generated from cmake by runing
 cmake -DCMAKE_EXPORT_COMPILE_COMMANDS=on path/to/source

All the extracted path will be writen into a config file,
which is defaulted named as 'qm4d.config'.

Yuncai Mei
Apri-29, 2018
"""

import json
import os
import sys
import argparse


def arg_parser():
    """ parser arguments"""

    parser = argparse.ArgumentParser(description="""extract
             all the include file path for qm4d package from
             compilation database.""")

    parser.add_argument('file_json', help='path for database file')
    parser.add_argument('-n', dest='file_config', default='qm4d.config',
                        help='name the file used to contain all the \
                             include file path.')
    return parser.parse_args()


def get_flag_I(cmd):
    """
    extract the flag -I from a compile command.

    cmd : <type: str>  the whole compile cmd.
    return a list, in which each element is an include
    path.
    """
    include_path = []
    cmd_parse = cmd.split()
    for i in range(len(cmd_parse)):
        if cmd_parse[i].startswith("-I"):
            include_path.append(cmd_parse[i])
    return include_path


def write_include(include_path, args):
    """
    write all the include path into file.

    include_path : <type: list> each element is
    a string that is a -I flag with a include path.
    """
    file_config = args.file_config
    if os.path.isfile(file_config):
        msg = 'Output file is already existed. Sure to overwirte ? [y/n]\n'
        while (True):
            answer = input(msg)
            if answer in ['y', 'Y', 'N', 'n']:
                answer = answer.upper()
                break
            else:
                print("accepted choice: y, Y, n, N\n")

        if answer == 'N':
            sys.exit()

    fconf = open(file_config, "w")
    for i in range(len(include_path)):
        fconf.write(include_path[i] + '\n')
    fconf.close()


def main():
    args = arg_parser()

    # load compilation database file.
    path_json = args.file_json
    with open(path_json) as data_file:
        data = json.load(data_file)

    include_path = []
    for i in range(len(data)):
        include_path += get_flag_I(data[i]['command'])
    include_path = list(set(include_path))
    write_include(include_path, args)


if __name__ == "__main__":
    main()
