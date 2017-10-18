import argparse

# qm4d supported functionals
dfa_qm4d={'b3lyp', 'blyp', 'lda', 'pbe'}

# g09 supported  functionals
dfa_g09={'b3lyp', 'blyp', 'lda', 'pbe'}

# input option for basis of fitbasis
basis_input_option={
'STO-3G', '6-31G', '6-31GS', '6-31GSS',
'6-311GS', '6-311++G_3DF_3PD',
'CC-PVDZ', 'CC-PVTZ', 'CC-PVQZ',
'CC-PV5Z', 'CC-PV6Z',
'AUG-CC-PVDZ', 'AUG-CC-PVTZ',
'AUG-CC-PVQZ', 'AUG-CC-PV5Z',
'AUG-CC-PV6Z'
}

# basis or fitbasis command for qm4d
basis_command_qm4d={
'STO-3G':  'STO-3G',
'6-31G':   '6-31G',
'6-31GS':  '6-31GS',
'6-31GSS': '6-31GSS',
'6-311GS': '6-311GS',
'6-311++G_3DF_3PD': '6-311++G_3df_3pd',
'CC-PVDZ': 'cc-pVDZ',
'CC-PVTZ': 'cc-pVTZ',
'CC-PVQZ': 'cc-pQTZ',
'CC-PV5Z': 'cc-p5TZ',
'CC-PV6Z': 'cc-p6TZ',
'AUG-CC-PVDZ': 'aug-cc-pVDZ',
'AUG-CC-PVTZ': 'aug-cc-pVTZ',
'AUG-CC-PVQZ': 'aug-cc-pVQZ',
'AUG-CC-PV5Z': 'aug-cc-pV5Z',
'AUG-CC-PV6Z': 'aug-cc-pV6Z'
}

# basis command for g09
basis_command_g09={
'STO-3G':  'sto-3g',
'6-31G':   '6-31g',
'6-31GS':  '6-31g*',
'6-31GSS': '6-31g**',
'6-311GS': '6-311g*',
'6-311++G_3DF_3PD': '6-311++g(3df,3pd)',
'CC-PVDZ': 'cc-pVDZ',
'CC-PVTZ': 'cc-pVTZ',
'CC-PVQZ': 'cc-pQTZ',
'CC-PV5Z': 'cc-p5TZ',
'CC-PV6Z': 'cc-p6TZ',
'AUG-CC-PVDZ': 'aug-cc-pVDZ',
'AUG-CC-PVTZ': 'aug-cc-pVTZ',
'AUG-CC-PVQZ': 'aug-cc-pVQZ',
'AUG-CC-PV5Z': 'aug-cc-pV5Z',
'AUG-CC-PV6Z': 'aug-cc-pV6Z'
}

# basis level for mem request
# mem = default_mem * basis_mem_level[basis]
basis_mem_level={
'STO-3G':  1,
'6-31G':   1,
'6-31GS':  1,
'6-31GSS': 1,
'6-311GS': 1,
'6-311++G_3DF_3PD': 2,
'CC-PVDZ': 1,
'CC-PVTZ': 1,
'CC-PVQZ': 2,
'CC-PV5Z': 2,
'CC-PV6Z': 2,
'AUG-CC-PVDZ': 2,
'AUG-CC-PVTZ': 2,
'AUG-CC-PVQZ': 3,
'AUG-CC-PV5Z': 3,
'AUG-CC-PV6Z': 3
}

# For qm4d inp file
# {args.dfa : dfa_command}
dfa_xcfunc_qm4d = {
'blyp' : 'xfunc  xb88\ncfunc  clyp',
'pbe'  : 'xfunc  xpbe\ncfunc  cpbe',
'b3lyp': 'xcfunc b3lyp',
'lda'  : 'xfunc  xlda\ncfunc  clda' }

# For g09 inp file
# {args.dfa : dfa_command }
dfa_xcfunc_g09 = {
'blyp' : 'blyp',
'pbe'  : 'pbepbe',
'b3lyp': 'b3lyp',
'lda'  : 'lsda' }

# {args.partition : max_mem}
partition_mem = {
'mei11950' : 14,
'mei1super': 20,
'mei1blade': 29,
'mei2'     : 29,
'mei3'     : 29,
'mei2med'  : 60,
'mei2big'  : 120,
'mei2hug'  : 250}

# {args.partition : max_time}
partition_time = {
'mei11950' : 10000,
'mei1super': 10000,
'mei1blade': 10000,
'mei2'     : 10000,
'mei3'     : 10000,
'mei2med'  : 40000,
'mei2big'  : 40000,
'mei2hug'  : 40000}

# {args.partition : partition_name}
partition_name = {
'mei11950' : 'mei1_dell_1950',
'mei1super': 'mei1_supermicro',
'mei1blade': 'mei1_dell_blade',
'mei2'     : 'mei2',
'mei3'     : 'mei3',
'mei2med'  : 'mei2_medmem',
'mei2big'  : 'mei2_bigmem',
'mei2hug'  : 'mei3_hugmem'}

