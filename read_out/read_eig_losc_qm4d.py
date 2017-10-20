#!/usr/bin/python
"""
Description:
1. This is python script is used to extract all the eigenvales
from losc functional calculation by QM4D.
2. [eig].eig file is created under the dir of current execute
path.
3. The format of [eig].eig file is sperated columns, shown as
below:
"spin    orbital    eig_prev    eig_losc"

Note:
1. qm4d.out output file is required to execute this script

Work flow:
qm4d.out check normal terminated --> [eig].eig

Author: Yuncai Mei
Date:   2017/10/20
"""

import sys
import os.path
import argparse
from subprocess import Popen, PIPE

def SigExit(*string):
    for i in string:
        print i
    sys.eixt()

def set_parser():
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

def check_normal_termination(args):
    """
    check is qm4d.out file is termianted normally
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
    f_out = args._f_out
    partern = 'Alpha electron'
    f = open(f_out, 'r')
    for line in f:
        if partern in line:
            rst = line.split()
            f.close()
            return rst[3], rst[7]
    f.close()
    SigExit('Terminated: no electron info find\n')


def extract_eig(args):
    f_out = args._f_out
    aelec, belec = read_elec_num(args)
    match_line = []
    partern = 'eig_proj'
    f = open(f_out, 'r')
    for line in f:
        if partern in line:
            #item = line.replace('=', ' ').split()
            match_line.append( line.replace('=', ' ').split() )
    f.close()
    #print match_line
    alpha_eig = []
    beta_eig  = []
    eig = {'0': [], '1':[]}
    for item in match_line:
            string = "{:<7s}{:<6s}{:<16s}{:<16s}"\
                    .format(item[1], item[3], item[5], item[7])
            eig[item[1]].append(string)
    #print eig['0'], eig['1']
    return eig['0'], eig['1']


def main():
    args = set_parser()
    init_args(args)
    print args
    if not check_normal_termination(args):
        SigExit("Terminated: qm4d.out not normal terminated\n")
    alpha_eig, beta_eig = extract_eig(args)
    
    f = open(args._f_eig, 'w')
    eig_format = "{:<7s}{:<6s}{:<16s}{:<16s}".format('spin', 'orb',
            'eig_prev','eig_losc')
    print >>f, eig_format
    for i in alpha_eig: print >>f, i
    for i in beta_eig:  print >>f, i
    f.close()
    return


if __name__ == '__main__':
    main()
