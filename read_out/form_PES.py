#!/usr/bin/python

"""
Description:
Use to eigenvalues from DFT calculation to form
Photoemission Spectrum (PES) by Gaussian expanssian

Note:
1. [eig].eig file is required. It is can be created
   by run "read_eig_losc_qm4d.py" script.
2. [spectrum].spec file will be created by this script
   under current execute directory.
3. The peaks of PES is started from a value specified
   by user (which is used to locate the left-most peak)
   and ended at LUMO orbital.

Author: Yuncai Mei
Date:   2017/10/22
"""

import sys
import os.path
import argparse
import math
import numpy as np

def main():
    args = set_parser()
    check_args(args)
    init_args(args)
    # get eigenvalues
    eig_dft, eig_losc = load_eig(args)
    # generate spectrum data
    step  = 0.02

    # standard functional spectrum
    start = math.floor(eig_dft[0]) - 0.5
    end   = math.ceil(eig_dft[-1]) + 0.5
    row   = int((end-start)/step)
    col   = len(eig_dft)
    table_dft = np.zeros((row, col+1), dtype=np.float64)
    for i in range(row):
        x = start + step*i
        table_dft[i, 0] = x
        for j in range(1, col+1):
            table_dft[i,j]=G_distribution(x, eig_dft[j-1], float(args.sigma))

    # losc spectrum
    start = math.floor(eig_losc[0]) - 0.5
    end   = math.ceil(eig_losc[-1]) + 0.5
    row   = int((end-start)/step)
    col   = len(eig_losc)
    table_losc=np.zeros((row, col+1), dtype=np.float64)
    for i in range(row):
        x = start + step*i
        table_losc[i, 0]=x
        for j in range(1, col+1):
            table_losc[i,j]=G_distribution(x, eig_losc[j-1], float(args.sigma))

    # write spectrum file
    f = open(args._f_spec_dft, 'w')
    for i in range(len(table_dft)):
        string = "{:<8.2f}    {:<10f}"\
                .format(table_dft[i,0], 10*np.sum(table_dft[i, 1:]))
        print >>f, string.rstrip()
    f.close()
    f = open(args._f_spec_losc, 'w')
    for i in range(len(table_losc)):
        string = "{:<8.2f}    {:<10f}"\
                .format(table_losc[i,0], 10*np.sum(table_losc[i, 1:]))
        print >>f, string.rstrip()
    f.close()

    print "Created spectrum file: [{:s}] [{:s}]"\
            .format(args._f_spec_dft, args._f_spec_losc)
    return


def SigExit(*string):
    for i in string:
        print i
    sys.exit()


def set_parser():
    """
    Posotional argument
    f_eig: file name for stadard eigenvalue file
    
    Optional argument
    name: file name for specturm file
    start: specified value used to locate left-most peak at PES
    sigma: standard deviation for Gaussian distribution
    """
    parser = argparse.ArgumentParser(description=
            "Generate PhotoEmission Spectrum from DFT "
            "eigenvalues of standard and LOSC functional "
            "by Gaussian expansion.")
    parser.add_argument('f_eig', help='file name for standard eig file')
    parser.add_argument('-name', '-n', dest='f_spec', default=None,
            help='Default=f_eig.spec; file name for spectrum file')
    parser.add_argument('-start', '-s', dest='start', default=-20,
            help='Default=-20; value used to locate left-most peak at PES')
    parser.add_argument('-sigma', dest='sigma', default=0.2,
            help='Default=0.2; standard deviation for Gaussian expansion')
    parser.set_defaults(_f_eig=None, _f_spec_dft=None, _f_spec_losc=None)
    return parser.parse_args()

def check_args(args):
    if not os.path.isfile(args.f_eig):
        SigExit("Terminated: eig file not existed\n")
    elif not args.f_eig.endswith('.eig'):
        SigExit('Terminated: f_eig is not an eig type file\n')
    try:
        float(args.start)
    except ValueError:
        SigExit('Terminated: arg[start] is not a number\n')
    try:
        float(args.sigma)
    except ValueError:
        SigExit('Terminated: arg[sigma] is not a number\n')


def init_args(args):
    args._f_eig = args.f_eig
    if args.f_spec == None:
        args._f_spec_dft = args.f_eig[0:-4] + '.std.spec'
        args._f_spec_losc= args.f_eig[0:-4] + '.losc.spec'
    else:
        args._f_spec_dft = args.f_spec + '.std.spec'
        args._f_spec_losc= args.f_spec + '.losc.spec'


def load_eig(args):
    f_eig = args._f_eig
    f = open(f_eig, 'r')
    eig_origin = np.loadtxt(f_eig, skiprows=1)
    aelec = eig_origin[0,1]
    belec = eig_origin[1,1]
    # extract to alpha LUMO orbital
    eig_dft  = list(eig_origin[2:3+aelec, 2])
    eig_losc = list(eig_origin[2:3+aelec, 3])
    if aelec != belec: # open shell case
        del eig_dft[-1]
        del eig_losc[-1]
        for i in range(2, len(eig_origin)):
            if eig_origin[i, 0] == 1:
                count = i-2
                break
        eig_dft  += list(eig_origin[2+count:3+count+belec, 2])
        eig_losc += list(eig_origin[2+count:3+count+belec, 3])
    eig_dft_select=[]
    eig_losc_select=[]
    for i in range(len(eig_dft)):
        if eig_dft[i] >= float(args.start):
            eig_dft_select.append(eig_dft[i])
    for i in range(len(eig_losc)):
        if eig_losc[i] >= float(args.start):
            eig_losc_select.append(eig_losc[i])
    eig_dft_select.sort()
    eig_losc_select.sort()
    return eig_dft_select, eig_losc_select


def G_distribution(x, miu, sigma):
   return 1/( math.sqrt(2*math.pi)*sigma )\
           * math.exp( -((x-miu)**2)/(2*(sigma**2)) )


if __name__ == '__main__':
    main()
