#!/usr/bin/python
import argparse
import wqm_func 


def main():
    # Create parent parser
    # Necessary arguments to write QM4D inp file
    # args = {f_xyz, spin, charge, mult, basis, -guess}
    parent_parser = argparse.ArgumentParser(add_help=False)
    parent_parser.add_argument('f_xyz',  help = 'coordinate file')
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
    
    
    # Cerate top-level parser
    parser = argparse.ArgumentParser(description=
                """Use *.xyz file to wirte the input
                files needed for QM4D calculations""")
    # Create sub-level parser for command {dft, losc, hf}
    subparser = parser.add_subparsers(help= "Calculation method choices")
    
    # Create parser for "dft" command
    parser_dft = subparser.add_parser('dft',
                    help='DFT calculation with standard dfa',
                    parents=[parent_parser])
    parser_dft.add_argument('-dfa', default = 'b3lyp',
                    help='Default=b3lyp')
    parser_dft.set_defaults(func=wqm_func.dft_inp, method='dft')
    
    # Create parser for "losc" command
    parser_losc = subparser.add_parser('losc', parents=[parent_parser],
                    help='DFT calculation with LOSC dfa')
    parser_losc.add_argument('-dfa', default = 'b3lyp',
                    help='Default=b3lyp')
    parser_losc.add_argument('-fitbasis', default = 'aug-cc-pVTZ',
                    help='Default=aug-cc-pVTZ')
    parser_losc.add_argument('-window', default = '-30  10',
                    help='Default="-30 10", [set LOSC calculation wimdow]')
    parser_losc.add_argument('-postSCF', default = '1',
                    help='Default=1 [1:POSTSCF  0:SCF]')
    parser_losc.set_defaults(func=wqm_func.losc_inp, method='losc')
    
    # Create parser for "hf" command
    parser_hf = subparser.add_parser('hf', help='HF calculation',
                    parents=[parent_parser])
    parser_hf.set_defaults(func=wqm_func.hf_inp, method='hf')
    

    args = parser.parse_args()
    print args
    # Check if all the args are valid
    wqm_func.check_arg(args)
    # Start writing the input file
    args.func(args)


if __name__ == "__main__":
    main()
