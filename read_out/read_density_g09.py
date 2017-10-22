#!/usr/bin/python
"""
Description:
1. This python script is used to extract densitry (dst) matrix
from g09 output.
2. [dst].txt file is created under the dir of current execute path
and can be used as 'guess read' file for QM4D.

Note:
1. g09.chk file is required to execute this script.

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
    parser = argparse.ArgumentParser(description=
            """Extract the density file from g09
            output file.
            """)
    parser.add_argument('f_chk', help='g09.chk file')
    parser.add_argument('-name', '-n', default='-1',
                        help='density.txt file name')
    parser.set_defaults(f_chk_name=None, f_log_name=None,
                        f_txt_name=None)
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
    print '\n Succeed to write "%s" density file' %args.f_txt_name
    return


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
    cmd = [ 'formchk', f_chk_name ]
    subp.call(cmd)


def extract_density(args):
    """
    Extract densitry matrix from g09.fchk file
    string 'Total S', 'Spin' and 'Mulliken' are
    the parttens for locate the density matrix data
    """
    f_fchk = args.f_chk_name[0:-4] + '.fchk'
    f_txt  = args.f_txt_name
    partten_1 = 'Total S' # Start: Total Spin
    partten_2 = 'Spin'    # Spin: for open shell case
    partten_3 = 'Mulliken'# End
    
    start = False
    f1 = open(f_fchk, 'r')
    f2 = open(f_txt,  'w')
    for line in f1:
        if partten_3 in line:
            break
        if start: #start write density
            # only collect data number
            if partten_2 not in line:
                f2.write(line)
        if partten_1 in line:
            start = True
    f1.close()
    f2.close()



def init_default_var(args):
    args.f_chk_name = args.f_chk
    args.f_log_name = args.f_chk[0:-4] + '.log'
    args.f_txt_name = args.f_chk[0:-4] + '.txt'
    if args.name != '-1': # customize f_txt_name
        args.f_txt_name = args.name



if __name__ == '__main__':
    main()
