"""
functions related to slurm
"""

import sys
import subprocess
import os.path
import os
import sub_claims as s_claims
from sub_func_support import SigExit


def hf_slurm(args):
    #job_name = args.f_xyz[0:-4] + '.hf'
    f_inp_name   = args._f_inp_name
    f_out_name   = args._f_out_name
    f_com_name   = args._f_com_name
    f_slurm_name = args._f_slurm_name
    job_name = args._job_name
    partition = s_claims.partition_name[args.partition]
    # create slurm file
    if args.g09 == True:
        f = open('g09/' + f_slurm_name, 'w')
        job_name += '.g09'
    else:
        f = open(f_slurm_name, 'w')
    # start writing slurm
    print >>f, '#!/bin/bash'
    print >>f, '#SBATCH --job-name ' + job_name
    print >>f, '#SBATCH --time=' +\
            str(s_claims.partition_time[args.partition])
    print >>f, '#SBATCH --nodes=1'
    print >>f, '#SBATCH --ntasks=' + args.cpu
    print >>f, '#SBATCH --mem=' + args.mem + 'G'
    #print >>f, '#SBATCH --cpus-per-task=1'
    print >>f, '#SBATCH --partition=' + partition
    print >>f, '#SBATCH --mail-type=FAIL'
    print >>f, '#SBATCH --mail-user=ym95'
    # write slurm command line
    if args.g09 == True:
        print >>f, 'g09 ' + f_com_name
    else:
        print >>f, 'export OMP_NUM_THREADS=' + args.cpu
        print >>f, 'qm4d_omp ' + f_inp_name +\
                ' > ' + f_out_name
    # finished wrting slurm


def dft_slurm(args):
    #job_name = args.f_xyz[0:-4] + '.' + args.dfa
    f_inp_name   = args._f_inp_name
    f_out_name   = args._f_out_name
    f_com_name   = args._f_com_name
    f_slurm_name = args._f_slurm_name
    job_name = args._job_name
    partition = s_claims.partition_name[args.partition]
    # create slurm file
    if args.g09 == True:
        f = open('g09/' + f_slurm_name, 'w')
        job_name += '.g09'
    else:
        f = open(f_slurm_name, 'w')
    # start writing slurm
    print >>f, '#!/bin/bash'
    print >>f, '#SBATCH --job-name ' + job_name
    print >>f, '#SBATCH --time=' +\
            str(s_claims.partition_time[args.partition])
    print >>f, '#SBATCH --nodes=1'
    print >>f, '#SBATCH --ntasks=' + args.cpu
    print >>f, '#SBATCH --mem=' + args.mem + 'G'
    #print >>f, '#SBATCH --cpus-per-task=1'
    print >>f, '#SBATCH --partition=' + partition
    print >>f, '#SBATCH --mail-type=FAIL'
    print >>f, '#SBATCH --mail-user=ym95'
    # write slurm command line
    if args.g09 == True:
        print >>f, 'g09 ' + f_com_name
    else:
        print >>f, 'export OMP_NUM_THREADS=' + args.cpu
        print >>f, 'qm4d_omp ' + f_inp_name +\
                ' > ' + f_out_name
    # finished wrting slurm


def losc_slurm(args):
    f_inp_name   = args._f_inp_name
    f_out_name   = args._f_out_name
    f_slurm_name = args._f_slurm_name
    job_name = args._job_name
    partition = s_claims.partition_name[args.partition]
    # create slurm file
    f = open(f_slurm_name, 'w')
    # start writing slurm
    print >>f, '#!/bin/bash'
    print >>f, '#SBATCH --job-name ' + job_name
    print >>f, '#SBATCH --time=' +\
            str(s_claims.partition_time[args.partition])
    print >>f, '#SBATCH --nodes=1'
    print >>f, '#SBATCH --mem=' + args.mem + 'G'
    print >>f, '#SBATCH --ntasks=' + args.cpu
    print >>f, '#SBATCH --partition=' + partition
    print >>f, '#SBATCH --mail-type=FAIL'
    print >>f, '#SBATCH --mail-user=ym95'
    print >>f, 'export OMP_NUM_THREADS=' + args.cpu
    print >>f, 'qm4d_omp ' + f_inp_name + ' > ' + f_out_name
    # finished wrting slurm


def real_sbatch(args):
    """
    brief:  submit jobs with external command 'sbatch'.

    return: 1 (submitted jobs)
            0 (only create inp files)
    """
    f_inp_name   = args._f_inp_name
    f_out_name   = args._f_out_name
    f_com_name   = args._f_com_name
    f_slurm_name = args._f_slurm_name
    job_name = args._job_name
    if args.nosub: # require no job submit
        return 0
    if args._method == 'losc':
        if os.path.isfile(f_slurm_name) == True:
            subprocess.call(['sbatch', f_slurm_name])
        else:
            SigExit('Terminated: No slurm file to sbatch')
    else:
        if args.g09 == True: # sbatch g09
            if os.path.isfile('g09/' + f_slurm_name) == True:
                os.chdir('g09')
                subprocess.call(['sbatch', f_slurm_name])
                os.chdir('..')
            else:
                SigExit('Terminated: No slurm file in g09 dir to sbatch')
        else: # sbatch qm4d
            if os.path.isfile(f_slurm_name) == True:
                subprocess.call(['sbatch', f_slurm_name])
            else:
                SigExit('Terminated: No slurm file to sbatch')
    return 1

def sbatch(args):
    print "Request memory: %s G" %args.mem # show mem information
    if args._sys_warning:
        SigExit("Create inp files. Check before submit jobs!")
    status = real_sbatch(args)
    if status == 0:
        print 'Created inp files. Green to submit manually!'
