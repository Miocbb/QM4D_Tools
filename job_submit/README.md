# job_submit
job submit for qm4d or g09 package

Use f_name.xyz file to wirte the input files needed for QM calculations.
qm4d: f_name.inp, slurm
g09 : f_name.com, slurm

sbatch command is used to submit jobs.
python 2.7 was used for implementation.

Run sub.py to see usage details.

# Note:
args.charge: required as an integer

args.____elec_num: the current total electron number

the elctron configuration is always defaulted as the lowest
configuration, when mult command is not used.

args.aocc and args.bocc only possess the capability to
set ONE zero or fractional charge in spin alpha or beta.
