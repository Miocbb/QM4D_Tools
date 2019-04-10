#!/usr/bin/env python

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
import inspect
import time


DFA_Gaussian = {'blyp': ['blyp', 'ublyp'],
                'b3lyp': ['b3lyp', 'ub3lyp'],
                'pbe': ['pbepbe', 'upbepbe']
}

Basis_Gaussian = {'STO-3G':  'sto-3g',
                  '3-21G':   '3-21g',
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
    Start_All = time.time()
    parser = argparse.ArgumentParser(description="""Utility for QM4D package. Feed QM4D
    with the density from Gaussian package to speed up SCF process.
    ATTENTION: QM4D CAN ONLY READ DENSITY FILE WITH SUFFIX AS '.TXT'""")
    parser.add_argument('finp', help='input file for QM4D.')
    parser.add_argument('mem', help='mem in GB for g09. E.g. 5GB')
    parser.add_argument('--qm4d', default='qm4d_force', help='qm4d cmd. Default="qm4d_force"')
    parser.add_argument('--dfa', default=None, help='dfa used in Gaussian calculation. Default=the same dfa in qm4d input')
    parser.set_defaults(f_inp_name=None, f_com_name=None,
                        f_dst_name=None, f_chk_name=None,
                        f_log_name=None)
    args = parser.parse_args()

    if not os.path.isfile(args.finp):
        print('Error: "{:s}" file not existed.'.format(args.finp))
        sys.exit(1)

    if args.finp[-4:] != '.inp':
        print('Error: Inp file for QM4D has be *.inp.')
        sys.exit(1)
    else:
        args.f_inp_name = args.finp[:-4]
        args.f_com_name = args.f_inp_name + '.com'
        args.f_log_name = args.f_inp_name + '.log'
        args.f_dst_name = args.f_inp_name + '.txt'
        args.f_chk_name = args.f_inp_name + '.chk'
        args.f_dst_name = qm4d_inp_get_dst_name(args)

    if not args.mem.upper().endswith("GB"):
        if args.mem.upper().endswith("G"):
            args.mem = args.mem.upper() + 'B'
        else:
            print('Error: Memory specification wrong.')
            sys.exit(1)

    if args.dfa:
        if args.dfa not in DFA_Gaussian.keys():
            print("Error: dfa ({:s}) for gaussian calculation is not supportted yet.".format(args.dfa))
            sys.exit(1)

    f = open(args.finp)
    calc_g09 = False
    for line in f:
        if 'guess' in line and 'read' in line:
            calc_g09 = True
    if calc_g09 is False:
        print("Error: no gaussian dst is needed in qm4d inp file.")
        return;
    f.close()

    basis = qm4d_inp_get_basis(args)
    dfa = qm4d_inp_get_dfa(args)
    charge = qm4d_inp_get_charge(args)
    mult = qm4d_inp_get_mult(args)
    xyz_cont = qm4d_inp_get_xyz(args)
    spin = qm4d_inp_get_spin(args)

    write_g09_inp(basis, dfa, charge, mult, spin, xyz_cont, args)

    Start_Gaussian = time.time()
    run_Gaussian(args)
    End_Gaussian = time.time()

    get_gaussian_dst(args)

    Start_QM4D = time.time()
    run_QM4D(args)
    End_QM4D = time.time()

    End_All = time.time()

    print("\n")
    print("           Time Usage Report")
    print("--------------------------------------------")
    print("| Process                 | Wall Time")
    print("|-------------------------------------------")
    print("| Gaussian                | {:f}".format(End_Gaussian - Start_Gaussian))
    print("| QM4D                    | {:f}".format(End_QM4D - Start_QM4D))
    print("| Total                   | {:f}".format(End_All - Start_All))
    print("--------------------------------------------")


def run_Gaussian(args):
    print("*************************")
    print("Output from Gaussian:")
    print("*************************")
    cmd = ' '.join(['g09', args.f_com_name])
    os.system(cmd)
    sys.stdout.flush()

    f = open(args.f_log_name)
    for line in f:
        pass
    lastline = line
    if 'Normal termination' in lastline:
        print("Gaussian terminated normally.")
    else:
        print("Error: Gaussian terminated with error.")
        sys.exit(1)


def run_QM4D(args):
    print("qm4d cmd: ", args.qm4d)
    print("*************************")
    print("Output from QM4D:")
    print("*************************")
    cmd = ' '.join([args.qm4d, args.finp])
    os.system(cmd)
    sys.stdout.flush()


def get_gaussian_dst(args):
    abs_path = os.path.abspath(inspect.stack()[0][1])
    abs_path = os.path.realpath(abs_path)
    formdst_path = '/'.join(abs_path.split('/')[:-2]) + '/read_out/read_density_g09.py'
    print("path of formdst cmd: ",formdst_path)
    cmd = ['/usr/bin/python', formdst_path, args.f_chk_name, '-n', args.f_dst_name]
    p = Popen(cmd, stdout=PIPE, stderr=PIPE)
    stdout, stderr = p.communicate()
    print("*************************")
    print("Output from formdst:")
    print("*************************")
    print(stdout.decode('utf-8'))
    print(stderr.decode('utf-8'))
    sys.stdout.flush()


def write_g09_inp(basis, dfa_qm4d, charge, mult, spin, xyz_cont, args):
    try:
        num_threads = os.environ['OMP_NUM_THREADS']
    except KeyError:
        num_threads = '1'

    if args.dfa:
        dfa = args.dfa
    else:
        dfa = dfa_qm4d

    finp = open(args.f_com_name, 'w')
    finp.write('%chk={:s}\n'.format(args.f_chk_name))
    finp.write('%nprocshared={:s}\n'.format(num_threads))
    finp.write('%mem={:s}\n'.format(args.mem))
    finp.write('#p {:s}/{:s} 6d 10f Int=NoBasisTransform NoSymm\n'.format(DFA_Gaussian[dfa][spin-1], Basis_Gaussian[basis]))
    finp.write('\n')
    finp.write('Gaussian calculation to give converged density\n')
    finp.write('\n')
    finp.write('{:s} {:s}\n'.format(charge, mult))
    for i in xyz_cont:
        cont = i.split()
        finp.write('{:s} {:.8f} {:.8f} {:.8f}\n'.format(cont[0],
            float(cont[1]),float(cont[2]), float(cont[3])))
    finp.write('\n')
    return;


def qm4d_inp_get_spin(args):
    finp = open(args.finp, 'r')
    for line in finp:
        if 'spin' in line:
            spin = line.split()[-1]
            break
    if spin:
        return int(spin)
    else:
        print('Error: no spin is specified.')
        sys.exit(1)


def qm4d_inp_get_dst_name(args):
    finp = open(args.finp, 'r')
    for line in finp:
        if 'guess' in line:
            dst = line.split()[-1]
            break
    if dst:
        return dst
    else:
        print('Error: no density file is specified.')
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
        print('Error: no charge is specified.')
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
            elif cfunc == 'cpbe' and xfunc == 'xpbe':
                dfa = 'pbe'
            elif cfunc == 'b3lyp':
                dfa = 'b3lyp'
            else:
                print("Error: specified DFA in qm4d inp file is not supported for now.")
                exit()
            break
    finp.close()
    if dfa:
        return dfa
    else:
        print("Error: no DFA is specified in QM4D inp file.")


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
            print('Error: more than one basis set is used, not supportted yet.')
            exit()
    else:
        print('Error: no basis is specified.')
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
        print('Error: no xyz file is specifed.')
        exit()


if __name__ == '__main__':
    main()


