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
    if not is_integer(args.charge):
        SigExit("Terminated: arg[charge] not integer\n")
    elif float(args.charge) > (args._elec_num + float(args.charge)):
        SigExit("Terminated: arg[charge] too large\n")
    if not args.aelec[1] <= 1:
        SigExit("Terminated: arg[aelec] not <= 1\n")
    if not args.belec[1] <= 1:
        SigExit("Terminated: arg[belec] not <= 1\n")
    if not args.mult.isdigit():
        SigExit("Terminated: arg[mult] not non-negative\n")
    if args.guess != 'atom' and \
       os.path.isfile(args.guess) != True:
            SigExit("Terminated: guess density file not existed!\n")
    if not args.cpu.isdigit():
        SigExit("Terminated: arg[cpu] not a non-negative integer\n")
    elif int(args.cpu) >16:
        SigWarring(args, "Terminated: arg[cpu] > 16\n")
    if not is_positive_int(args.mem):
        SigExit("Terminated: arg[mem] not a positive integer\n")
    else:
        check_mem(args)

    # DFT args check
    if args._method == 'dft':
        if not args.g09: # choose qm4d
            if args.dfa not in s_claims.dfa_qm4d:
                SigExit("Terminated: functional not supported in qm4d",
                        "functional choice:", s_claims.dfa_qm4d)
        else: # choose g09
            if args.dfa not in s_claims.dfa_g09:
                SigWarring(args, "Warning: functional not supported in g09",
                        "functional choice:", s_claims.dfa_g09)
    # LOSC args check
    if args._method == 'losc':
        if args.dfa not in s_claims.dfa_qm4d:
            SigExit("Terminated: functional not supported in qm4d",
                    "functional choice:", s_claims.dfa_qm4d)
        if args.postSCF not in {'0', '1'}:
            SigExit("Terminated: arg[postSCF] not in {0, 1}\n")
        if len( args.window.split() ) > 2:
            SigExit("Terminated: arg[window] at most 2 nums\n")
        elif len( args.window.split() ) == 1\
                and args.window != '0':
            SigExit("Terminated: arg[window] has to be 0 to disable LOEnergy\n")

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
        args._f_out_name = args.out_name + '.out'
    # slurm file name initial
    if args.slurm_name == '-1': # init defaul name for slurm file
        args._f_slurm_name = 'slurm'
    else:
        args._f_slurm_name = args.slurm_name

def init_args_slurm_val(args):
    f_xyz_name = args.f_xyz[0:-4]
    if args.job_name == '-1': # init default job_name in slurm
        args._job_name = f_xyz_name + '.' + args._method
        if args._method in {'dft', 'losc'}:
            args._job_name = args._job_name + '.' + args.dfa
    else:
        args._job_name = args.job_name


def init_args_basis(args):
    args._basis = args.basis.upper()
    if args._basis not in s_claims.basis_input_option:
        SigWarring(args, "Warning: basis not in normal options")
        s_claims.basis_command_qm4d.update({args._basis:args.basis})
        s_claims.basis_command_g09.update({args._basis:args.basis})
        s_claims.basis_mem_level.update({args._basis:1})
    if args._method == 'losc':
        args._fitbasis = args.fitbasis.upper()
        if args._fitbasis not in s_claims.basis_input_option:
            SigWarring(args, "Warning: fitbasis not in normal options")
            s_claims.basis_command_qm4d.update({args._fitbasis:args.fitbasis})

def init_args_abelec(args):
    aelec = args.aelec
    belec = args.belec
    try:
        aelec[0] = int(aelec[0])
        aelec[1] = float(aelec[1])
    except:
        SigExit("Terminated: arg[aelec] invalid. aelec=[int, float]\n")
    try:
        belec[0] = int(belec[0])
        belec[1] = float(belec[1])
    except:
        SigExit("Terminated: arg[aelec] invalid. aelec=[int, float]\n")


def check_mem(args):
    """
    check if args[mem] is valid or not
    """
    if int(args.mem) > s_claims.partition_mem[args.partition]:
        SigExit('Terminated: arg[mem] oversize, mem={}, max_mem={}G\n'
                .format(args.mem, s_claims.partition_mem[args.partition]))


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

