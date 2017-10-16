"""
supporting functions for Project 'job_submit'
"""
import sys
import os
import os.path
import argparse
import sub_claims as s_claims

def check_position_args(args):
    """
    check if the positional args are valid
    """
    if os.path.isfile(args.f_xyz) != True:
        SigExit("Terminated: coordinate file not existed!\n")
    if args.f_xyz.endswith('.xyz') != True:
        SigExit("Terminated: not a coordinate file\n")
    if args.partition not in s_claims.partition_name:
        SigExit("Terminated: not a partition name\n")
 

def check_optional_arg(args):
    """
    check if the optional args are valid;
    """
    if args.spin not in {'1','2'}:
        SigExit("Terminated: arg[spin] not in {1,2}\n")
    if args.mult.isdigit() != True:
        SigExit("Terminated: arg[mult] not non-negative\n")
    if args.guess != 'atom' and \
       os.path.isfile(args.guess) != True:
            SigExit("Terminated: guess file not existed!\n")
    if args.cpu.isdigit() != True:
        SigExit("Terminated: arg[cpu] not a non-negative integer\n")
    elif int(args.cpu) >16:
        SigExit("Terminated: arg[cpu] bigger than 16\n")
    if args.mem.isdigit() != True:
        SigExit("Terminated: arg[mem] not a non-negative integer\n")
    else:
        check_mem(args)

    # DFT and LOSC DFT args check
    if args._method in {'dft', 'losc'}:
        if not args.g09: # choose qm4d
            if args.dfa not in s_claims.dfa_qm4d:
                SigExit("Terminated: functional not supported in qm4d\n")
        else: # choose g09
            if args.dfa not in s_claims.dfa_g09:
                SigExit("Terminated: functional not supported in g09\n")
    # LOSC args check
    if args._method == 'losc':
        if args.postSCF not in {'0', '1'}:
            SigExit("Terminated: arg[postSCF] not in {0, 1}\n")
        if len( args.window.split() ) > 2:
            SigExit("Terminated: arg[window] at most 2 nums\n")
        elif len( args.window.split() ) == 1\
                and args.window != '0':
            SigExit("Terminated: arg[window]=0 to disable LOEnergy\n")

def init_args_f_name(args):
    f_xyz_name = args.f_xyz[0:-4]
    # inp or com file name initial
    if args.inp_name == '-1': # init default name for inp file
        args._f_inp_name = f_xyz_name + '.inp'
        args._f_com_name = f_xyz_name + '.com'
        args._f_chk_name = f_xyz_name + '.chk'
    else:
        args._f_inp_name = args.inp_name + '.inp'
        args._f_com_name = args.inp_name + '.com'
        args._f_chk_name = args.inp_name + '.chk'
    # out file name inital
    if args.out_name == '-1': # init default name for out file
        args._f_out_name = args._f_inp_name[0:-4] + '.out'
    else:
        args._f_out_name = args.out_name
    # slurm file name initial
    if args.slurm_name == '-1': # init defaul name for slurm file
        args._f_slurm_name = 'slurm'
    else:
        args._f_slurm_name = args.slurm_name

def init_args_slurm_val(args):
    f_xyz_name = args.f_xyz[0:-4]
    if args.job_name == '-1': # init default job_name in slurm
        args._job_name = f_xyz_name + '.' + args._method
    else:
        args._job_name = args.job_name


def check_mem(args):
    """
    check if args[mem] is valid or not
    """
    if int(args.mem) > s_claims.partition_mem[args.partition]:
        SigExit('Terminated: arg[mem] oversize, max={}G\n'.\
             format(s_claims.partition_mem[args.partition]))



def read_elements(f_xyz):
    """
    read out the elements from xyz file;
    reading is based on the coordinates line;

    return:  list elements[];
    """
    element = []
    f =open(f_xyz)
    count = 0
    for line in f:
        line_split = line.split()
        if len(line_split) > 0: #skip the emmty line
            if line_split[0].startswith('#') != True:
                count += 1
            if count >= 3: # start read the element
                if len(line_split[0]) >= 3:
                    element.append(line_split[0][0:2])
                else:
                    element.append(line_split[0])
    return list(set(element))



def write_basis(f_inp, element, basis):
    """
    write 'basis' command for qm4d inp file

    f_inp: qm4d inp file
    element[]: list of elements of the system
    basis: basis string
    """
    f = open(f_inp, 'a')
    for i in element:
        string = 'basis    ' + i + ' ' + i + '.' + basis + '\n'
        f.write(string)
    f.close()


def write_fitbasis(f_inp, element, basis):
    """
    write 'fitbasis' command for qm4d inp file

    f_inp: qm4d inp file
    element[]: list of elements of the system
    basis: fitbasis string
    """
    f = open(f_inp, 'a')
    for i in element:
        string = 'fitbasis ' + i + ' ' + i + '.' + basis + '\n'
        f.write(string)
    f.close()


def write_xyz_g09(f_inp, f_xyz):
    """
    write coordinates line for g09 inp file

    f_inp: g09 inp file
    f_xyz: xyz file
    """
    f1 =open(f_inp, 'a')
    f2 =open(f_xyz)
    count = 0
    for line in f2:
        line_split = line.split()
        if len(line_split) > 0: #skip the emmty line
            if line_split[0].startswith('#') != True:
                count += 1
            if count >= 3: # start write coordinates
                # check if coordinate is complete
                if len(line_split) != 4:
                    print "terminated: xyz file missing data for coordinates"
                    sys.exit()
                # screen coordinate data to be float
                # required by g09 inp file
                line = '{:<3} {:<10f} {:<10f} {:<10f}'.format(line_split[0],\
                        float(line_split[1]), float(line_split[2]),
                        float(line_split[3]))
                f1.write(line + '\n')
    f1.close()
    f2.close()

def count_elec_num(args):
    """
    count the total electron number of the input system
    """
    f_xyz = args.f_xyz
    # collect the list of all the element
    element = []
    f =open(f_xyz)
    count = 0
    for line in f:
        line_split = line.split()
        if len(line_split) > 0: #skip the emmty line
            if line_split[0].startswith('#') != True:
                count += 1
            if count >= 3: # start read the element
                if len(line_split[0]) >= 3:
                    element.append(line_split[0][0:2])
                else:
                    element.append(line_split[0])
    # start count electron num
    elec_num = 0
    for i in element:
        elec_num += s_claims.element_table[i]
    elec_num += int(args.charge)
    return elec_num

def auto_set_mem(args, elec_num):
    if elec_num > 560:
        print "warning: system too large, 30G mem required, use mei2_medmem or above"
    if args.mem == '-1': # using default mem setting
        args.mem = str( (elec_num/40) * 2 + 2 )


def auto_set_mult(args, elec_num):
    """
    set the 'mult' command based on total elec_num
    odd:  mult=2
    even: mult=1
    """
    if args.mult == '-1': # using default mult setting
        args.mult = str(elec_num % 2 + 1)


def SigExit(string):
    print string
    sys.exit()


