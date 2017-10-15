
import sys
import os.path
import os
import sub_claims
import sub_func_slurm as sfs #supporting funcs for writing slurm file


def hf_main(args):
    """
    hf calculation main function
    """
    hf_inp(args)
    sfs.hf_slurm(args)
    sfs.sbatch(args)
    print 'job submitted.'


def dft_main(args):
    """
    standard dft calculation main function
    """
    dft_inp(args)
    sfs.dft_slurm(args)
    sfs.sbatch(args)
    print 'job submitted.'


def losc_main(args):
    """
    DFT with losc functional main function
    """
    losc_inp(args)
    sfs.losc_slurm(args)
    sfs.sbatch(args)
    print 'job submitted.'


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
    f_inp = args.f_xyz[0:-4] + '.inp'
    f_xyz = args.f_xyz
    f = open(f_inp, 'w')
    print >>f, '$qm'
    print >>f, 'xyz    ' + f_xyz
    print >>f, 'spin   ' + args.spin
    print >>f, 'charge ' + args.charge
    print >>f, 'mult   ' + args.mult
    print >>f, 'method  dft'
    # write 'dfa' command
    print >>f, sub_claims.dfa_xcfunc_qm4d[args.dfa]
    # write 'guess' command
    if args.guess == 'atom':
        print >>f, 'guess  atom'
    else:
        print >>f, 'guess read ' + args.guess
    # write 'POSTSCF' command
    if args.postSCF == '1':
        print >>f, 'POSTSCF LMOSC Boys 1000 1.e-10'
    else:
        print >>f, 'SCF LOSC !!!!!!!!!!!!!!'
    # write 'LOEnergy' command
    if args.window != '0':
        print >>f, 'LOEnergy  ' + args.window
    # write losc template inp
    print >>f, sub_claims.inp_temp_losc
    f.close()
    # write 'basis' and 'fitbasis' command
    element = read_elements(args.f_xyz)
    write_basis(f_inp, element, args.basis)
    write_fitbasis(f_inp, element, args.fitbasis)
    f = open(f_inp, 'a')
    print >>f, 'end'
    print >>f, '$doqm'
    f.close()
    # finished writing



def dft_inp_qm4d(args):
    f_inp = args.f_xyz[0:-4] + '.inp'
    f_xyz = args.f_xyz
    f = open(f_inp, 'w')
    print >>f, '$qm'
    print >>f, 'xyz    ' + f_xyz
    print >>f, 'spin   ' + args.spin
    print >>f, 'charge ' + args.charge
    print >>f, 'mult   ' + args.mult
    print >>f, 'method  dft'
    # write 'xcfunc' command
    print >>f, sub_claims.dfa_xcfunc_qm4d[args.dfa]
    # write 'guess' command
    if args.guess == 'atom':
        print >>f, 'guess  atom'
    else:
        print >>f, 'guess read ' + args.guess
    # write DFT template
    print >>f, sub_claims.inp_temp
    f.close()
    # write 'basis' command
    element = read_elements(args.f_xyz)
    write_basis(f_inp, element, args.basis)
    f = open(f_inp, 'a')
    print >>f, 'end'
    print >>f, '$doqm'
    f.close()
    # finished writing



def dft_inp_g09(args):
    f_inp = args.f_xyz[0:-4]+ '.com'
    f_xyz = args.f_xyz
    f_name = args.f_xyz[0:-4]
    # match 'dfa' command for g09 inp file
    dfa =  sub_claims.dfa_xcfunc_g09[args.dfa]
    # generator command line in g09 inp file
    command  = '# ' + dfa + '/'
    command += args.basis
    command += ' 6d 10f Int=NoBasisTransform NoSymm'
    # put all g09 ralted files in g09 dir
    if not os.path.isdir('g09'):
        os.makedirs('g09')
    f = open('g09/'+f_inp, 'w')
    print >>f, '%chk=' + f_name + '.chk'
    print >>f, '%nprocshared=' + args.cpu
    print >>f, '%mem=' + args.mem + 'gb'
    print >>f, command
    print >>f, ''
    print >>f, f_name
    print >>f, ''
    print >>f, args.charge + ' ' + args.mult
    f.close()
    # write coordinate
    write_xyz_g09('g09/'+f_inp, f_xyz)
    f = open('g09/' + f_inp, 'a')
    print >>f, ''
    f.close()
    # finished writing


