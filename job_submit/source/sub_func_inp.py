"""
function related to inp file module
"""

import os.path
import os
import sub_claims as s_claims
import sub_func_support as sf_support


def hf_inp(args):
    if args.g09 == True:
        hf_inp_g09(args)
    else:
        hf_inp_qm4d(args)


def dft_inp(args):
    if args.g09 == True:
        dft_inp_g09(args)
    else:
        dft_inp_qm4d(args)


def losc_inp(args):
    #f_inp = args.f_xyz[0:-4] + '.inp'
    f_inp = args._f_inp_name
    f_xyz = args.f_xyz
    basis = s_claims.basis_command_qm4d[args._basis]
    fitbasis = s_claims.basis_command_qm4d[args._fitbasis]
    f = open(f_inp, 'w')
    print >>f, '$qm'
    print >>f, 'xyz    ' + f_xyz
    print >>f, 'spin   ' + args.spin
    if args.aocc == [0,1] and args.bocc == [0,1]:
        print >>f, 'charge ' + args.charge
        print >>f, 'mult   ' + args.mult
    else:
        sf_support.write_occ(f, args)
    print >>f, 'method  dft'
    # write 'dfa' command
    print >>f, s_claims.dfa_xcfunc_qm4d[args.dfa]
    # write 'guess' command
    if args.guess == 'atom':
        print >>f, 'guess  atom'
    else:
        print >>f, 'guess read ' + args.guess
    # write 'POSTSCF' command
    if args.postSCF == '1':
        print >>f, 'POSTSCF LMOSC Boys 1000 1.e-10'
    else:
        print >>f, 'LOSC Boys 1000 1.e-10'
    # write 'LOEnergy' command
    if args.window != '0':
        print >>f, 'LOEnergy  ' + args.window
    # write losc template inp
    print >>f, s_claims.inp_temp_losc
    f.close()
    # write 'basis' and 'fitbasis' command
    element = sf_support.read_elements(args)
    sf_support.write_basis(f_inp, element, basis)
    sf_support.write_fitbasis(f_inp, element, fitbasis)
    f = open(f_inp, 'a')
    print >>f, 'end'
    print >>f, '$doqm'
    f.close()
    # finished writing



def dft_inp_qm4d(args):
    #f_inp = args.f_xyz[0:-4] + '.inp'
    f_inp = args._f_inp_name
    f_xyz = args.f_xyz
    basis = s_claims.basis_command_qm4d[args._basis]
    f = open(f_inp, 'w')
    print >>f, '$qm'
    print >>f, 'xyz    ' + f_xyz
    print >>f, 'spin   ' + args.spin
    if args.aocc == [0,1] and args.bocc == [0,1]:
        print >>f, 'charge ' + args.charge
        print >>f, 'mult   ' + args.mult
    else:
        sf_support.write_occ(f, args)
    print >>f, 'method  dft'
    # write 'xcfunc' command
    print >>f, s_claims.dfa_xcfunc_qm4d[args.dfa]
    # write 'guess' command
    if args.guess == 'atom':
        print >>f, 'guess  atom'
    else:
        print >>f, 'guess read ' + args.guess
    # write DFT template
    print >>f, s_claims.inp_temp
    f.close()
    # write 'basis' command
    element = sf_support.read_elements(args)
    sf_support.write_basis(f_inp, element, basis)
    f = open(f_inp, 'a')
    print >>f, 'end'
    print >>f, '$doqm'
    f.close()
    # finished writing



def dft_inp_g09(args):
    #f_inp = args.f_xyz[0:-4]+ '.com'
    f_com = args._f_com_name
    f_chk = args._f_chk_name
    f_xyz = args.f_xyz
    f_xyz_name = f_xyz[0:-4]
    basis = s_claims.basis_command_g09[args._basis]
    # match 'dfa' command for g09 inp file
    dfa =  s_claims.dfa_xcfunc_g09[args.dfa]
    # generator command line in g09 inp file
    command  = '#p ' + dfa + '/'
    command += basis
    command += ' 6d 10f Int=NoBasisTransform NoSymm'
    # put all g09 ralted files in g09 dir
    if not os.path.isdir('g09'):
        os.makedirs('g09')
    f = open('g09/'+ f_com, 'w')
    print >>f, '%chk=' + f_chk
    print >>f, '%nprocshared=' + args.cpu
    print >>f, '%mem=' + args.mem + 'gb'
    print >>f, command
    print >>f, ''
    print >>f, f_xyz_name
    print >>f, ''
    print >>f, args.charge + ' ' + args.mult
    f.close()
    # write coordinate
    sf_support.write_xyz_g09('g09/' + f_com, f_xyz)
    f = open('g09/' + f_com, 'a')
    print >>f, ''
    f.close()
    # finished writing


def hf_inp_qm4d(args):
    #f_inp = args.f_xyz[0:-4] + '.inp'
    f_inp = args._f_inp_name
    f_xyz = args.f_xyz
    basis = s_claims.basis_command_qm4d[args._basis]
    f = open(f_inp, 'w')
    print >>f, '$qm'
    print >>f, 'xyz    ' + f_xyz
    print >>f, 'spin   ' + args.spin
    if args.aocc == [0,1] and args.bocc == [0,1]:
        print >>f, 'charge ' + args.charge
        print >>f, 'mult   ' + args.mult
    else:
        sf_support.write_occ(f, args)
    print >>f, 'method  hf'
    # write 'guess' command
    if args.guess == 'atom':
        print >>f, 'guess  atom'
    else:
        print >>f, 'guess read ' + args.guess
    # write template
    print >>f, s_claims.inp_temp
    f.close()
    # write 'basis' command
    element = sf_support.read_elements(args)
    sf_support.write_basis(f_inp, element, basis)
    f = open(f_inp, 'a')
    print >>f, 'end'
    print >>f, '$doqm'
    f.close()
    # finished writing



def hf_inp_g09(args):
    #f_inp = args.f_xyz[0:-4]+ '.com'
    f_com = args._f_com_name
    f_chk = args._f_chk_name
    f_xyz = args.f_xyz
    f_xyz_name = args.f_xyz[0:-4]
    basis = s_claims.basis_command_g09[args._basis]
    # generate command line in g09 inp file
    command  = '#p ' + 'hf/'
    command += basis
    command += ' 6d 10f Int=NoBasisTransform NoSymm'
    # collect all g09 related files in g09 dir
    if not os.path.isdir('g09'):
        os.makedirs('g09')
    f = open('g09/'+f_com, 'w')
    print >>f, '%chk=' + f_chk
    print >>f, '%nprocshared=' + args.cpu
    print >>f, '%mem=' + args.mem + 'gb'
    print >>f, command
    print >>f, ''
    print >>f, f_xyz_name
    print >>f, ''
    print >>f, args.charge + ' ' + args.mult
    f.close()
    # write coordinates
    sf_support.write_xyz_g09('g09/' + f_com, f_xyz)
    f = open('g09/' + f_com, 'a')
    print >>f, ''
    f.close()
    # finished writing

#*************************
if __name__ == "__main__":
    print count_elec_num('1.xyz')

