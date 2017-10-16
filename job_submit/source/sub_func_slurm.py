import sub_claims
import subprocess
import os.path
import os

def hf_slurm(args):
    job_name = args.f_xyz[0:-4] + '.hf'
    name_xyz = args.f_xyz[0:-4]
    f_inp = name_xyz + '.inp'
    # create slurm file
    if args.g09 == True:
        f = open('g09/slurm', 'w')
        job_name += '.g09'
        f_inp = name_xyz + '.com'
    else:
        f = open('slurm', 'w')
    # start writing slurm
    print >>f, '#!/bin/bash'
    print >>f, '#SBATCH --job-name ' + job_name
    print >>f, '#SBATCH --time=' +\
            str(sub_claims.partition_time[args.partition])
    print >>f, '#SBATCH --nodes=1'
    print >>f, '#SBATCH --mem=' + args.mem + 'G'
    print >>f, '#SBATCH --cpus-per-task=1'
    print >>f, '#SBATCH --partition=' + args.partition
    print >>f, '#SBATCH --mail-type=FAIL'
    print >>f, '#SBATCH --mail-user=ym95'
    # write slurm command line
    if args.g09 == True:
        print >>f, '#SBATCH --ntasks-per-node=' + args.cpu
        print >>f, 'g09 ' + f_inp
    else:
        print >>f, '#SBATCH --ntasks-per-node=1'
        print >>f, 'qm4d_git ' + f_inp +\
                ' > ' + name_xyz + '.out'
    # finished wrting slurm


def dft_slurm(args):
    job_name = args.f_xyz[0:-4] + '.' + args.dfa
    name_xyz = args.f_xyz[0:-4]
    f_inp = name_xyz + '.inp'
    # create slurm file
    if args.g09 == True:
        f = open('g09/slurm', 'w')
        job_name += '.g09'
        f_inp = name_xyz + '.com'
    else:
        f = open('slurm', 'w')
    # start writing slurm
    print >>f, '#!/bin/bash'
    print >>f, '#SBATCH --job-name ' + job_name
    print >>f, '#SBATCH --time=' +\
            str(sub_claims.partition_time[args.partition])
    print >>f, '#SBATCH --nodes=1'
    print >>f, '#SBATCH --mem=' + args.mem + 'G'
    print >>f, '#SBATCH --cpus-per-task=1'
    print >>f, '#SBATCH --partition=' + args.partition
    print >>f, '#SBATCH --mail-type=FAIL'
    print >>f, '#SBATCH --mail-user=ym95'
    # write slurm command line
    if args.g09 == True:
        print >>f, '#SBATCH --ntasks-per-node=' + args.cpu
        print >>f, 'g09 ' + f_inp
    else:
        print >>f, '#SBATCH --ntasks-per-node=1'
        print >>f, 'qm4d_git ' + f_inp +\
                ' > ' + name_xyz + '.out'
    # finished wrting slurm


def losc_slurm(args):
    job_name = args.f_xyz[0:-4] + '.' + args.dfa
    name_xyz = args.f_xyz[0:-4]
    f_inp = name_xyz + '.inp'
    # create slurm file
    f = open('slurm', 'w')
    # start writing slurm
    print >>f, '#!/bin/bash'
    print >>f, '#SBATCH --job-name ' + job_name
    print >>f, '#SBATCH --time=' +\
            str(sub_claims.partition_time[args.partition])
    print >>f, '#SBATCH --nodes=1'
    print >>f, '#SBATCH --mem=' + args.mem + 'G'
    print >>f, '#SBATCH --cpus-per-task=1'
    print >>f, '#SBATCH --partition=' + args.partition
    print >>f, '#SBATCH --mail-type=FAIL'
    print >>f, '#SBATCH --mail-user=ym95'
    print >>f, 'qm4d_git ' + f_inp + ' > ' + name_xyz + '.out'
    # finished wrting slurm


def sbatch(args):
    """
    brief:  submit jobs with external command 'sbatch'.

    return: 1 (submitted jobs)
            0 (only create inp files)
    """
    if args.nosub: # require no job submit
        return 0
    if args.method != 'losc':
        if args.g09 == True: # sbatch g09
            if os.path.isfile('g09/slurm') == True:
                os.chdir('g09')
                subprocess.call(['sbatch', 'slurm'])
                os.chdir('..')
            else:
                print 'Terminated: No slurm file in g09 dir'
                sys.exit()
        else: # sbatch qm4d
            if os.path.isfile('slurm') == True:
                subprocess.call(['sbatch', 'slurm'])
            else:
                print 'Terminated: No slurm file'
                sys.exit()
    else:
        if os.path.isfile('slurm') == True:
            subprocess.call(['sbatch', 'slurm'])
        else:
            print 'Terminated: No slurm file'
            sys.exit()
    return 1
 

