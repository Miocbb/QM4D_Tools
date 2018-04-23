#!/usr/bin/python
"""
Description:
    This python script is used to extract densitry (dst) matrix
    from g09 output. A file with ".txt" extension will be generated
    which can be used directly as "guess read" file for QM4D package.
    The density file will be created under the same folder as g09 output
    directory, if "-n" flag is not specified.

Usage:
    f_chk   g09 output file. Do not accept "*" expression.
            Only specify one output file at one execution.
    -h      show help information then exit.
    -n      specified a customized output name with a user-defined
            path to save output file.
Note:
    1. g09.chk file is required to execute this script.
    2. if '-n' flag is not specified, density.txt file is defaultly
    created under the same directory where the g09 output file is located.
    Otherwise, it will be created under the specified directory with costumized
    name.

Work flow illustration:
g09.chk --> check g09.log normal terminated
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
    parser.add_argument('f_com', help='g09 input file. Do not accept "*"\
                        expression. Only specify one input file at one\
                        execution.')
    parser.add_argument('-n', '-name', default='-1', dest='name',
                        help='specified a customized output name with a\
                        user-defined path to save output file.')
    parser.set_defaults(f_chk_name=None, f_log_name=None,
                        f_txt_name=None, f_com_name=None)
    args = parser.parse_args()

    # initial default valuable based on args
    init_default_var(args)
    # check existence of g09 out file
    # g09.chk, g09.log
    if not os.path.isfile(args.f_chk_name):
        print 'Terminated: g09.chk file not existed'
        sys.exit()
    if not os.path.isfile(args.f_log_name):
        print 'Terminated: g09.log file not existed'
        sys.exit()
    # check normal termination of g09 calc
    if not check_terminattion(args):
        print 'Terminated: g09.log terminated with error'
        sys.exit()
    # formchk g09.chk to g09.fchk
    formchk(args)
    # extract density file
    extract_density(args)
    print '\n Succeed to write "%s" density file' % args.f_txt_name
    return


def init_default_var(args):
    args.f_com_name = args.f_com
    if not os.path.isfile(args.f_com_name):
        print 'Terminated: g09.com file not existed'
        sys.exit()
    # get chk file name from g09.com file.
    f = open(args.f_com_name, 'r')
    for line in f:
        line = line.lstrip().rstrip()
        if line.startswith('%chk='):
            args.f_chk_name = line.split('=')[1]
            break
    if args.f_chk_name is None:
        print 'Terminated: no chk file can be found'
        sys.exit()
    # initial other vars.
    args.f_log_name = args.f_com_name[0:-4] + '.log'
    args.f_txt_name = args.f_chk_name[0:-4] + '.txt'
    if args.name != '-1':  # customize f_txt_name
        args.f_txt_name = args.name + '.txt'


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
    f_txt = args.f_txt_name
    partten_1 = 'Total S'  # Start: Total Spin
    partten_2 = 'Spin'    # Spin: for open shell case
    partten_3 = 'Mulliken'  # End

    start = False
    f1 = open(f_fchk, 'r')
    f2 = open(f_txt,  'w')
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
