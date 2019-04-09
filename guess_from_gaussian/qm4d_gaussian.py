#!/usr/bin/evn python

""" 
Utility for qm4d package. Calculate with Gaussian package first, 
then feed qm4d with the density from Gaussian.

Yuncai Mei
2019/04/09
"""

import argparse
import os.path
import sys
import subprocess as subp
from subprocess import Popen, PIPE
import os


DFA_Gaussian = {'blyp': 'blyp',
                'b3lyp': 'b3lyp',
                'lda': 'lsda',
                'pbe': 'pbepbe'
}

Basis_Gaussian = {'STO-3G':  'sto-3g',
                  '6-31G':   '6-31g',
                  '6-31GS':  '6-31g*',
                  '6-31GSS': '6-31g**',
                  '6-311GS': '6-311g*',
                  '6-311++G_3df_3pd': '6-311++g(3df,3pd)',
                  'cc-pVDZ': 'cc-pVDZ',
                  'cc-pVTZ': 'cc-pVTZ',
                  'aug-cc-pVDZ': 'aug-cc-pVDZ',
                  'aug-cc-pVTZ': 'aug-cc-pVTZ',
}


def main():
    parser = argparse.ArgumentParser(description="""Utility for QM4D package. Feed QM4D
    with the density from Gaussian package to speed up SCF process.""")
    parser.add_argument('finp', help='input file for QM4D.')
    parser.add_argument('--ncpu', help='number of cpus.')
    parser.add_argument('--qm4d', help='command for qm4d. Default="qm4d_force"')
    args = parser.parse_args()

    if not os.path.isfile(args.finp):
        print('Error: "{:s}" file not existed.'.format(args.finp))
        exit()

    basis = qm4d_inp_get_basis(args)
    dfa = qm4d_inp_get_dfa(args)
    charge = qm4d_inp_get_charge(args)
    mult = qm4d_inp_get_mult(args)
    xyz_cont = qm4d_inp_get_xyz(args)
    dst = qm4d_inp_get_dst_name(args)


    write_g09_inp(basis, dfa, charge, mult, xyz_cont, args)

    run_Gaussian(args)

    get_gaussian_dst(args)


def run_Gaussian(args):  
    cmd = ['g09', 'tem.com']
    p = Popen(cmd, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()

def run_QM4D(args):  
    cmd = [args.qm4d, 'tem.com']
    p = Popen(cmd, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()


def get_gaussian_dst(args):
    cmd = ['/usr/bin/python', '../read_out/read_density_g09.py', '-n', 'tem.dst']
    p = Popen(cmd, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()


def write_g09_inp(basis, dfa, charge, mult, xyz_cont, args):
    try:
        num_threads = os.environ['OMP_NUM_THREADS']
    except KeyError:
        num_threads = '1'

    finp = open('tem.com', 'w')
    finp.write('%chk=tem.chk\n')
    finp.write('%nprocshared={s}\n'.format(num_threads))
    finp.write('%mem=29G\n')
    finp.write('#p {s}/{s} 6d 10f Int=NoBasisTransform NoSymm\n'.format(DFA_Gaussian[dfa], Basis_Gaussian[basis]))
    finp.wirte('\n')
    finp.wirte('tem file to give gaussian density\n')
    finp.wirte('\n')
    finp.wirte('{s} {s}\n'.format(charge, mult))
    for i in xyz_cont:
        finp.write(i)
    finp.write('\n')
    return;


def qm4d_inp_get_dst_name(args):
    finp = open(args.finp, 'r')
    for line in finp:
        if 'guess' in line:
            dst = line.split()[-1]
            break
    if dst:
        return dst
    else:
        print('Error: no density file is specified.\n')
        sys.exit(1)


def qm4d_inp_get_charge(args):
    finp = open(args.finp, 'r')
    for line in finp:
        if 'charge' in line:
            charge = line.split()[-1]
            break
    if charge:
        return charge
    else:
        print('Error: no charge is specified.\n')
        sys.exit(1)

def qm4d_inp_get_mult(args):
    finp = open(args.finp, 'r')
    for line in finp:
        if 'mult' in line:
            mult = line.split()[-1]
            break
    if mult:
        return mult
    else:
        print('Error: no mult is specified.\n')
        sys.exit(1)


def qm4d_inp_get_dfa(args):
    finp = open(args.finp, 'r')
    for line in finp:
        if 'xfunc' in line:
            xfunc = line.split()[-1]
            break

    finp.seek(0)

    for line in finp:
        if 'cfunc' in line:
            cfunc = line.split()[-1]
            if cfunc == 'clyp' and xfunc == 'xb88':
                dfa = 'blyp'
            elif cfunc == 'clda' and xfunc == 'xlda':
                dfa = 'lda'
            elif cfunc == 'xpbe' and xfunc == 'xpbe':
                dfa = 'pbe'
            elif cfunc == 'b3lyp':
                dfa = 'b3lyp'
            else:
                print("Error: specified DFA in qm4d inp file is not supported for now.\n")
                exit()
            break
    finp.close()
    if dfa:
        return dfa
    else:
        print("Error: no DFA is specified in QM4D inp file.\n")


def qm4d_inp_get_basis(args):
    finp = open(args.finp, 'r')
    basis = []
    for line in finp:
        if 'basis' in line:
            basis_t = line.split()[-1].split('.')[-1]
            basis.append(basis_t)
    basis = list(set(basis))
    if basis:
        if len(basis) == 1:
            return basis[0]
        else:
            print('Error: more than one basis set is used, not supportted yet.\n')
            exit()
    else:
        print('Error: no basis is specified.\n')
        exit()


def qm4d_inp_get_xyz(args):
    finp = open(args.finp, 'r')
    for line in finp:
        if 'xyz' in line:
            fxyz = line.split()[-1]
            break
    finp.close()

    if os.path.isfile(fxyz):
        return open(fxyz, 'r').readlines()[2:]
    else:
        print('Error: no xyz file is specifed.\n')
        exit()

if __name__ == '__main__':
    main()


