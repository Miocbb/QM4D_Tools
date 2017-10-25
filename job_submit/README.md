# job_submit
job submit for qm4d or g09 package

Use f_name.xyz file to wirte the input files needed for QM calculations.
qm4d: f_name.inp, slurm
g09 : f_name.com, slurm

sbatch command is used to submit jobs.
python 2.7 was used for implementation.

Run sub.py to see usage details.

# Note:
-----------------------------------
args.charge: required as an integer

-----------------------------------
args.____elec_num: the current total electron number

-----------------------------------
the elctron configuration is always defaulted as the lowest
configuration, when mult command is not used.

-----------------------------------
args.aocc and args.bocc only possess the capability to
set ONE zero or fractional charge occupation in orbitals
with spin alpha or beta.

[-aocc(bocc) num1 num2] usage:
num1 refers to the relative postion of the occupation setting.
0 stands for HOMO orbital with alpha(beta) spin.
-i stands for the HOMO-i orbitals with alpha(beta) spin.
+i(i) stands for the HOMO+i orbitals with alpha(beta) spin.

-----------------------------------
[-basis basis] usage:
this program stores some commonly used basis sets
(see var 'basis_input_option' in 'source/sub_claims.py').
If the using basis is one of these stored choices, input
choice is not case-sensitive. Otherwise a sys_warining will be
raised, the automatically submission will be suspended, and
the basis input will be treated case-sensitively.

If QM4D package is used for calcultion, this program will check
if the used basis is existed under the path specified by a global
variable 'QM4D_GTOLIB' (defaulted in file 'source/sub_claims.py').

If g09 package is used for calculation, basis existence will not be
checked.
-----------------------------------