def write_occ(f, args):
    """
    f: the opened inp file
    write 'guess occ' command for QM4D inp file
    """
    elec_num = args._elec_num
    aelec_num = elec_num/2 + elec_num % 2
    belec_num = elec_num/2
    aelec = args.aelec
    belec = args.belec
    # set real elec_num for spin alpha and beta
    if aelec[0] <= 0:
        real_aelec_num = aelec_num -1 + aelec[1]
    else:
        real_aelec_num = aelec_num + aelec[1]
    if belec[0] <= 0:
        real_belec_num = belec_num -1 + belec[1]
    else:
        real_belec_num = belec_num + belec[1]
    if real_aelec_num < real_belec_num:
        SigExit("Terminated: aelec < belec\n")
    a_occ = aelec_num
    b_occ = belec_num
    # check aelec and belec
    if (a_occ+aelec[0]) <= 0:
        SigExit("Terminated: aelec[position] too negative, a_occ<=0\n")
    if (b_occ+belec[0]) <= 0:
        SigExit("Terminated: belec[position] too negative, b_occ<=0\n")
    # set alpha and beta occupation
    if aelec[0] > 0: # occ at LUMO or above
        a_occ += aelec[0]
    if belec[0] > 0: # occ at LUMO or above
        b_occ += belec[0]
    # write 'aelec' and 'belec' command
    print >>f, 'aelec  ' + str(real_aelec_num)
    print >>f, 'belec  ' + str(real_belec_num)
    # print ruler line for alpha occ
    string = ''
    for i in range(10):
        if i == aelec_num + aelec[0] - 1:
            length = len(str(aelec[1]))
            string += str(i)
            for j in range(length):
                string += ' '
        else:
            string += str(i) + ' '
    print >>f, '#************************'+string
    # write 'guess occ set alpha' command
    string = ''
    for i in range(a_occ):
        if i == aelec_num + aelec[0] - 1:
            string = string + str(aelec[1]) + ' '
        elif i > aelec_num - 1:
            string += '0 '
        else:
            string += '1 '
    print >>f, 'guess occ set alpha {:<5d}'.format(a_occ)\
            + string
   # write 'guess occ set beta' command
    string = ''
    for i in range(b_occ):
        if i == belec_num + belec[0] - 1:
            string = string + str(belec[1]) + ' '
        elif i > belec_num - 1:
            string += '0 '
        else:
            string += '1 '
    print >>f, 'guess occ set beta  {:<5d}'.format(b_occ)\
            + string
    # print ruler line for beta occ
    string = ''
    for i in range(10):
        if i == belec_num + belec[0] - 1:
            length = len(str(belec[1]))
            string += str(i)
            for j in range(length):
                string += ' '
            #string += str(belec[1]) + ' '
        else:
            string += str(i) + ' '
    print >>f, '#************************'+string
 

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
    elec_num -= float(args.charge)
    args._elec_num = int(elec_num)

def auto_set_mem(args):
    """
    memory requst is based on the total number of
    system electron and used basis set.
    40 electron is request 2G memory with cc-pVTZ basis.
    With other customized basis, the request memory has
    to time a corresponding factor.
    """
    elec_num = args._elec_num
    if args.mem == '-1': # using default mem setting
        memory = (int(elec_num)/40) * 2 + 2
        memory *= s_claims.basis_mem_level[args._basis]
        args.mem = str( memory )
    if int(args.mem) > 30:
        SigWarring(args, "Warning: request mem {} > 30G".
                    format(args.mem))


def auto_set_mult(args):
    """
    set the 'mult' command based on total elec_num
    odd:  mult=2
    even: mult=1
    """
    elec_num = args._elec_num
    if args.mult == '-1': # using default mult setting
        args.mult = str(int(elec_num) % 2 + 1)
    #if elec_num != int(elec_num):
    #    SigWarring(args, "Warning: fractional charged case, reset '-mult'")


def SigExit(*string):
    for i in string:
        print i
    sys.exit()

def SigWarring(args, *string):
    for i in string:
        print i
    args._sys_warning = 1

def is_number(string):
    """
    check string represent number or not.
    +3.14: True
    -3.14: True
    3: True
    """
    test = string.replace('+','',1).replace('-','',1).\
            replace('.','',1)
    return test.isdigit()

def is_integer(string):
    """
    int and float sign and unsigned integer is checked as True
    3 3.0 +3 +3.0: True
    """
    if is_number(string):
        return int(float(string)) == float(string)
    return False

def is_positive_int(string):
    """
    check string represents non negative integer or not.
    +3 (3): True;
    +3.0 (3.0): False
    """
    if not is_number(string):
        return False
    test = string.replace('+','',1)
    if test.isdigit():
        if int(test)>0:
            return True
        else:
            return False
    else:
        return False 