# {element : elec_num}
element_table = {
'H' :1  , 'He':2  , 'Li':3  , 'Be':4  , 
'B' :5  , 'C' :6  , 'N' :7  , 'O' :8  , 
'F' :9  , 'Ne':10 , 'Na':11 , 'Mg':12 , 
'Al':13 , 'Si':14 , 'P' :15 , 'S' :16 , 
'Cl':17 , 'Ar':18 , 'K' :19 , 'Ca':20 , 
'Sc':21 , 'Ti':22 , 'V' :23 , 'Cr':24 , 
'Mn':25 , 'Fe':26 , 'Co':27 , 'Ni':28 , 
'Cu':29 , 'Zn':30 , 'Ga':31 , 'Ge':32 , 
'As':33 , 'Se':34 , 'Br':35 , 'Kr':36 , 
'Rb':37 , 'Sr':38 , 'Y' :39 , 'Zr':40 , 
'Nb':41 , 'Mo':42 , 'Tc':43 , 'Ru':44 , 
'Rh':45 , 'Pd':46 , 'Ag':47 , 'Cd':48 , 
'In':49 , 'Sn':50 , 'Sb':51 , 'Te':52 , 
'I' :53 , 'Xe':54 , 'Cs':55 , 'Ba':56 , 
'La':57 , 'Ce':58 , 'Pr':59 , 'Nd':60 , 
'Pm':61 , 'Sm':62 , 'Eu':63 , 'Gd':64 , 
'Tb':65 , 'Dy':66 , 'Ho':67 , 'Er':68 , 
'Tm':69 , 'Yb':70 , 'Lu':71 , 'Hf':72 , 
'Ta':73 , 'W' :74 , 'Re':75 , 'Os':76 , 
'Ir':77 , 'Pt':78 , 'Au':79 , 'Hg':80 , 
'Tl':81 , 'Pb':82 , 'Bi':83 , 'Po':84 , 
'At':85 , 'Rn':86 , 'Fr':87 , 'Ra':88 , 
'Ac':89 , 'Th':90 , 'Pa':91 , 'U' :92 , 
'Np':93 , 'Pu':94 , 'Am':95 , 'Cm':96 , 
'Bk':97 , 'Cf':98 , 'Es':99 , 'Fm':100, 
'Md':101, 'No':102, 'Lr':103, 'Rf':104, 
'Db':105, 'Sg':106, 'Bh':107, 'Hs':108, 
'Mt':109, 'Ds':110, 'Rg':111, 'Cn':112, 
'Nh':113, 'Fi':114, 'Mc':115, 'Lv':116, 
'Ts':117, 'Og':118}

inp_temp_losc = (
"""iter        300
LOSC_r0     2.7
LOSC_eta    3.0
LOSC_eps    2.50
LOSC_gamma  2.0
LOSC_exf    1.23780
LOSC_pow    2.0
Boys Anal   20
dentol      1.0E-004
etol        1.0E-008
print       1
directvee
diis        12  0.30""")

#for dft and hf methods
inp_temp =(
"""iter      300
dentol    1.0E-004
etol      1.0E-008
print     1
directvee
diis      12  0.30""")

# Create parent parser
# Necessary arguments to write inp file
# args = {f_xyz, -spin, -charge, -mult, -basis, -guess, -g09}
parent_parser = argparse.ArgumentParser(add_help=False)
parent_parser.add_argument('f_xyz',  help = 'coordinate file')
parent_parser.add_argument('partition', help='choose partition')
parent_parser.add_argument('-in', default='-1', dest='inp_name',
                help='Default=f_xyz.inp(.com) [customized inp file name]')
parent_parser.add_argument('-on', default='-1', dest='out_name',
                help='Default=inp_name.out [customized out file name]')
parent_parser.add_argument('-sn', default='-1', dest='slurm_name',
                help='Default=slurm [customized slurm file name]')
parent_parser.add_argument('-jn', default='-1', dest='job_name',
                help='Default=f_xyz.method [customized job_name in slurm]')
parent_parser.add_argument('-no', action='store_true', dest='nosub',
                help='no job submission, only create inp')
parent_parser.add_argument('-spin',   default = '2', dest='spin',
                help = 'Default=2 [2:Unrestricted; 1:restricted]')
parent_parser.add_argument('-charge', default = '0', dest='charge',
                help = 'Default=0')
parent_parser.add_argument('-basis', default = 'cc-pVTZ', dest='basis',
                help='Default="cc-pVTZ"')
parent_parser.add_argument('-guess',  default='atom', dest='guess',
                help='Default=atom [inital guess option]',)
parent_parser.add_argument('-cpu', default='8', dest='cpu',
        help='Default=1(qm4d), 8(g09)')
parent_parser.add_argument('-mem', default='-1', dest='mem',
                help='Default=auto_set [based on elec_num]')
parent_parser.add_argument('-mult',  default = '-1', dest='mult',
                help ='Default=auto_set [based on elec_num]')
parent_parser.set_defaults(_f_inp_name=None, _f_out_name=None,
                           _f_com_name=None, _f_chk_name=None,
                           _f_slurm_name=None, _job_name=None,
                           _basis=None, _fitbasis=None,
                           _func=None, _method=None,
                           _elec_num=0,
                           _sys_warning=0)

