# Introduction
job submit script for **QM4D** or **g09** package.

This script will use coordinate file, `f_name.xyz`, to wirte the needed files for QM calculations.The generated files for **QM4D** and **g09** are listed below.
**QM4D**: f_name.inp, slurm
**g09**: f_name.com, slurm

## Requirement
1. `sbatch`
1. `python 2.7`

# Note:
1. `-charge`: required as an integer
1. `args._elec_num`: the current total electron number
1. The elctron configuration is always defaulted as the lowest configuration, when `-mult` flag is not used.
1. `-aocc` and `-bocc` only possess the capability to set **ONE** zero or fractional charge occupation in orbitals with spin alpha or beta.
1. `[-aocc(bocc) num1 num2]` usage: `num1` refers to the relative postion of the occupation setting.  `0` stands for HOMO orbital with alpha(beta) spin.  `-i` stands for the HOMO-i orbitals with alpha(beta) spin.  `+i`(or just using `i`) stands for the HOMO+i orbitals with alpha(beta) spin.
1. `[-basis basis]` usage: this program stores some commonly used basis sets (see var `basis_input_option` in `source/sub_claims.py`).  If the using basis is one of these stored choices, input choice is not case-sensitive. If it is not, a sys_warining will be raised, the automatically submission will be suspended, and the basis input will be treated case-sensitively.
1. If **QM4D** package is used for calcultion, this program will check if the used basis is existed under the path specified by a global variable `QM4D_GTOLIB` (defaulted in file `source/sub_claims.py`).
1. If **g09** package is used for calculation, basis existence will not be checked.
1. `[-mem mem]` usage: memory request is defaulted to be auto-setted.  For **QM4D** package, the auto-setted memory is based on the total number of CGTO.  40CGTO = 1G
1. For **g09** package, the auto-setted memory is based on the total number of electrons (considering the charge of the system) and the type of the basis set.
1. when flag, `-mem`, is specified, the costumized memory set will be used.
