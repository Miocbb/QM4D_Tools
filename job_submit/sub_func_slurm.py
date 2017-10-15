import sub_claims

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
    pass