def hf_inp_qm4d(args):
    f_inp = args.f_xyz[0:-4] + '.inp'
    f_xyz = args.f_xyz
    f = open(f_inp, 'w')
    print >>f, '$qm'
    print >>f, 'xyz    ' + f_xyz
    print >>f, 'spin   ' + args.spin
    print >>f, 'charge ' + args.charge
    print >>f, 'mult   ' + args.mult
    print >>f, 'method  hf'
    # write 'guess' command
    if args.guess == 'atom':
        print >>f, 'guess  atom'
    else:
        print >>f, 'guess read ' + args.guess
    # write template
    print >>f, sub_claims.inp_temp
    f.close()
    # write 'basis' command
    element = read_elements(args.f_xyz)
    write_basis(f_inp, element, args.basis)
    f = open(f_inp, 'a')
    print >>f, 'end'
    print >>f, '$doqm'
    f.close()
    # finished writing



def hf_inp_g09(args):
    f_inp = args.f_xyz[0:-4]+ '.com'
    f_xyz = args.f_xyz
    f_name = args.f_xyz[0:-4]
    # generate command line in g09 inp file
    command  = '# ' + 'hf/'
    command += args.basis
    command += ' 6d 10f Int=NoBasisTransform NoSymm'
    # collect all g09 related files in g09 dir
    if not os.path.isdir('g09'):
        os.makedirs('g09')
    f = open('g09/'+f_inp, 'w')
    print >>f, '%chk=' + f_name + '.chk'
    print >>f, '%nprocshared=' + args.cpu
    print >>f, '%mem=' + args.mem + 'gb'
    print >>f, command
    print >>f, ''
    print >>f, f_name
    print >>f, ''
    print >>f, args.charge + ' ' + args.mult
    f.close()
    # write coordinates
    write_xyz_g09('g09/'+f_inp, f_xyz)
    f = open('g09/' + f_inp, 'a')
    print >>f, ''
    f.close()
    # finished writing

def check_arg(args):
    """
    check if the parse args are valid;
    """
    # key args check
    # args.[f_xyz, partition, spin, mult, \
    #       guess, cpu, mem, method]
    if os.path.isfile(args.f_xyz) != True:
        print "Terminated: coordinate file not existed!\n"
        sys.exit()
    if args.f_xyz.endswith('.xyz') != True:
        print "Terminated: not a coordinate file\n"
        sys.exit()
    if args.partition not in sub_claims.partition_name:
        print "Terminated: not a partition name\n"
        sys.exit()
    if args.spin not in {'1','2'}:
        print "Terminated: arg[spin] not in {1,2}\n"
        sys.exit()
    if args.mult.isdigit() != True:
        print "Terminated: arg[mult] not non-negative\n"
        sys.exit()
    if args.guess != 'atom' and \
       os.path.isfile(args.guess) != True:
        print "Terminated: guess file not existed!\n"
        sys.exit()
    if args.cpu.isdigit() != True:
        print "Terminated: arg[cpu] not a non-negative integer\n"
        sys.exit()
    elif int(args.cpu) >16:
        print "Terminated: arg[cpu] bigger than 16\n"
        sys.exit()
    if args.mem.isdigit() != True:
        print "Terminated: arg[mem] not a non-negative integer\n"
        sys.exit()
    else:
        check_mem(args)

    # DFT and LOSC DFT args check
    if args.method in {'dft', 'losc'}:
        if args.dfa not in {'b3lyp', 'blyp', 'lda', 'pbe'}:
            print "Terminated: choose a wrong functional!\n"
            sys.exit()
    # LOSC args check
    if args.method == 'losc':
        if args.postSCF not in {'0', '1'}:
            print "Terminated: arg[postSCF] not in {0, 1}\n"
            sys.exit()
        if len( args.window.split() ) > 2:
            print "Terminated: arg[window] at most 2 nums\n"
            sys.exit()
        elif len( args.window.split() ) == 1\
                and args.window != '0':
            print "Terminated: arg[window]=0 to disable LOEnergy\n"
            sys.exit()



def check_mem(args):
    """
    check if args[mem] is valid or not
    """
    if int(args.mem) > sub_claims.partition_mem[args.partition]:
        print 'Terminated: arg[mem] oversize, max={}G\n'.\
                format(sub_claims.partition_mem[args.partition])
        sys.exit()



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
                f1.write(line)
    f1.close()
    f2.close()



#*************************
if __name__ == "__main__":
    print read_elements('1.xyz')


