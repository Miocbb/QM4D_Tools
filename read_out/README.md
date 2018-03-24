# Introduction

Read the interested output results from **QM4D** or **g09** package.


## List of scripts
*****************
### form_PES.py:
##### Description:
Use to eigenvalues from DFT calculation to form Photoemission Spectrum (PES) by applying Gaussian expanssian.  A spectrum file with ".spec" extension will be created.
##### Usage:
```shell
./form_PES.py eig.eig
eig.eig:    the eigenvalue file created from running **read_eig_losc_qm4d.py**.
```
##### Note:
2. **[spectrum].spec** file will be created by this script under current execute directory.
3. The peaks of PES is started from a value specified by user (which is used to locate the left-most peak) and ended at LUMO orbital.


*****************
### read_density_g09.py
##### Description:
This python script is used to extract densitry (dst) matrix from **g09** output. A file with ".txt" extension will be generated which can be used directly as `guess read` file for **QM4D** package.  The density file will be created under the same folder as g09 output directory, if `-n` flag is not specified.
##### Usage:
```shell
./read_density_g09.py [-h, -n] f_chk

f_chk:  g09 output file. Do not accept "*" expression.
        Only specify one output file at one execution.
-h:     show help information then exit.
-n:     specified a customized output name with a user-defined
        path to save output file.
```

##### Note:
1. `g09.chk` file is required to execute this script.
2. if `-n` flag is not specified, `density.txt` file is defaultly created under the same directory where the g09 output file is located.  Otherwise, it will be created under the specified directory with costumized name.

##### Work flow illustration:
    g09.chk --> check g09.log normal terminated --> g09.fchk (formchk) --> [dst].txt

*******************
### read_eig_losc_qm4d.py
##### Description:
This is python script is used to extract all the eigenvales from LOSC functional calculation from QM4D package. A file with ".eig" extension will be generated. The eigenvalue file will be created under the same flder as QM4D output file, if `-n` flag is not specifed. The format of [eig].eig file is sperated columns, shown as below:
```
"spin    orbital    eig_prev    eig_losc".
```
##### Usage:
```shell
./read_eig_losc_qm4d.py [-h, -n] f_out

f_out     QM4D output file. Do not accept "*" expression.
          Only specify one output file at one execution.
-h        show help information then exit.
-n        specified a customized output name with a user-defined path to
          save output file.
```

##### Note:
if `-n` flag is not specified, eigenvalue.eig file is defaultly created under the same directory where the QM4D output file is located.  Otherwise, it will be created under the specified directory with costumized name.  Eigenvalues are extracted based on the **eig_proj** key word.

##### Work flow:
    qm4d.out check normal terminated --> [eig].eig

*******************
### calcxyz.py
##### Description
a script used to calculate the distance between two atoms, the bond angle of
three atoms.

##### usage:
```shell
    python3 calcxzy.py xyz_file [-dist num1, num2] [-angle num1, num2, num3]
```

1. The xyz_file are the path (absolute or relative path) to the xyz file.
   Each line in the xyz file start with a atom name and followed by three
   number (x, y and z coordinates).

2. num1, num2, num3 are the line number of each atoms in the xyz file.

3. the center atom in angle calculation is atom2 (num2).
