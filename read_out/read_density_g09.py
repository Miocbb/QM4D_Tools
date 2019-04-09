#!/usr/bin/python
"""
Description:
    This python script is used to extract densitry (dst) matrix
    from g09 output. A file with ".txt" extension will be generated
    which can be used directly as "guess read" file for QM4D package.
    The density file will be created under the same folder as g09 output
    directory, if "-n" flag is not specified.

Usage:
    f_inp   g09 file (can only by either g09.com or g09.log). Do not accept
            "*" expression. Only specify one input file at one execution.
    -h      show help information then exit.
    -n      specified a customized output name with a user-defined
            path to save output file.
Note:
    1. a g09 file (CAN ONLY BE EITHER g09.com or g09.log) is required to
    execute this script.
    2. if '-n' flag is not specified, density.txt file is defaultly
    created under the same directory where the g09 output file is located.
    Otherwise, it will be created under the specified directory with costumized
    name.

Work flow illustration:
g09.com/g09.log --> check g09.log normal terminated --> g09.chk
--> g09.fchk (formchk) --> [dst].txt

Author: Yuncai Mei
Date:   2017/10/20
"""

import argparse
import os.path
import sys
import subprocess as subp
from subprocess import Popen, PIPE


def main():
    # setting argument parser
    parser = argparse.ArgumentParser(description="""Extract densitry matrix from g09 output. A density file with ".txt"
    extension will be generated which can be used directly as "guess read"
    file for QM4D package. The density file will be created under the same
    directory with the g09 output file, if "-n" flag is not specified.""")
    parser.add_argument('f_chk', help='g09 chk file. Do not accept "*"\
                        expression. Only specify one chk file at one\
                        execution.')
    parser.add_argument('-n', '-name', default='-1', dest='name',
                        help='specified a customized output name with a\
                        user-defined path to save output file.')
    parser.add_argument('--check_termination', default=None, dest='check_termination_file',
                        help='check if it is normally terminated for the given\
                        log file.')
    parser.set_defaults(f_chk_name=None, f_log_name=None,
                        f_dst_name=None)
    args = parser.parse_args()

    # initial default valuable based on args
    init_default_var(args)

    if args.check_termination_file:
        if not check_terminattion(args):
            print 'Terminated: {:s} terminated with error'.format(args.check_termination_file)

        sys.exit()

    # formchk g09.chk to g09.fchk
    formchk(args)

    # extract density file
    extract_density(args)
    print '\n Succeed to write "%s" density file' % args.f_dst_name
    return


def init_default_var(args):
    # chk file
    args.f_chk_name = args.f_chk
    if not os.path.isfile(args.f_chk_name):
        print 'Terminated: chk file not existed'
        sys.exit()

    # dst file
    args.f_dst_name = args.f_chk_name[0:-4] + '.dst'
    if args.name != '-1':  # customize f_txt_name
        args.f_dst_name = args.name

    # log file
    if args.check_termination_file:
        args.f_log_name = args.check_termination_file;
        if not os.path.isfile(args.f_log_name):
            print 'Terminated: "{:s}" file not existed'.format(args.check_termination_file)
            sys.exit()

def check_terminattion(args):
    """
    check if g09.log terminate normally
    """
    f_log_name = args.f_log_name
    key = 'Normal termination'
    cmd = ['tail', '-1', f_log_name]
    p = Popen(cmd, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    if stdout.find(key):
        return True
    else:
        return False


def formchk(args):
    f_chk_name = args.f_chk_name
    f_fchk_name = f_chk_name[0:-4] + '.fchk'
    cmd = ['formchk', f_chk_name, f_fchk_name]
    subp.call(cmd)


def extract_density(args):
    """
    Extract densitry matrix from g09.fchk file
    string 'Total S', 'Spin' and 'Mulliken' are
    the parttens for locate the density matrix data
    """
    f_fchk = args.f_chk_name[0:-4] + '.fchk'
    f_dst  = args.f_dst_name
    partten_1 = 'Total S'  # Start: Total Spin
    partten_2 = 'Spin'    # Spin: for open shell case
    partten_3 = 'Mulliken'  # End

    start = False
    f1 = open(f_fchk, 'r')
    f2 = open(f_dst,  'w')
    for line in f1:
        if partten_3 in line:
            break
        if start:  # start write density
            # only collect data number
            if partten_2 not in line:
                f2.write(line)
        if partten_1 in line:
            start = True
    f1.close()
    f2.close()


if __name__ == '__main__':
    main()
