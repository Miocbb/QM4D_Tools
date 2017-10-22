#!/usr/bin/python
"""
Description:
1. This is python script is used to extract all the eigenvales
from LOSC functional calculation by QM4D.
2. [eig].eig file is created under the dir of current execute
path.
3. The format of [eig].eig file is sperated columns, shown as
below:
"spin    orbital    eig_prev    eig_losc".

Note:
1. qm4d.out output file is required to execute this script.
1. eigenvalues is extracted based on the "eig_proj" key word.

Work flow:
qm4d.out check normal terminated --> [eig].eig

Author: Yuncai Mei
Date:   2017/10/20
"""

import sys
import os.path
import argparse
#from subprocess import Popen, PIPE

def SigExit(*string):
    for i in string:
        print i
    sys.eixt()

def set_parser():
    """
    Positional argument
    f_out:  losc qm4d.out file

    Optional arugment
    -name, -n: [eig].eig file name
    """
    parser = argparse.ArgumentParser(description =
            "Extract the all the eigenvales from "
            "losc qm4d.out file.")
    parser.add_argument('f_out', help='qm4d.out file')
    parser.add_argument('-n', '-name', default=0, dest='f_eig',
                        help='[eig].eig file name')
    parser.set_defaults(_f_out=None, _f_eig=None)
    return parser.parse_args()

def init_args(args):
    args._f_out = args.f_out
    if args.f_eig == 0:
        args._f_eig = args.f_out + '.eig'
    else:
        args._f_eig = args.f_eig

def check_args(args):
    """
    !if _f_eig file is existed, it will
    !be re-wrote with new data
    """
    if not os.path.isfile(args._f_out):
        SigExit("Terminated: qm4d out file not existed\n")

def check_normal_termination(args):
    """
    Return 1 when qm4d is normally terminated and
    SCF convergence is reached. otherwise return 0
    """
    f_out = args._f_out
    partern1 = 'SCF converged'
    partern2 = 'Lucky'
    status1 = 0
    status2 = 0
    f = open(f_out, 'r')
    for line in f:
        if line.find(partern1): status1 = 1
        elif line.find(partern2): status2 = 1
    f.close()
    return (status1 and status2)

def read_elec_num(args):
    """
    Return alpha and beat electron number with float type.

    return = (alpha_elec_num, beta_elec_num)
    """
    f_out = args._f_out
    partern = 'Alpha electron'
    f = open(f_out, 'r')
    for line in f:
        if partern in line:
            rst = line.split()
            f.close()
            return float(rst[3]), float(rst[7])
    f.close()
    SigExit('Terminated: no electron info find\n')


def extract_eig(args):
    """
    Extract alpha and beta eigenvalues with "spin,
    orbital_num, eig_prev, eig_losc" imformation".

    return = (alpha_eig[], beta_eig[])
    """
    f_out = args._f_out
    match_line = []
    partern = 'eig_proj'
    f = open(f_out, 'r')
    for line in f:
        if partern in line:
            #item = line.replace('=', ' ').split()
            match_line.append( line.replace('=', ' ').split() )
    f.close()
    #print match_line
    eig = {'0': [], '1':[]}
    for item in match_line:
            string = "{:<7s}{:<6s}{:<16s}{:<16s}"\
                    .format(item[1], item[3], item[5], item[7])\
                    .rstrip()
            eig[item[1]].append(string)
    #print eig['0'], eig['1']
    return eig['0'], eig['1']


def main():
    args = set_parser()
    init_args(args)
    check_args(args)
    #print args
    if not check_normal_termination(args):
        SigExit("Terminated: qm4d.out not normal terminated\n")
    aelec_num, belec_num = read_elec_num(args)
    alpha_eig, beta_eig  = extract_eig(args)
    title_str = "{:<7s}{:<6s}{:<16s}{:<16s}"\
                .format('spin','orb','eig_prev','eig_losc')\
                .rstrip()
    str_aelec = "{:<7d}{:<6d}{:<16d}{:<16d}"\
                .format(0, int(aelec_num), 0, 0)\
                .rstrip()
    str_belec = "{:<7d}{:<6d}{:<16d}{:<16d}"\
                .format(1, int(belec_num), 0, 0)\
                .rstrip()
    f = open(args._f_eig, 'w')
    print >>f, title_str
    print >>f, str_aelec
    print >>f, str_belec
    for i in alpha_eig: print >>f, i
    for i in beta_eig:  print >>f, i
    f.close()
    return


if __name__ == '__main__':
    main()
