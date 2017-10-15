# inp file template
import argparse

partition_mem = {'mei11950':14,
                 'mei1super': 20,
                 'mei1blade': 29,
                 'mei2': 29,
                 'mei3': 29,
                 'mei2med': 60,
                 'mei2big': 120,
                 'mei2hug': 250}

partition_name = {'mei1blade', 'mei11950', 
                  'mei1super', 'mei2',
                  'mei3', 'mei2med',
                  'mei2big', 'mei2hug'}

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
parent_parser.add_argument('-spin',   default = '2',
                help = 'Default=2 [2:Unrestricted; 1:restricted]')
parent_parser.add_argument('-charge', default = '0',
                help = 'Default=0')
parent_parser.add_argument('-mult',  default = '1',
                help = 'Default=1')
parent_parser.add_argument('-basis', default = 'cc-pVTZ',
                help='Default="cc-pVTZ"')
parent_parser.add_argument('-guess',  default='atom',
                help='Default=atom [inital guess option]',)
parent_parser.add_argument('-cpu', default='8',
                help='[Default: qm4d=1 g09=8]')
parent_parser.add_argument('-mem', default='10',
                help='Default=10G')
 
