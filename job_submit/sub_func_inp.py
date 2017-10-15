
import sys
import os.path
import os
import sub_claims


def dft_inp(args):
    if args.g09 == True:
        dft_inp_g09(args)
    else:
        dft_inp_qm4d(args)

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

    if args.dfa == 'blyp':
        print >>f, 'xfunc  xb88'
        print >>f, 'cfunc  clyp'
    elif args.dfa == 'pbe':
        print >>f, 'xfunc  xpbe'
        print >>f, 'cfunc  cpbe'
    elif args.dfa == 'lda':
        print >>f, 'xfunc  xlda'
        print >>f, 'cfunc  clda'
    elif args.dfa == 'b3lyp':
        print >>f, 'xcfunc b3lyp'

    if args.guess == 'atom':
        print >>f, 'guess  atom'
    else:
        print >>f, 'guess read ' + args.guess

    print >>f, claims.inp_temp
    f.close()
    element = read_elements(args.f_xyz)
    write_basis(f_inp, element, args.basis)
    f = open(f_inp, 'a')
    print >>f, 'end'
    print >>f, '$doqm'
    f.close()


def dft_inp_g09(args):
    f_inp = args.f_xyz[0:-4]+ '.com'
    f_xyz = args.f_xyz
    f_name = args.f_xyz[0:-4]
    dfa = args.dfa

    if args.dfa == 'pbe':
        dfa = 'pbepbe'
    elif args.dfa == 'lda':
        dfa = 'lsda'

    command  = '# ' + dfa + '/'
    command += args.basis
    command += ' 6d 10f Int=NoBasisTransform NoSymm'

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

    write_xyz_g09('g09/'+f_inp, f_xyz)
    f = open('g09/' + f_inp, 'a')
    print >>f, ''
    f.close()


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
    
    if args.dfa == 'blyp':
        print >>f, 'xfunc  xb88'
        print >>f, 'cfunc  clyp'
    elif args.dfa == 'pbe':
        print >>f, 'xfunc  xpbe'
        print >>f, 'cfunc  cpbe'
    elif args.dfa == 'lda':
        print >>f, 'xfunc  xlda'
        print >>f, 'cfunc  clda'
    elif args.dfa == 'b3lyp':
        print >>f, 'xcfunc b3lyp'
    if args.guess == 'atom':
        print >>f, 'guess  atom'
    else:
        print >>f, 'guess read ' + args.guess
    if args.postSCF == '1':
        print >>f, 'POSTSCF LMOSC Boys 1000 1.e-10'
    else:
        print >>f, 'SCF LOSC !!!!!!!!!!!!!!'
    if args.window != '0':
        print >>f, 'LOEnergy  ' + args.window

    print >>f, claims.inp_temp_losc
    f.close()
    element = read_elements(args.f_xyz)
    write_basis(f_inp, element, args.basis)
    write_fitbasis(f_inp, element, args.fitbasis)
    f = open(f_inp, 'a')
    print >>f, 'end'
    print >>f, '$doqm'
    f.close()


def hf_inp(args):
    if args.g09 == True:
        hf_inp_g09(args)
    else:
        hf_inp_qm4d(args)


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
    
    if args.guess == 'atom':
        print >>f, 'guess  atom'
    else:
        print >>f, 'guess read ' + args.guess

    print >>f, claims.inp_temp
    f.close()
    element = read_elements(args.f_xyz)
    write_basis(f_inp, element, args.basis)
    f = open(f_inp, 'a')
    print >>f, 'end'
    print >>f, '$doqm'
    f.close()


def hf_inp_g09(args):
    f_inp = args.f_xyz[0:-4]+ '.com'
    f_xyz = args.f_xyz
    f_name = args.f_xyz[0:-4]

    command  = '# ' + 'hf/'
    command += args.basis
    command += ' 6d 10f Int=NoBasisTransform NoSymm'

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

    write_xyz_g09('g09/'+f_inp, f_xyz)
    f = open('g09/' + f_inp, 'a')
    print >>f, ''
    f.close()


def check_arg(args):
    # check if the parse args are valid
    # return just the name of f_xyz file
    # key args check
    if os.path.isfile(args.f_xyz) != True:
        print "Terminated: coordinate file not existed!\n"
        sys.exit()
    if args.partition not in sub_claims.partition_name:
        print "Terminated: not a partition name\n"
        sys.exit()
    if args.f_xyz.endswith('.xyz') != True:
        print "Terminated: not a coordinate file\n"
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
    if int(args.mem) > sub_claims.partition_mem[args.partition]:
        print 'Terminated: arg[mem] oversize, max={}G\n'.\
                format(sub_claims.partition_mem[args.partition])
        sys.exit()
#    if int(args.mem) > sub_claims.partition_mem['mei11950']:
#        print "Terminated: arg[mem] oversize\n"
#        sys.exit()
#    if int(args.mem) > sub_claims.partition_mem['mei1super']:
#        print "Terminated: arg[mem] oversize\n"
#        sys.exit()
#    if int(args.mem) > sub_claims.partition_mem['mei2']:
#        print "Terminated: arg[mem] oversize\n"
#        sys.exit()
#    if int(args.mem) > sub_claims.partition_mem['mei3']:
#        print "Terminated: arg[mem] oversize\n"
#        sys.exit()
#    if int(args.mem) > sub_claims.partition_mem['mei2med']:
#        print "Terminated: arg[mem] oversize\n"
#        sys.exit()
#    if int(args.mem) > sub_claims.partition_mem['mei2big']:
#        print "Terminated: arg[mem] oversize\n"
#        sys.exit()
#    if int(args.mem) > sub_claims.partition_mem['mei2hug']:
#        print "Terminated: arg[mem] oversize\n"
#        sys.exit()



def read_elements(f_xyz):
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
    f = open(f_inp, 'a')
    for i in element:
        string = 'basis    ' + i + ' ' + i + '.' + basis + '\n'
        f.write(string)
    f.close()


def write_fitbasis(f_inp, element, basis):
    f = open(f_inp, 'a')
    for i in element:
        string = 'fitbasis ' + i + ' ' + i + '.' + basis + '\n'
        f.write(string)
    f.close()

def write_xyz_g09(f_inp, f_xyz):
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


if __name__ == "__main__":
    print read_elements('1.xyz')


