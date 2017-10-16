"""
main function module for Project 'sub'
"""
import argparse
import sub_claims as s_claims
import sub_func_slurm as sf_slurm
import sub_func_inp as sf_inp


def hf_main(args):
    """
    hf calculation main function
    """
    sf_inp.hf_inp(args)
    sf_slurm.hf_slurm(args)
    if not sf_slurm.sbatch(args):
        print 'successfully create inp files'


def dft_main(args):
    """
    standard dft calculation main function
    """
    sf_inp.dft_inp(args)
    sf_slurm.dft_slurm(args)
    if not sf_slurm.sbatch(args):
        print 'successfully create inp files'


def losc_main(args):
    """
    DFT with losc functional main function
    """
    sf_inp.losc_inp(args)
    sf_slurm.losc_slurm(args)
    if not sf_slurm.sbatch(args):
        print 'successfully create inp files'

def Parser():
    # Cerate top-level parser
    parser = argparse.ArgumentParser(description=
                """Use f_name.xyz file to wirte the input
                files needed for QM calculations.
                {qm4d: f_name.inp, slurm},
                {g09 : f_name.com, slurm}""")
    # Create sub-level parser for command {dft, losc, hf}
    subparser = parser.add_subparsers(help= "Calculation method choices")
    # Create parser for "dft" command
    parser_dft = subparser.add_parser('dft',
                    help='DFT calculation with standard dfa',
                    parents=[s_claims.parent_parser])
    parser_dft.add_argument('-dfa', default = 'b3lyp', dest='dfa',
                    help='Default=b3lyp')
    parser_dft.add_argument('-g09', action='store_true', dest='g09',
                    help='[calculation package: g09]')
    parser_dft.set_defaults(_func=dft_main, _method='dft')
    # Create parser for "losc" command
    parser_losc = subparser.add_parser('losc', parents=[s_claims.parent_parser],
                    help='DFT calculation with LOSC dfa')
    parser_losc.add_argument('-dfa', default = 'b3lyp', dest='dfa',
                    help='Default=b3lyp')
    parser_losc.add_argument('-fitbasis', default = 'aug-cc-pVTZ',
                    dest='fitbasis', help='Default=aug-cc-pVTZ')
    parser_losc.add_argument('-window', default = '-30  10', dest='window',
                    help='Default="-30 10", [set LOSC calculation wimdow]')
    parser_losc.add_argument('-postSCF', default = '1', dest='postSCF',
                    help='Default=1 [1:POSTSCF  0:SCF]')
    parser_losc.set_defaults(_func=losc_main, _method='losc')
    # Create parser for "hf" command
    parser_hf = subparser.add_parser('hf', help='HF calculation',
                    parents=[s_claims.parent_parser])
    parser_hf.add_argument('-g09', action='store_true', dest='g09',
                    help='[calculation package: g09]')
    parser_hf.set_defaults(_func=hf_main, _method='hf')
    return parser.parse_args()




